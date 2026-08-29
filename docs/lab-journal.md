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

