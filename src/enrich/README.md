# CVE Finding Enrichment Lambda

This dependency-free Python Lambda handler takes one CVE-bearing finding event, performs an exact read of the normalized CISA KEV record, and returns a compact triage result. It is an intentionally small first step toward a later detection and investigation workflow.

## Deployment configuration

| Setting | Value |
| --- | --- |
| Runtime | Python 3.14 |
| Handler | `lambda_function.lambda_handler` |
| Execution role | A dedicated enrichment role created for this lab |
| Memory | 128 MB |
| Timeout | 10 seconds |
| VPC | None; the function only accesses DynamoDB through its execution role |

Set this environment variable in the Lambda console only; do not commit its value:

| Variable | Purpose |
| --- | --- |
| `INDICATOR_TABLE` | DynamoDB table that stores normalized indicator records |

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Python log level |

## Required role permissions

The dedicated enrichment role must retain its AWS-managed basic Lambda logging policy and have one inline permission:

- `dynamodb:GetItem` on only the normalized-indicator table.

Do not add `Scan`, `Query`, `PutItem`, `BatchWriteItem`, delete, list, administrative, cross-account, or broader DynamoDB permissions. The handler performs one exact primary-key lookup per finding.

## Accepted event shapes

For initial manual testing, pass a direct `cve_id`:

```json
{
  "cve_id": "CVE-YYYY-NNNN"
}
```

For a future EventBridge integration, the handler also accepts the CVE ID inside `detail`:

```json
{
  "detail": {
    "cve_id": "CVE-YYYY-NNNN"
  }
}
```

Use an existing public CVE identifier from the normalized table for the first match test. Do not commit the selected CVE, Lambda test event, output, table name, or logs.

## Result behavior

- A matching normalized record returns `status: known_exploited`, `kev_match: true`, `triage: prioritize`, and compact KEV context.
- A nonmatching CVE returns `status: not_known_exploited`, `kev_match: false`, and `triage: standard`.
- The handler never scans, writes to, or exposes raw-object locations from DynamoDB.
- Logs contain only the boolean match result, not the event payload, CVE identifier, table name, or indicator fields.

## Validation status

Source is prepared for deployment. The function must be deployed with the dedicated role and manually validated before any EventBridge source, notification workflow, or public interface is considered.

