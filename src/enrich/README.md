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
| `ALERT_TOPIC_ARN` | Existing private notification topic used only for known-exploited match alerts |

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Python log level |

## Required role permissions

The dedicated enrichment role must retain its AWS-managed basic Lambda logging policy and have narrowly scoped inline permissions:

- `dynamodb:GetItem` on only the normalized-indicator table.
- `sns:Publish` on only the existing alert topic.

Do not add `Scan`, `Query`, `PutItem`, `BatchWriteItem`, delete, list, administrative, cross-account, or broader DynamoDB permissions. Do not add broad SNS administration or delivery permissions. The handler performs one exact primary-key lookup per finding and publishes only after a known-exploited match.

## Accepted event shapes

For initial manual testing, pass a direct `cve_id`:

```json
{
  "cve_id": "CVE-YYYY-NNNN"
}
```

For a controlled EventBridge integration, the handler also accepts the CVE ID inside `detail`:

```json
{
  "detail": {
    "cve_id": "CVE-YYYY-NNNN"
  }
}
```

For an Amazon Inspector package-vulnerability event, it accepts the Inspector CVE field:

```json
{
  "detail": {
    "packageVulnerabilityDetails": {
      "vulnerabilityId": "CVE-YYYY-NNNN"
    }
  }
}
```

Use an existing public CVE identifier from the normalized table for the first match test. Do not commit the selected CVE, Lambda test event, output, table name, or logs.

## Result behavior

- A matching normalized record returns `status: known_exploited`, `kev_match: true`, `triage: prioritize`, and compact KEV context.
- A nonmatching CVE returns `status: not_known_exploited`, `kev_match: false`, and `triage: standard`.
- When `ALERT_TOPIC_ARN` is configured, a matching record sends one compact email notification through the existing topic and reports `alert_sent: true`; no-match events never alert.
- The handler never scans, writes to, or exposes raw-object locations from DynamoDB.
- Logs contain only the boolean match result, not the event payload, CVE identifier, table name, or indicator fields.

## Validation status

The function was deployed with the dedicated enrichment role and validated with an existing normalized CISA KEV record.

- The successful result returned a known-exploited match, a prioritize triage outcome, and compact indicator context.
- A controlled EventBridge event successfully invoked the function and sent the email-only known-exploited alert.
- The dedicated role uses the AWS-managed basic Lambda logging policy plus exact-table `dynamodb:GetItem` and exact-topic `sns:Publish` permissions.
- The function's CloudWatch log group uses the Standard log class with 14-day retention. Deletion protection remains off for this short-lived lab workload.
- A second EventBridge rule is prepared for active Amazon Inspector package-vulnerability findings; Amazon Inspector is intentionally not activated in this lab account.
- No public Function URL, VPC attachment, write permission, raw-object location, live test value, notification topic identifier, or account-specific event is recorded here.

