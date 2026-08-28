# Phase 0 — Secure AWS Account Foundation

**Status:** completed  
**Evidence level:** configuration validated in the AWS console and through federated AWS STS access.  
**Scope:** administrative access foundation only; no application workloads are included in this phase.

## Objective

Establish a secure administrative baseline before building services in the AWS account. The intended outcome was to minimize root-user use, centralize workforce access, enforce MFA, and validate that administrators operate through federated identities instead of long-lived credentials.

## Implemented controls

| Control area | Implemented outcome |
| --- | --- |
| Root-account protection | Phishing-resistant MFA configured; no root access keys retained. |
| Centralized access | An IAM Identity Center organization instance was configured in `us-west-2`. |
| Encryption | AWS-owned encryption selected for the IAM Identity Center configuration. |
| Authorization model | Group-based administrative access established through permission sets. |
| MFA | MFA required for administrative access. |
| Session validation | Federated administrative access verified through AWS Security Token Service (STS). |

## Security rationale

- Root credentials are reserved for exceptional account-level tasks and are protected with strong MFA.
- Eliminating root access keys reduces the risk of long-lived, difficult-to-audit credentials.
- IAM Identity Center provides a centralized identity plane for access assignments and supports a group-based authorization model.
- Permission sets provide repeatable administrative entitlements without assigning permissions independently to each user.
- STS validation confirms the administrator uses short-lived federated credentials rather than root or static IAM-user credentials.

## Verification record

The following checks were performed during the lab. Specific account, identity, organization, and session identifiers are intentionally omitted.

- Root-user MFA protection was confirmed.
- Root access-key inventory was confirmed empty.
- IAM Identity Center instance region and encryption selection were confirmed.
- An administrative group and permission set assignment were confirmed.
- A federated administrative session was tested and returned AWS STS identity information.

## Deliberately omitted details

The repository excludes account numbers, organization identifiers, names/emails of identities, permission-set names when they could identify the environment, ARNs, console URLs, session data, and all screenshots from the initial setup.

## Next phase

Before deploying workloads, configure cost guardrails: AWS Budgets, billing alerts, cost anomaly detection, and cost / Free Tier visibility. Record only sanitized confirmation of each control.

