# Phase 8 — Least-Privilege Assurance and Threat Model

**Status:** Completed. The lab's custom Lambda permission policies were reviewed with IAM Access Analyzer basic policy validation, and the existing architecture was documented through a sanitized threat model.

## Objective

Demonstrate that the pipeline's permissions and data flow are intentional, narrowly scoped, and understood before introducing any optional new security capability.

## Policy-validation record

The review used the IAM console's built-in IAM Access Analyzer **basic policy validation** view. Four custom inline policy documents were reviewed across the three Lambda execution roles:

| Function responsibility | Allowed capability validated | Validation result |
| --- | --- | --- |
| Ingestion | Write raw threat-intelligence objects only to the approved private raw-data location. | No security findings, errors, warnings, or suggestions. |
| Normalization | Read approved raw objects and write normalized indicator records only to the approved indicator data store. | No security findings, errors, warnings, or suggestions. |
| Enrichment | Read one exact normalized indicator record by CVE identifier. | No security findings, errors, warnings, or suggestions. |
| Enrichment alerting | Publish an alert only to the approved notification destination. | No security findings, errors, warnings, or suggestions. |

No policy JSON was altered or saved during review. The optional **Check for new access** capability was deliberately not used because it is a custom policy check rather than the no-change basic validation review.

## Assets and security objectives

| Asset | Security objective |
| --- | --- |
| Raw public-feed snapshots | Preserve confidential access controls and data integrity until normalization is complete. |
| Normalized indicator data | Preserve integrity and constrain reads to exact-key enrichment lookups. |
| Lambda execution roles and environment configuration | Preserve least privilege and keep account-specific configuration out of source control. |
| Controlled event path and alert destination | Accept only intended event shapes and keep notification delivery bounded. |
| Operational records | Support investigation without exporting logs, event payloads, or account-specific evidence. |

## Trust boundaries and controls

| Boundary | Main risk | Existing control |
| --- | --- | --- |
| Public vulnerability feed to ingestion | Feed unavailability, malformed data, or an unexpected response. | Input validation, response-size limit, JSON structure checks, checksum recording, and a private raw-data landing area. |
| Private raw storage to normalization | Unauthorized reads or writes, duplicate delivery, or unexpected object keys. | Public access block, ownership enforcement, encryption, prefix-limited trigger, prefix-limited read/write role scope, and idempotent normalization. |
| Normalized store to enrichment | Broad data access or unsafe lookup behavior. | Exact-key lookup only, read-only enrichment access, and no scan or write capability. |
| EventBridge to enrichment | Unintended events reaching the function. | Exact source and detail-type event patterns, separate rules by source, no public function endpoint, and manual controlled-event validation. |
| Enrichment to notification | Information leakage or uncontrolled message delivery. | One exact publish destination, compact triage context, console-only environment configuration, and no recipient data in source control. |
| Operator to AWS console | Accidental privilege expansion or unreviewed configuration drift. | IAM Identity Center administration, policy validation before changes, CloudTrail Event History review, and sanitized documentation. |

## Threats and mitigations

| Threat | Current mitigation | Residual risk |
| --- | --- | --- |
| Accidental public exposure of raw data | Private storage controls, ownership enforcement, and encryption at rest. | A future manual configuration change could weaken controls; periodic console review remains necessary. |
| Overly broad function permission | Separate roles, resource-scoped policies, and basic policy-validation review. | Basic validation is not a substitute for runtime authorization testing or independent review. |
| Malformed or duplicated input | Validation before processing and idempotent normalized writes. | Upstream feed semantics may change; the ingestion and normalization logs should be monitored. |
| False confidence from a KEV match | The workflow labels a match as a prioritization signal, not proof of exploitation. | A real environment still needs asset verification and approved remediation work. |
| Failed processing or notification | Existing CloudWatch metrics, error alarms, dashboard, logs, and a console-first response runbook. | The lab has no dead-letter queue or automated retry-analysis workflow. |
| Unreviewed service expansion | Inspector is prepared for future events but not activated; no analyzer or scanner was created in this phase. | Future service activation requires an explicit governance and cost decision. |

## Deliberate non-goals

- No IAM Access Analyzer external, internal, or unused-access analyzer was created.
- No custom policy check, "Check for new access" action, policy change, or new policy version was created.
- No automated remediation, ticket integration, CloudTrail trail, data store, or additional scanning service was added.
- No live identifiers, policy JSON, event payloads, logs, screenshots, recipient details, or account-specific values are kept in this repository.

## Evidence summary

The evidence is text-only: zero basic-policy-validation findings for each reviewed custom policy document, a documented separation of duties, and the threat-model decisions above. Account-specific policy and console details remain in AWS only.

