"""Enrich one CVE-bearing finding with private normalized KEV context."""

import logging
import os
import re
from typing import Any

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
DYNAMODB = boto3.resource("dynamodb")
CVE_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$")
OUTPUT_FIELDS = (
    "source",
    "catalog_version",
    "vendor_project",
    "product",
    "vulnerability_name",
    "date_added",
    "due_date",
    "required_action",
    "known_ransomware_campaign_use",
    "cwes",
)


def _optional_text(value: Any) -> str | None:
    """Return a trimmed nonempty string, or omit an unusable value."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def _cve_id_from_event(event: Any) -> str:
    """Read a CVE ID from a direct test event or a future EventBridge detail object."""
    if not isinstance(event, dict):
        raise RuntimeError("Expected a JSON object event")

    candidates = [event]
    detail = event.get("detail")
    if isinstance(detail, dict):
        candidates.append(detail)

    for candidate in candidates:
        cve_id = _optional_text(candidate.get("cve_id"))
        if cve_id:
            cve_id = cve_id.upper()
            if CVE_PATTERN.fullmatch(cve_id):
                return cve_id
            raise RuntimeError("cve_id must use the form CVE-YYYY-NNNN")

    raise RuntimeError("Event must include cve_id directly or under detail")


def _safe_indicator_context(item: dict[str, Any]) -> dict[str, Any]:
    """Return only the enrichment fields intended for a downstream finding."""
    context: dict[str, Any] = {}
    for field in OUTPUT_FIELDS:
        value = item.get(field)
        if value is not None:
            context[field] = value
    return context


def lambda_handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    """Look up one normalized CVE record without scanning or changing DynamoDB."""
    indicator_table = os.environ.get("INDICATOR_TABLE", "").strip()
    if not indicator_table:
        raise RuntimeError("INDICATOR_TABLE must be configured")

    cve_id = _cve_id_from_event(event)
    table = DYNAMODB.Table(indicator_table)
    response = table.get_item(Key={"cve_id": cve_id})
    item = response.get("Item")

    if not isinstance(item, dict):
        LOGGER.info("Enrichment completed: match=false")
        return {
            "status": "not_known_exploited",
            "cve_id": cve_id,
            "kev_match": False,
            "triage": "standard",
        }

    LOGGER.info("Enrichment completed: match=true")
    return {
        "status": "known_exploited",
        "cve_id": cve_id,
        "kev_match": True,
        "triage": "prioritize",
        "indicator": _safe_indicator_context(item),
    }

