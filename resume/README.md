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
