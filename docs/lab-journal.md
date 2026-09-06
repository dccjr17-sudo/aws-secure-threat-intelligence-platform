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

## 2026-09-04 — Finding-enrichment foundation validated

- Created a dedicated Lambda execution role with only CloudWatch Logs basic execution access and one inline `dynamodb:GetItem` permission scoped to the normalized indicator table.
- Deployed the source-controlled enrichment handler with a console-only table-name environment variable; no public Function URL, VPC attachment, or write permission was configured.
- Manually validated one known CISA KEV match and confirmed that the function returned a prioritize outcome with compact indicator context.
- Set the enrichment function's CloudWatch log group to the Standard log class with 14-day retention and left deletion protection off for this developing lab workload.
- Evidence added: sanitized validation record only; no selected CVE, table name, event payload, function identifier, output, logs, screenshots, or account identifier.
- Next step: design a narrowly scoped detection source and email-only alert path before connecting the enrichment function to automatic events.

## 2026-09-04 — Event-driven KEV alert path validated

- Extended the enrichment function to accept a direct CVE, a controlled EventBridge detail value, or the package-vulnerability CVE field used by Amazon Inspector finding events.
- Added one exact-topic publish permission to the existing enrichment role and configured the alert topic only as a console environment variable.
- Validated a controlled EventBridge event end to end: the event invoked enrichment, enrichment performed the exact indicator lookup, a known-exploited match was prioritized, and the existing email subscription received one alert.
- Created a distinct EventBridge rule ready to route active Amazon Inspector package-vulnerability findings to enrichment. Amazon Inspector was not activated because this organization requires an explicit delegated-administrator design that is outside the lab's current scope.
- Used free CloudTrail Event History to verify the successful EventBridge rule changes. No CloudTrail trail, data store, Inspector delegated administrator, Inspector scan, or automatic remediation was configured.
- Evidence added: sanitized source and outcome record only; no event payload, selected CVE, topic identifier, recipient, role name, account identifier, CloudTrail record, or screenshot.
- Next step: complete the incident-response runbook and portfolio-safe architecture boundary.

## 2026-09-04 — Infrastructure-as-code readiness documented

- Added a parameterized AWS SAM reference template representing the secure raw-data path, normalized indicator table, purpose-limited Lambda roles, daily schedule, controlled event triage, prepared Inspector event path, and email-only KEV alerts.
- Added a sanitized architecture diagram and documentation that distinguish the reusable reference design from the existing manually built lab environment.
- Did not package, deploy, create a change set, import resources, create duplicate services, enable Inspector, create a CloudTrail trail, or change the live account.
- Evidence added: reviewed source and text-only architecture record; no live identifiers, events, logs, screenshots, recipients, or account details.
- Next step: build a low-overhead security-operations dashboard using only existing service metrics and alarms.

## 2026-09-06 — Security operations dashboard and response runbook completed

- Created one CloudWatch dashboard using existing Lambda invocation and error metrics for ingestion, normalization, and enrichment, plus the state of the two existing pipeline error alarms.
- Reviewed a one-week view to confirm historical pipeline activity, zero recorded function errors for the displayed period, and both pipeline error alarms in the OK state.
- Recorded an alarm-investigation workflow that starts with the alarm state, narrows to the affected function, and uses existing logs and CloudTrail Event History without exporting sensitive records.
- Did not add custom metrics, new alarms, a CloudTrail trail, a data store, a scanning service, or automatic remediation. The dashboard was explicitly saved because dashboard autosave is disabled.
- Evidence added: text-only dashboard and runbook record; no screenshots, account identifiers, logs, payloads, recipients, or live resource names.
- Next step: review the complete portfolio evidence set and identify one optional advanced feature only after a cost and governance review.

## 2026-09-06 — Least-privilege assurance and threat model completed

- Reviewed the custom inline policies for the ingestion, normalization, and enrichment roles using IAM Access Analyzer basic policy validation in the console.
- The four reviewed policy documents returned zero security findings, errors, warnings, and suggestions. The review did not modify or save any policy.
- Confirmed the intended separation of duties: raw-data write, raw-data read, normalized-indicator write, exact indicator read, and alert publish remain action- and resource-scoped.
- Added a sanitized threat model and residual-risk register for the existing architecture. No access analyzer, custom policy check, automated remediation, or additional security service was created.
- Evidence added: text-only validation and design record; no policy JSON, resource identifier, account identifier, console URL, screenshot, or live event data.
- Next step: perform a final portfolio review or consider an optional resilience feature only after a separate cost review.

## 2026-09-06 — Portfolio readiness completed

- Added a concise project brief, evidence map, resume-bullet candidates, and interview talking points based only on completed lab work.
- Completed a final documentation privacy review and retained the text-only evidence approach; no screenshots, raw logs, policy JSON, account identifiers, recipients, or live configuration values were added.
- Documented the lab's limits honestly, including the absence of a deployed infrastructure template, dead-letter queue, automated remediation, production workload inventory, and active Inspector integration.
- Next step: treat the current lab as complete; evaluate any optional resilience feature through a separate cost and governance review.

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

