# Resume and Interview Notes

Keep these notes factual, specific, and tied to verified lab work. Do not claim production scale, monitoring coverage, or operational ownership that the lab does not demonstrate.

## Current accomplishment record

### Phase 0 — Secure AWS Account Foundation

**Evidence-backed summary**

Secured an AWS lab account by enabling phishing-resistant MFA for the root user, removing root access keys, and establishing federated, group-based administrative access through IAM Identity Center and permission sets. Validated short-lived administrative access through AWS STS.

**Resume-bullet candidates**

- Secured an AWS lab account by enabling phishing-resistant root MFA and eliminating root access keys to reduce long-lived credential exposure.
- Implemented group-based, MFA-protected administrative access with AWS IAM Identity Center and permission sets; validated federated sessions using AWS STS.
- Documented a secure cloud foundation with a privacy-safe evidence process for portfolio review and ongoing security engineering work.

**Interview talking points**

- Why root access must be exceptional and why root access keys are especially risky.
- Why federated, short-lived sessions are preferable to standing administrative credentials.
- How group-based access and permission sets make authorization more repeatable and auditable.
- How the repository avoids oversharing sensitive cloud environment details while preserving useful evidence.

### Phase 1 — Cost Guardrails and Billing Visibility

**Evidence-backed summary**

Implemented practical cost controls for an AWS security lab: a monthly all-services budget with tiered actual-cost email alerts, AWS-managed service-level anomaly detection with a low-impact daily alert threshold, and Free Tier usage review. Enabled federated billing visibility through the root-only account setting while keeping root use exceptional.

**Resume-bullet candidates**

- Implemented AWS cost guardrails using a monthly all-services budget with tiered email thresholds, avoiding automated remediation actions in a learning environment.
- Configured AWS Cost Anomaly Detection for all services and tuned daily alerts to surface small unexpected spend; verified Free Tier usage remained within limits.
- Delegated billing visibility to federated administrative access through the root-only IAM access setting, preserving root credentials for exceptional account tasks.

**Interview talking points**

- Why a budget is an alerting control rather than a hard spending cap.
- Why a small lab needs lower anomaly thresholds than a production environment.
- Why enabling billing access for federated roles improves routine operations while root access remains exceptional.
- Why all notifications were email-only and no automated budget action was attached during early lab work.

## Update template

For each phase, add:

- The verified outcome and the tools/services used
- One or two results-oriented resume bullets
- The security decision and its rationale
- A limitation or follow-up to discuss honestly in interviews

## Project-level portfolio package

### Evidence-backed summary

Built and documented a private AWS security-engineering lab that ingests public CISA Known Exploited Vulnerabilities (KEV) data, normalizes indicators, enriches controlled security findings through exact-key lookups, and prioritizes known-exploited matches through an event-driven alert path. The lab pairs least-privilege controls with operational dashboards, alert response documentation, infrastructure-as-code readiness, and a sanitized threat model.

### Selected resume-bullet candidates

- Designed and validated a serverless AWS threat-intelligence pipeline that ingests public CISA KEV data, normalizes CVE indicators, and enriches controlled findings through exact-key lookups in DynamoDB.
- Implemented event-driven KEV prioritization with Amazon EventBridge, AWS Lambda, and a bounded email-only notification path; validated the controlled finding-to-alert workflow end to end.
- Applied least privilege through separate Lambda execution roles with action- and resource-scoped access, then reviewed four custom policies with IAM Access Analyzer basic validation and recorded zero findings.
- Built low-overhead security operations visibility with CloudWatch function metrics, error alarms, a saved dashboard, and a console-first alert investigation runbook.
- Produced a parameterized, reference-only AWS SAM blueprint and threat model that document trust boundaries, residual risks, and cost-aware decisions without exposing live cloud configuration.

### Skills demonstrated

- AWS IAM Identity Center, IAM role design, policy validation, and short-lived federated administration
- Amazon S3, DynamoDB, AWS Lambda, Amazon EventBridge, EventBridge Scheduler, Amazon SNS, and Amazon CloudWatch
- Python serverless development, event-driven architecture, exact-key data access, and safe notification design
- CloudTrail Event History review, cost guardrails, security documentation, threat modeling, and privacy-safe evidence handling

### Interview talking points

**How would you summarize the project?**

Explain the flow from public KEV feed to private raw storage, normalized CVE indicators, controlled enrichment, and a priority alert. Emphasize that the project is a lab, while the design choices mirror security-engineering concerns: least privilege, idempotency, observability, and privacy-safe evidence.

**How did you implement least privilege?**

Describe the separation of ingestion, normalization, enrichment, and alert publishing into distinct roles. Explain that permissions were limited by action and target resource, enrichment performs an exact-key read rather than a scan, and the reviewed custom policies produced no IAM Access Analyzer basic-validation findings.

**How would you investigate an alert?**

Start with the CloudWatch alarm state and dashboard, identify the affected function and time window, review only the matching console log entry, and use CloudTrail Event History if a configuration change is suspected. Avoid exporting or committing sensitive records.

**Why was Inspector not activated?**

The account required an explicit organization-level delegated-administrator decision. The lab prepared an event route but did not enable a scanner without a clear governance and cost decision. This demonstrates deliberate scope control rather than treating a trial as inherently free.

**What would you improve for production?**

Add a dead-letter and retry-analysis design, a formal asset inventory and ownership model, peer-reviewed and deployed infrastructure-as-code, controlled integration testing, and an approved incident/ticket workflow. Keep these as future improvements, not completed claims.

