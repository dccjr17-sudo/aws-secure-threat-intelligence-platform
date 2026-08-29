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

**In progress: Phase 2 — Architecture and Secure Data Foundation**

- Defined a low-cost serverless design using a public CISA vulnerability feed, private raw storage, normalized indicator data, narrowly scoped processing roles, and operational logging.
- The first deployment step is a private S3 raw-data bucket; no workload resources have been deployed yet.

## Documentation map

- [`docs/phase-0/`](docs/phase-0/) — sanitized record of the secure account foundation.
- [`docs/phase-1-cost-guardrails/`](docs/phase-1-cost-guardrails/) — budget, anomaly-detection, and Free Tier visibility record.
- [`docs/phase-2-architecture/`](docs/phase-2-architecture/) — approved low-cost serverless design and secure implementation sequence.
- [`docs/lab-journal.md`](docs/lab-journal.md) — concise running log for future lab sessions.
- [`images/`](images/) — intentional, redacted portfolio screenshots only.
- [`resume/`](resume/) — resume bullets and interview talking points maintained as work progresses.

## Security and privacy rules

This repository must never contain real credentials, account identifiers, private console URLs, personal identifiers, raw logs, or unredacted screenshots. Read the [image sanitization rules](images/README.md) and the [contribution guide](CONTRIBUTING.md) before adding evidence.

## Planned progression

1. Cost guardrails and billing visibility
2. Secure baseline services and least-privilege access
3. Threat-intelligence data ingestion and normalization
4. Detection, alerting, investigation, and response workflows
5. Portfolio polish, architecture diagrams, and final resume evidence

## Portfolio note

This is an educational lab, not a production service. Documentation describes what was implemented and verified in the lab environment; it does not expose live configuration values.
