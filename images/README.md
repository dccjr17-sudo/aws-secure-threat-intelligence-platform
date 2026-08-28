# Screenshot Evidence — Sanitization Rules

This folder is intentionally empty until a screenshot has been manually reviewed. Screenshots are optional; text documentation is preferred when it proves the same point.

## Allowed

Only add a screenshot when it documents a specific configuration or verification outcome and all identifying information has been removed. Use descriptive neutral filenames, such as `phase-1-budget-alert-configured.png`.

## Redact before committing

Remove or obscure every occurrence of:

- AWS account, organization, canonical-user, resource, and identity IDs
- ARNs, access keys, secret values, session tokens, QR codes, recovery codes, and MFA material
- User names, email addresses, profile photos, account aliases, and browser profile names
- Console URLs, tenant/portal URLs, domain names, IP addresses, region-specific resource names, and bucket names
- Billing amounts, payment information, timestamps if identifying, support-case data, and browser tabs/bookmarks

## Required review

1. Redact a copy outside this repository.
2. Inspect the full-resolution image at 100% zoom, including the address bar and browser chrome.
3. Confirm the image supports one documentation claim and give it a non-sensitive caption in the associated phase notes.
4. Commit only the reviewed, flattened final image. Never store the unredacted original anywhere in the repository history.

If a field is difficult to redact cleanly, do not include the screenshot.

