"""Enrich CVE findings with private normalized KEV context and alert on matches."""

import json
import logging
import os
import re
from typing import Any

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
DYNAMODB = boto3.resource("dynamodb")
SNS = boto3.client("sns")

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


def _valid_cve_id(value: Any) -> str | None:
    """Return an uppercase CVE ID when the value is valid."""
    cve_id = _optional_text(value)
    if not cve_id:
        return None

    cve_id = cve_id.upper()
    if CVE_PATTERN.fullmatch(cve_id):
        return cve_id
    raise RuntimeError("cve_id must use the form CVE-YYYY-NNNN")


def _cve_id_from_event(event: Any) -> str:
    """Read a CVE from a direct test, custom EventBridge, or Inspector event."""
    if not isinstance(event, dict):
        raise RuntimeError("Expected a JSON object event")

    direct_cve_id = _valid_cve_id(event.get("cve_id"))
    if direct_cve_id:
        return direct_cve_id

    detail = event.get("detail")
    if not isinstance(detail, dict):
        raise RuntimeError("Event must include cve_id directly or under detail")

    detail_cve_id = _valid_cve_id(detail.get("cve_id"))
    if detail_cve_id:
        return detail_cve_id

    package_details = detail.get("packageVulnerabilityDetails")
    if isinstance(package_details, dict):
        inspector_cve_id = _valid_cve_id(package_details.get("vulnerabilityId"))
        if inspector_cve_id:
            return inspector_cve_id

    raise RuntimeError(
        "Event must include cve_id directly, under detail, or in "
        "detail.packageVulnerabilityDetails.vulnerabilityId"
    )


def _safe_indicator_context(item: dict[str, Any]) -> dict[str, Any]:
    """Return only enrichment fields intended for a downstream finding."""
    context: dict[str, Any] = {}
    for field in OUTPUT_FIELDS:
        value = item.get(field)
        if value is not None:
            context[field] = value
    return context


def _publish_kev_alert(cve_id: str, indicator: dict[str, Any]) -> bool:
    """Publish a compact alert only when an alert topic is configured."""
    alert_topic_arn = os.environ.get("ALERT_TOPIC_ARN", "").strip()
    if not alert_topic_arn:
        return False

    message = {
        "alert": "known_exploited_vulnerability_match",
        "cve_id": cve_id,
        "triage": "prioritize",
        "kev_match": True,
        "indicator": indicator,
    }

    SNS.publish(
        TopicArn=alert_topic_arn,
        Subject=f"TI Lab: KEV match {cve_id}",
        Message=json.dumps(message, indent=2, sort_keys=True, default=str),
    )
    return True


def lambda_handler(event: dict[str, Any], context: object) -> dict[str, Any]:
    """Look up one CVE without scanning or changing DynamoDB."""
    indicator_table = os.environ.get("INDICATOR_TABLE", "").strip()
    if not indicator_table:
        raise RuntimeError("INDICATOR_TABLE must be configured")

    cve_id = _cve_id_from_event(event)
    table = DYNAMODB.Table(indicator_table)
    response = table.get_item(Key={"cve_id": cve_id})
    item = response.get("Item")

    if not isinstance(item, dict):
        LOGGER.info("Enrichment completed: match=false alert_sent=false")
        return {
            "status": "not_known_exploited",
            "cve_id": cve_id,
            "kev_match": False,
            "triage": "standard",
            "alert_sent": False,
        }

    indicator = _safe_indicator_context(item)
    alert_sent = _publish_kev_alert(cve_id, indicator)

    LOGGER.info("Enrichment completed: match=true alert_sent=%s", alert_sent)
    return {
        "status": "known_exploited",
        "cve_id": cve_id,
        "kev_match": True,
        "triage": "prioritize",
        "alert_sent": alert_sent,
        "indicator": indicator,
    }
