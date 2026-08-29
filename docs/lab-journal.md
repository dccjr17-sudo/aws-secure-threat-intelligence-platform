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

