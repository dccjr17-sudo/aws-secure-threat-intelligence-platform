# Phase 1 — Cost Guardrails and Billing Visibility

## Objective

Establish practical cost visibility and early-warning controls before provisioning security-lab workloads.

## Completed controls

### Monthly cost budget

- Created a recurring, all-services monthly cost budget.
- Used unblended cost as the tracked cost metric.
- Configured actual-cost email alerts at 20%, 80%, and 100% of the budgeted amount.
- Deliberately did not attach automated actions, SNS topics, chat integrations, or budget reports.

### Federated billing visibility

- Enabled the root-only IAM access to Billing setting once for the account.
- Confirmed that the federated administrator could subsequently view cost-management data without performing routine work as root.

### Cost anomaly detection

- Retained the default AWS-managed monitor covering all AWS services.
- Used a daily email summary with a small absolute anomaly-impact threshold appropriate for a low-spend lab.
- Did not configure immediate SNS delivery or automated remediation.

### Free Tier review

- Reviewed the Free Tier dashboard after enabling federated billing visibility.
- Verified that five service offers were in use and none was at or above its usage limit at the time of review.

## Validation and operating notes

- Budget, Free Tier, and anomaly data are delayed and should not be treated as real-time billing enforcement.
- A budget sends alerts; it does not stop resources or cap charges.
- New anomaly monitors may need time and historical usage before detections become meaningful.
- No screenshots, account identifiers, private portal URLs, notification addresses, or credentials are recorded in this repository.

## Next phase

Define the secure baseline for workload services, least-privilege access, and safe provisioning practices before ingesting threat-intelligence data.
