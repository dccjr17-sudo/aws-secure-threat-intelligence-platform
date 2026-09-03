"""Normalize private CISA KEV raw snapshots into DynamoDB indicator records."""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any
from urllib.parse import unquote_plus

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
S3 = boto3.client("s3")
DYNAMODB = boto3.resource("dynamodb")
RAW_PREFIX = "raw/cisa-kev/"


def _optional_text(value: Any) -> str | None:
    """Return a nonempty string, or omit an unusable optional catalog value."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def _cwe_values(value: Any) -> list[str]:
    """Keep only nonempty CWE identifiers from the public catalog."""
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _normalized_item(
    vulnerability: Any,
    catalog_version: str,
    object_key: str,
    normalized_at: str,
) -> dict[str, Any]:
    """Produce one compact, query-ready indicator record from a catalog entry."""
    if not isinstance(vulnerability, dict):
        raise RuntimeError("CISA KEV catalog included a non-object vulnerability entry")

    cve_id = _optional_text(vulnerability.get("cveID"))
    if not cve_id:
        raise RuntimeError("CISA KEV catalog included an entry without cveID")

    item: dict[str, Any] = {
        "cve_id": cve_id,
        "source": "cisa-kev",
        "catalog_version": catalog_version,
        "raw_object_key": object_key,
        "normalized_at": normalized_at,
    }
    field_mapping = {
        "vendor_project": "vendorProject",
        "product": "product",
        "vulnerability_name": "vulnerabilityName",
        "date_added": "dateAdded",
        "due_date": "dueDate",
        "required_action": "requiredAction",
        "known_ransomware_campaign_use": "knownRansomwareCampaignUse",
    }
    for item_field, catalog_field in field_mapping.items():
        value = _optional_text(vulnerability.get(catalog_field))
        if value is not None:
            item[item_field] = value

    cwes = _cwe_values(vulnerability.get("cwes"))
    if cwes:
        item["cwes"] = cwes

    return item


def _event_objects(event: dict[str, Any]) -> list[tuple[str, str]]:
    """Extract and constrain S3 object locations from an S3 notification event."""
    records = event.get("Records")
    if not isinstance(records, list) or not records:
        raise RuntimeError("Expected an S3 event with at least one record")

    objects: list[tuple[str, str]] = []
    for record in records:
        if not isinstance(record, dict) or record.get("eventSource") != "aws:s3":
            raise RuntimeError("Only Amazon S3 notification events are supported")

        try:
            bucket = record["s3"]["bucket"]["name"]
            object_key = unquote_plus(record["s3"]["object"]["key"])
        except (KeyError, TypeError) as error:
            raise RuntimeError("S3 event did not include a bucket and object key") from error

        if not isinstance(bucket, str) or not bucket.strip():
            raise RuntimeError("S3 event included an invalid bucket name")
        if not object_key.startswith(RAW_PREFIX):
            raise RuntimeError("S3 event object is outside the approved CISA KEV raw prefix")
        objects.append((bucket, object_key))

    return objects


def _catalog_items(bucket: str, object_key: str, normalized_at: str) -> list[dict[str, Any]]:
    """Read one raw snapshot, validate its shape, and build all indicator items first."""
    response = S3.get_object(Bucket=bucket, Key=object_key)
    try:
        catalog = json.loads(response["Body"].read())
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError("Raw object was not valid CISA KEV JSON") from error

    vulnerabilities = catalog.get("vulnerabilities") if isinstance(catalog, dict) else None
    if not isinstance(vulnerabilities, list):
        raise RuntimeError("Raw object did not match the expected CISA KEV catalog shape")

    catalog_version = _optional_text(catalog.get("catalogVersion")) or "unknown"
    return [
        _normalized_item(entry, catalog_version, object_key, normalized_at)
        for entry in vulnerabilities
    ]


def lambda_handler(event: dict[str, Any], context: object) -> dict[str, int | str]:
    """Normalize raw CISA KEV S3 notifications into idempotent DynamoDB records."""
    indicator_table = os.environ.get("INDICATOR_TABLE", "").strip()
    if not indicator_table:
        raise RuntimeError("INDICATOR_TABLE must be configured")

    normalized_at = datetime.now(timezone.utc).isoformat()
    s3_objects = _event_objects(event)
    indicator_items: list[dict[str, Any]] = []
    for bucket, object_key in s3_objects:
        indicator_items.extend(_catalog_items(bucket, object_key, normalized_at))

    table = DYNAMODB.Table(indicator_table)
    with table.batch_writer(overwrite_by_pkeys=["cve_id"]) as batch:
        for item in indicator_items:
            batch.put_item(Item=item)

    LOGGER.info("Normalized CISA KEV indicators: count=%d", len(indicator_items))
    return {
        "status": "normalized",
        "processed_objects": len(s3_objects),
        "written_indicators": len(indicator_items),
    }
