# Lab Journal

Use this file for short, outcome-focused updates after each lab session. Do not paste raw command output, console URLs, screenshots, or identifiers.

## 2026-08-28 — Portfolio tracking initialized

- Created the private repository structure and documentation guardrails.
- Recorded the completed secure AWS account foundation as Phase 0.
- Defined cost guardrails as the next lab milestone.

## 2026-08-29 — Phase 1 cost guardrails completed

- Created a monthly all-services cost budget with actual-cost email thresholds at 20%, 80%, and 100% of the budgeted amount.
- Used email notifications only; no budget actions, SNS topics, or chat integrations were configured.
- Enabled the root-only IAM access to Billing setting so the federated administrator could access cost data without using root for routine work.
- Retained the AWS-managed all-services anomaly monitor and tuned its daily email alert to a small absolute anomaly impact.
- Reviewed Free Tier usage: five service offers were in use, with none at or above a usage limit.
- Evidence added: documentation only; no screenshots or account-specific values.
- Next step: define the secure baseline for workload provisioning and least-privilege access.

## 2026-08-29 — Phase 2 private raw-data archive established

- Created and validated a private general-purpose S3 raw-data archive in the workload region before ingesting any data.
- Enabled Block Public Access, bucket-owner-enforced object ownership, versioning, and default SSE-S3 encryption; no bucket policy was required at this stage.
- Added portfolio tags for project, environment, and public threat-intelligence data classification.
- Added a lifecycle rule limited to the future `raw/` prefix: current objects expire after 30 days, while noncurrent versions and incomplete multipart uploads are cleaned up after 7 days.
- Evidence added: sanitized configuration record only; no bucket name, identifier, screenshots, or feed data.
- Next step: create the DynamoDB indicator table with a minimal access model.

## 2026-08-29 — Phase 2 normalized-indicator table established

- Created and validated an empty DynamoDB Standard table for normalized threat-intelligence indicators.
- Defined a single `cve_id` string partition key and intentionally omitted a sort key for the initial CISA KEV feed model.
- Retained on-demand read and write capacity and AWS-owned encryption; no secondary indexes, replica Regions, or resource-based policy were configured.
- Deferred deletion protection while the table is empty and the lab build is still changing.
- Evidence added: sanitized configuration record only; no table name, identifier, screenshots, or feed data.
- Next step: create separate least-privilege Lambda execution roles for ingestion and normalization.

## 2026-08-29 — Phase 2 least-privilege execution roles established

- Created separate Lambda-trusted execution roles for ingestion and normalization, each with CloudWatch Logs basic execution access only.
- Limited the ingestion role to writing objects under the private raw-data prefix.
- Limited the normalization role to reading that prefix and writing normalized records to the indicator table.
- Did not attach administrative, broader S3 or DynamoDB, cross-account, list, scan, or delete permissions.
- Evidence added: sanitized policy-scope record only; no role names, ARNs, bucket names, table ARNs, screenshots, or feed data.
- Next step: deploy and manually test the ingestion Lambda function.

## 2026-08-29 — Ingestion handler prepared for deployment

- Added a dependency-free Python handler that retrieves the public CISA KEV feed, enforces a response-size limit, validates JSON structure, calculates a checksum, and writes only to the raw-data prefix.
- Kept the bucket name and all live configuration out of source control; the handler requires a console-only environment variable at deployment time.
- Performed a local Python syntax check before deployment.
- Next step: create the Lambda function, configure the private bucket environment variable, and perform one manual test invocation.

## 2026-08-29 — CISA KEV ingestion Lambda manually validated

- Deployed the source-controlled, dependency-free ingestion handler using the dedicated ingestion execution role.
- Configured the private raw bucket through a console-only environment variable; no live value was added to source control.
- Manually invoked the function and verified that it retrieved the public CISA KEV JSON feed and stored one checksummed raw snapshot under the protected raw-data prefix.
- Corrected an initial nonmatching bucket environment value without broadening the function role or changing its code.
- Evidence added: sanitized success outcome only; no payload, object key, checksum, request identifier, logs, screenshots, bucket name, or account identifier.
- Next step: create and manually validate the normalization Lambda function.

## 2026-09-03 — Ingestion log retention configured

- Set the ingestion function's CloudWatch log group to the Standard log class with 14-day retention.
- Left log-group deletion protection off while this is a short-lived, developing lab workload.
- Evidence added: sanitized retention configuration only; no log-group name, account identifier, request identifier, payload, or logs.
- Next step: create and manually validate the normalization Lambda function.

## 2026-09-03 — Normalization handler prepared for deployment

- Updated the dedicated normalization role to permit batch writes only to the already restricted indicator table; the existing raw-prefix S3 read scope was unchanged.
- Added a dependency-free normalization handler that validates an S3-triggered CISA KEV raw snapshot and writes compact, idempotent indicator records keyed by CVE identifier.
- Kept live bucket and table values out of source control; the handler requires only a console-configured table-name environment variable.
- Performed a local syntax check before deployment.
- Evidence added: source and sanitized deployment notes only; no bucket name, table name, identifier, event, raw data, logs, or screenshots.
- Next step: deploy and manually validate the normalization Lambda function.

## 2026-09-03 — Normalization Lambda and automated data path validated

- Deployed the source-controlled normalization handler using the dedicated normalization execution role and configured its indicator-table setting only in the Lambda console.
- Manually validated the handler with an Amazon S3 put event referencing one protected raw snapshot; it wrote normalized, CVE-keyed records to the existing table.
- Set the normalization function's CloudWatch log group to the Standard log class with 14-day retention and left deletion protection off for this developing lab workload.
- Added an S3 object-created trigger limited to the private CISA KEV raw prefix and JSON files. A fresh manual ingestion run then invoked normalization automatically and completed successfully, confirming the full event path.
- Added one enabled EventBridge Scheduler job that invokes ingestion every day at 8:15 AM Pacific. It uses a dedicated scheduler invocation role and no flexible time window.
- Evidence added: sanitized outcome record only; no live resource names, account identifiers, event payloads, raw data, record counts, logs, screenshots, or scheduler identifiers.
- Next step: add operational metrics, alerting, and a documented cleanup procedure.

## 2026-09-03 — Finding-enrichment handler prepared for deployment

- Added a dependency-free Lambda handler that accepts one CVE-bearing finding and looks up only that exact `cve_id` in the normalized indicator table.
- The handler returns compact CISA KEV context for a match and a clear no-match result otherwise; it neither scans nor writes to DynamoDB.
- Kept the table name as a console-only environment variable and prepared the dedicated role scope as CloudWatch logging plus `dynamodb:GetItem` on only the indicator table.
- Performed a local syntax check and mocked match/no-match behavior checks without connecting to a live AWS resource.
- Evidence added: source and sanitized deployment notes only; no live CVE value, table name, event, output, logs, or identifiers.
- Next step: create the dedicated enrichment role, deploy the function, and perform one manual exact-key validation.

## Future entry template

```markdown
## YYYY-MM-DD — Short session title

- Goal:
- Actions completed:
- Validation performed:
- Security / cost consideration:
- Evidence added (sanitized only):
- Next step:
```

