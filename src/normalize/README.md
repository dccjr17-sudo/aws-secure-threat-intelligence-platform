# CISA KEV Normalization Lambda

This dependency-free Python Lambda handler receives an S3 notification for a private CISA KEV raw snapshot, validates the catalog, and writes compact normalized indicator records to DynamoDB.

## Deployment configuration

| Setting | Value |
| --- | --- |
| Runtime | Python 3.14 |
| Handler | `lambda_function.lambda_handler` |
| Execution role | The dedicated normalization role created for this lab |
| Memory | 256 MB |
| Timeout | 30 seconds |
| VPC | None; the function only accesses AWS services through its execution role |

Set this environment variable in the Lambda console only; do not commit its value:

| Variable | Purpose |
| --- | --- |
| `INDICATOR_TABLE` | DynamoDB table name for normalized indicator records |

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Python log level |

## Required role permissions

The dedicated normalization role must retain its AWS-managed basic Lambda logging policy and have an inline policy limited to:

- `s3:GetObject` on the private `raw/*` object prefix.
- `dynamodb:PutItem` and `dynamodb:BatchWriteItem` on only the indicator table.

Do not add table scan, delete, list, administrative, cross-account, or broader S3 permissions.

## Security and data behavior

- Accepts only Amazon S3 notification events for objects below `raw/cisa-kev/`.
- Retrieves raw input only through the role's S3 permission and validates the expected CISA KEV JSON structure before any writes.
- Selects compact query-oriented fields, including the CVE identifier, source metadata, vendor/product context, dates, remediation guidance, and applicable CWEs.
- Keeps a reference to the originating raw object but does not copy the complete raw feed or its free-form notes into DynamoDB.
- Uses batched, idempotent writes keyed by `cve_id`; reprocessing the same object updates the existing indicator instead of creating duplicates.
- Logs only operational counts, never raw content, bucket names, table names, credentials, or event payloads.

## Manual validation event

After deploying the function, create a Lambda test event from the **Amazon S3 put** template and replace only its bucket name and object key with one existing private CISA KEV raw object. Keep the resulting event, object key, logs, and output out of source control.

## Validation status

The function was deployed with the dedicated role and validated in two stages:

1. A manually supplied Amazon S3 put event for one protected raw CISA KEV snapshot completed successfully and wrote normalized records to the existing DynamoDB table.
2. An S3 object-created trigger, limited to `raw/cisa-kev/` and `.json`, was added. A new snapshot from the ingestion function then invoked normalization automatically and completed without an error entry in CloudWatch Logs.

The function's CloudWatch log group uses the Standard log class with 14-day retention. The exact object location, record count, log output, table name, and other live values are intentionally not recorded here.

