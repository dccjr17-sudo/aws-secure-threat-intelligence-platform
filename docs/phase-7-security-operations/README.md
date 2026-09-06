# Phase 7 — Security Operations Dashboard and Response Runbook

**Status:** Completed. The lab has a saved, low-overhead operational view built only from existing CloudWatch service metrics and alarm states.

## Objective

Make the existing threat-intelligence workflow easier to monitor and investigate without enabling a new security service, creating custom metrics, or changing the alert path.

## Dashboard scope

The security-operations dashboard contains three widgets:

| Widget | Purpose | Source |
| --- | --- | --- |
| Pipeline invocations | Shows whether the ingestion, normalization, and enrichment functions are receiving work. | Existing Lambda `Invocations` metrics, grouped by function name. |
| Pipeline errors | Shows whether any of the three pipeline functions returned errors. | Existing Lambda `Errors` metrics, grouped by function name. |
| Pipeline alarm status | Shows the current state of the ingestion and normalization error alarms. | Existing CloudWatch alarm states. |

The Lambda count widgets use the `Sum` statistic with a five-minute period. This makes each plotted point a count of invocations or errors in that period rather than an average.

## Validation performed

A one-week dashboard view showed historical pipeline activity, no recorded function errors for the displayed period, and both existing pipeline error alarms in the OK state. This validates the dashboard wiring; it is not evidence that the lab is free of every possible failure mode.

## Alert-investigation runbook

When a pipeline error alarm changes state:

1. Open the security-operations dashboard in the workload Region and identify which pipeline error alarm is not OK.
2. Use the Pipeline errors widget to identify the affected function and time window. Confirm the corresponding invocation pattern in the Pipeline invocations widget.
3. Open only that function's CloudWatch log group and inspect the matching recent invocation. Keep account identifiers, request IDs, object keys, payloads, and raw logs in the console; do not copy them into this repository.
4. Determine whether the issue is in ingestion, normalization, enrichment, or event delivery. Review the appropriate existing configuration before changing code or permissions.
5. If a change was unexpected, use regional CloudTrail Event History to review relevant management events. Do not create a trail, data store, export, or screenshot merely for this lab.
6. Record any real remediation or escalation in the organization's approved process. This lab does not create tickets or perform automated remediation.

## Interpretation guide

| Observation | Meaning | Safe first action |
| --- | --- | --- |
| Invocation count rises and error count remains zero | The observed function activity completed without a Lambda error. | No change required; retain the dashboard as operating evidence. |
| A pipeline error alarm is in ALARM | At least one monitored function error met the configured threshold. | Start with the affected function's recent log entry and configuration. |
| Alarm state is OK but the pipeline appears quiet | The existing error condition has not been met; this is not proof that a schedule ran. | Review the expected schedule and the ingestion function's latest invocation. |
| No alert email after a controlled known-exploited match | The enrichment, EventBridge, or notification path may need investigation. | Follow the existing Phase 5 alert-response runbook before changing permissions. |
| Inspector-related activity is considered | The prepared rule alone does not activate a scanner or create findings. | Stop and perform an explicit organization-governance and cost review before activating Inspector. |

## Cost and security boundary

- The dashboard uses existing AWS service metrics and existing alarm states only.
- No custom metrics, new alarms, log exports, metric streams, Lambda Insights, CloudTrail trail, CloudTrail data store, or additional security service was enabled for this phase.
- The lab uses one custom dashboard and should remain within the account's reviewed dashboard allowance; verify current CloudWatch pricing and dashboard count before creating additional dashboards.
- No dashboard screenshot, account identifier, email recipient, event payload, log content, object key, or live resource identifier belongs in source control.

## Evidence summary

Accepted evidence is text-only: a saved dashboard with the three documented widget types, a one-week review showing historical activity and healthy alarm states, and this investigation workflow. The live AWS console remains the source of account-specific operational details.

