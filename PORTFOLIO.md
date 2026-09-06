# AWS Secure Threat Intelligence Platform

## Project brief

A private, hands-on AWS security-engineering lab that converts public CISA Known Exploited Vulnerabilities (KEV) data into normalized CVE indicators, enriches controlled findings, and prioritizes known-exploited matches through a bounded alert workflow.

The project is deliberately designed as a low-cost, security-first lab. It demonstrates real AWS implementation and validation while keeping all account-specific values, payloads, logs, and screenshots out of the repository.

## Problem addressed

Security teams need a defensible way to recognize when a finding relates to a vulnerability that is known to be exploited in the wild. Manually comparing every finding to a public KEV catalog is slow and difficult to audit.

This lab creates a narrow, event-driven path that ingests a public KEV feed, creates compact normalized indicators, evaluates controlled CVE-bearing findings, and sends a priority signal only when an exact match is present.

## What was built

| Capability | Implementation outcome |
| --- | --- |
| Secure account foundation | Root hardening, no root access keys, federated administration, group-based access, and MFA. |
| Cost controls | Budget alerts, anomaly visibility, Free Tier review, retention limits, and intentionally limited service scope. |
| Threat-intelligence data path | Private raw-data storage, normalized CVE indicators, dependency-free Python Lambda handlers, and an automated ingest-to-normalize flow. |
| Finding triage | Exact-key enrichment of controlled findings, known-exploited prioritization, and a bounded email-only notification path. |
| Operations | CloudWatch error alarms, a saved security-operations dashboard, a documented investigation sequence, and CloudTrail Event History review. |
| Design assurance | Reference-only AWS SAM blueprint, architecture documentation, IAM policy validation, and a threat model with residual risks. |

## Security decisions demonstrated

- Separate execution roles keep ingestion, normalization, enrichment, and alert publishing responsibilities isolated.
- Sensitive raw data remains private, encrypted at rest, versioned, and governed by a limited lifecycle policy.
- Enrichment uses exact-key reads and does not scan or write indicator data.
- Event rules use specific source and detail-type patterns, and the enrichment function has no public endpoint.
- Account-specific configuration stays in AWS console settings rather than source control.
- Operational evidence is text-only unless a future screenshot can be fully redacted and independently reviewed.

## Validation evidence

The lab validated the ingestion path, automatic normalization, controlled EventBridge-to-enrichment processing, known-exploited alert delivery, CloudWatch alarm status, dashboard metrics, CloudTrail Event History review, and IAM Access Analyzer basic-policy-validation results.

Detailed, sanitized records are available in the phase documentation. The implementation does not claim production scale, security coverage, or operational ownership beyond this lab.

## What I would say in an interview

> I built a serverless AWS threat-intelligence lab focused on turning CISA KEV data into actionable CVE prioritization. I designed the system around least-privilege roles, exact-key enrichment, controlled EventBridge events, low-overhead monitoring, and cost guardrails. I also documented the architecture, operational response sequence, and residual risks rather than treating a working demo as a production-ready system.

## Deliberate limitations and next steps

- The AWS SAM template is a reference design and was not deployed into the manually built lab account.
- No dead-letter queue, automated remediation, production ticket workflow, or formal asset inventory was added.
- Amazon Inspector is prepared as a future event source but was not activated because organization governance and cost approval are required first.
- Any resilience extension should begin with a separate cost and governance review.

## Evidence map

- [Architecture and data foundation](docs/phase-2-architecture/)
- [Finding enrichment](docs/phase-3-enrichment/)
- [Event-driven triage and alerting](docs/phase-4-event-driven-triage/)
- [Operations and audit readiness](docs/phase-5-operations/)
- [Infrastructure-as-code readiness](docs/phase-6-iac-and-architecture/)
- [Security operations dashboard](docs/phase-7-security-operations/)
- [Least-privilege review and threat model](docs/phase-8-least-privilege-and-threat-model/)
- [Resume and interview notes](resume/)

