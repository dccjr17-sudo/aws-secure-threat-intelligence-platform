# Safe Documentation Guide

## Before adding anything

Treat this as a portfolio repository, even while it is private. Add only material that would be safe to share publicly after review.

Never commit:

- Access keys, secret keys, session tokens, passwords, recovery codes, or MFA/QR material
- AWS account IDs, canonical user IDs, organization IDs, user emails, names, usernames, or private console URLs
- ARNs, resource IDs, IP addresses, DNS names, bucket names, or internal hostnames from the lab account
- Raw AWS CLI output, CloudTrail events, configuration exports, audit reports, logs, or browser screenshots
- Billing data, payment details, support cases, or screenshots containing personal/account information

## Evidence workflow

1. Capture evidence only when it supports a specific claim.
2. Create a copy outside the repository and redact it there.
3. Verify every visible field, including browser tabs, URLs, breadcrumbs, account menus, timestamps, and metadata.
4. Add a short caption that says what was verified without revealing identifiers.
5. Commit only the redacted final artifact.

When uncertain, do not add the item. Use a text-only implementation note instead.
