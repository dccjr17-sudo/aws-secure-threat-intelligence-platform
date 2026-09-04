# AWS Secure Threat Intelligence Platform

> Private, portfolio-oriented lab repository. This repository contains deliberately sanitized technical notes and selected redacted evidence only.

## Purpose

This hands-on AWS lab builds a secure foundation for a future threat-intelligence platform. It is designed to demonstrate practical security engineering decisions, implementation evidence, and clear operational documentation without disclosing account-specific information.

## Current status

**Completed: Phase 0 — Secure AWS Account Foundation**

- Secured the AWS root user with phishing-resistant multi-factor authentication (MFA).
- Confirmed that the root user has no access keys.
- Configured an AWS IAM Identity Center organization instance in `us-west-2`, using AWS-owned encryption.
- Implemented group-based administrative access with permission sets and MFA.
- Validated federated administrative access through AWS Security Token Service (STS).

**Completed: Phase 1 — Cost Guardrails and Billing Visibility**

- Created an all-services monthly AWS Budget with email-only thresholds and no automated actions.
- Enabled billing access for federated administrative sessions through the root-only account setting.
- Verified the AWS-managed all-services Cost Anomaly Detection monitor and tuned its daily email threshold for a small lab environment.
- Reviewed AWS Free Tier usage and confirmed no active offer was near a usage limit.

**Completed: Phase 2 — Architecture and Secure Data Foundation**

- Defined a low-cost serverless design using a public CISA vulnerability feed, private raw storage, normalized indicator data, narrowly scoped processing roles, and operational logging.
- Deployed and validated the private S3 raw-data bucket with public access blocked, bucket-owner-enforced ownership, versioning, SSE-S3 encryption, portfolio tags, and a cost-control lifecycle rule limited to the future `raw/` data prefix.
- Deployed and validated an empty DynamoDB indicator table using a `cve_id` string key, on-demand capacity, AWS-owned encryption, and no secondary indexes.
- Created distinct Lambda execution roles with only CloudWatch logging plus narrowly scoped S3 and DynamoDB data permissions appropriate to their individual duties.
- Deployed and manually validated a CISA KEV ingestion Lambda that retrieves the public JSON feed and stores private, checksummed raw snapshots; its operational log group retains events for 14 days.
- Deployed and validated a source-controlled normalization Lambda that transforms approved raw CISA KEV snapshots into idempotent DynamoDB indicator records; its log group also retains events for 14 days.
- Configured an S3 object-created trigger limited to the approved raw CISA KEV prefix and JSON files, then verified the complete ingest-to-normalize path through CloudWatch Logs.
- Configured one enabled EventBridge Scheduler job to begin the daily ingestion run at 8:15 AM Pacific, with a dedicated scheduler invocation role and no flexible time window.

**Completed: Phase 3 — Finding Enrichment and Triage Foundation**

- Deployed and manually validated a source-controlled, dependency-free enrichment Lambda that accepts one CVE-bearing finding and performs an exact read of the normalized indicator table.
- The handler returns only compact KEV context, never scans or changes DynamoDB, has no public endpoint, and retains operational logs for 14 days.

**Completed: Phase 4 — Event-Driven KEV Triage and Alerting**

- Extended the enrichment handler to accept controlled EventBridge findings and Amazon Inspector-compatible package-vulnerability events.
- Added a narrowly scoped email-only alert for known-exploited matches, using an existing private notification topic configured only in the Lambda console.
- Validated the complete controlled path: EventBridge event, exact DynamoDB KEV lookup, priority decision, and email notification.
- Added a separate EventBridge rule prepared for active Amazon Inspector package-vulnerability findings; Amazon Inspector itself was not activated.

**In progress: Phase 5 — Operations and Audit Readiness**

- Verified the EventBridge rule changes through the free, regional CloudTrail Event History view.
- Documenting a sanitized alert-response runbook and service-activation boundary without creating a CloudTrail trail, data store, or additional scanning service.

## Documentation map

- [`docs/phase-0/`](docs/phase-0/) — sanitized record of the secure account foundation.
- [`docs/phase-1-cost-guardrails/`](docs/phase-1-cost-guardrails/) — budget, anomaly-detection, and Free Tier visibility record.
- [`docs/phase-2-architecture/`](docs/phase-2-architecture/) — approved low-cost serverless design and secure implementation sequence.
- [`docs/phase-3-enrichment/`](docs/phase-3-enrichment/) — validated read-only finding-enrichment foundation and guardrails.
- [`docs/phase-4-event-driven-triage/`](docs/phase-4-event-driven-triage/) — controlled EventBridge-to-KEV alert flow and deferred Inspector integration boundary.
- [`docs/phase-5-operations/`](docs/phase-5-operations/) — audit evidence, alert-response runbook, and zero-additional-service operating model.
- [`docs/lab-journal.md`](docs/lab-journal.md) — concise running log for future lab sessions.
- [`src/ingest/`](src/ingest/) — dependency-free CISA KEV ingestion handler and deployment notes.
- [`src/normalize/`](src/normalize/) — dependency-free CISA KEV normalization handler and deployment notes.
- [`src/enrich/`](src/enrich/) — dependency-free read-only CVE finding-enrichment handler and deployment notes.
- [`images/`](images/) — intentional, redacted portfolio screenshots only.
- [`resume/`](resume/) — resume bullets and interview talking points maintained as work progresses.

## Security and privacy rules

This repository must never contain real credentials, account identifiers, private console URLs, personal identifiers, raw logs, or unredacted screenshots. Read the [image sanitization rules](images/README.md) and the [contribution guide](CONTRIBUTING.md) before adding evidence.

## Planned progression

1. Cost guardrails and billing visibility
2. Secure baseline services and least-privilege access
3. Threat-intelligence data ingestion and normalization
4. Detection, alerting, investigation, and response workflows
5. Operations, audit readiness, portfolio polish, architecture diagrams, and final resume evidence

## Portfolio note

This is an educational lab, not a production service. Documentation describes what was implemented and verified in the lab environment; it does not expose live configuration values.

