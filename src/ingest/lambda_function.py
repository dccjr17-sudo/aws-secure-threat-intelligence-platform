"""Retrieve the public CISA KEV feed and preserve its raw JSON in private S3."""

import hashlib
import json
import logging
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
S3 = boto3.client("s3")

DEFAULT_SOURCE_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)
MAX_PAYLOAD_BYTES = 10 * 1024 * 1024


def _fetch_catalog(source_url: str) -> tuple[dict, bytes]:
    """Download a bounded JSON document and confirm the expected top-level shape."""
    request = Request(
        source_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "aws-threat-intel-lab/1.0",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            if response.getcode() != 200:
                raise RuntimeError(f"Source returned HTTP {response.getcode()}")
            payload = response.read(MAX_PAYLOAD_BYTES + 1)
    except (HTTPError, URLError) as error:
        raise RuntimeError("Unable to retrieve the public threat-intelligence feed") from error

    if len(payload) > MAX_PAYLOAD_BYTES:
        raise RuntimeError("Source payload exceeded the configured size limit")

    try:
        catalog = json.loads(payload)
    except json.JSONDecodeError as error:
        raise RuntimeError("Source response was not valid JSON") from error

    if not isinstance(catalog, dict) or not isinstance(catalog.get("vulnerabilities"), list):
        raise RuntimeError("Source JSON did not match the expected CISA KEV catalog shape")

    return catalog, payload


def lambda_handler(event: dict, context: object) -> dict:
    """Store one raw CISA KEV snapshot and return safe operational metadata."""
    raw_bucket = os.environ.get("RAW_BUCKET", "").strip()
    if not raw_bucket:
        raise RuntimeError("RAW_BUCKET must be configured")

    source_url = os.environ.get("SOURCE_URL", DEFAULT_SOURCE_URL).strip()
    catalog, payload = _fetch_catalog(source_url)

    captured_at = datetime.now(timezone.utc)
    payload_sha256 = hashlib.sha256(payload).hexdigest()
    object_key = (
        f"raw/cisa-kev/ingest_date={captured_at.date().isoformat()}/"
        f"known_exploited_vulnerabilities-"
        f"{captured_at.strftime('%H%M%S')}-{payload_sha256[:12]}.json"
    )
    catalog_version = str(catalog.get("catalogVersion", "unknown"))[:128]

    S3.put_object(
        Bucket=raw_bucket,
        Key=object_key,
        Body=payload,
        ContentType="application/json",
        ServerSideEncryption="AES256",
        Metadata={
            "source": "cisa-kev",
            "sha256": payload_sha256,
            "catalog-version": catalog_version,
        },
    )

    LOGGER.info(
        "Stored raw CISA KEV catalog: key=%s sha256_prefix=%s",
        object_key,
        payload_sha256[:12],
    )
    return {
        "status": "stored",
        "source": "cisa-kev",
        "catalog_version": catalog_version,
        "object_key": object_key,
        "sha256": payload_sha256,
        "bytes": len(payload),
    }

