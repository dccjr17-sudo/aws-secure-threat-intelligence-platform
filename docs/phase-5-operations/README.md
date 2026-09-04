# Phase 5 — Operations and Audit Readiness

**Status:** In progress. The lab has a validated alert path and a no-additional-service operating model.

## Objective

Make the existing threat-intelligence workflow supportable without adding a paid logging, scanning, archival, or response service.

## Audit method

Use the regional CloudTrail **Event history** view to investigate recent AWS management activity.

For EventBridge rule changes:

1. Open CloudTrail Event history in the workload Region.
2. Filter by event name `PutRule`.
3. Confirm the event source is EventBridge, the event is a write operation, and the record has no error code.
4. Review only the console detail needed to confirm the change; do not export, screenshot, or commit the record.

The lab validated this procedure for both EventBridge rules created in Phase 4. CloudTrail Event History is a built-in 90-day regional view; no CloudTrail trail or data store was created for this lab.

## KEV alert response runbook

When the email-only KEV alert arrives:

1. Treat it as a prioritization signal, not proof that a resource is exploitable.
2. Confirm the message identifies a known-exploited CVE and a `prioritize` triage outcome.
3. Open the enrichment Lambda's CloudWatch log group and locate the corresponding recent invocation. Confirm only the boolean match and alert status; do not paste log content into this repository.
4. Review the compact CISA KEV remediation context in the email. Identify whether the relevant software exists in a real environment before taking remediation action.
5. Record any follow-up outside this repository using the organization's approved ticketing or incident process. This lab intentionally does not create tickets or make changes automatically.
6. If an alert was unexpected, verify the EventBridge rule and Lambda environment variables in the console, then use CloudTrail Event History to review the associated management changes.

## Failure handling

| Situation | Safe first action |
| --- | --- |
| No email after a controlled KEV event | Check the enrichment invocation result and Lambda logs, then verify the alert-topic environment variable and the exact-topic publish permission. |
| EventBridge rule does not invoke Lambda | Verify the rule is enabled, its event pattern is exact, and its target is the enrichment Lambda. |
| Lambda returns no match | Treat the CVE as not present in the normalized KEV table; do not broaden DynamoDB access or alert on the event. |
| Alert appears more than once | Treat delivery as potentially duplicated and investigate the matching event and rule before changing automation. |
| Inspector activation is considered later | Perform an organization-governance and cost review first; the existing prepared rule does not require Inspector to be enabled. |

## Guardrails retained

- No public endpoint or automated remediation
- No CloudTrail trail, data store, CloudTrail Lake query, archive, or screenshot evidence
- No Inspector delegated administrator, scan type, free-trial activation, or new paid service
- No raw event payloads, account identifiers, recipient data, topic identifiers, or live test values in source control
- Existing cost alerts remain the safety net for the lab account

## Evidence summary

The accepted evidence is text-only: successful creation of the two narrowly scoped EventBridge rules, successful controlled end-to-end notification, and successful review of the related EventBridge management records in CloudTrail Event History. Account-specific records remain in the AWS console only.

