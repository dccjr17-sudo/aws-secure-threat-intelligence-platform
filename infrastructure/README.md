# Infrastructure Reference Blueprint

`template.yaml` is a parameterized AWS SAM reference for a future, clean-room deployment of this lab. It represents the intended boundaries in source control without exposing live identifiers.

## Important deployment boundary

This template is **not deployed** and must not be deployed into the existing manually built lab account. Deploying it there could create duplicate resources, invoke functions, send alerts, or create storage and service charges.

Before any future deployment, start in a separate account or a clearly approved clean environment and complete all of the following:

1. Review the generated change set and all service pricing.
2. Configure an email subscription for the alert topic outside the template.
3. Confirm the daily scheduler time zone and the CISA feed endpoint behavior.
4. Validate the S3 notification configuration and each Lambda role scope.
5. Confirm whether Amazon Inspector governance is appropriate; the template prepares a rule but does not activate Inspector.
6. Run a limited manual validation before enabling the daily schedule.

## What the template represents

| Component | Intended boundary |
| --- | --- |
| Raw data bucket | Private, versioned, SSE-S3 encrypted, lifecycle-managed CISA KEV snapshots under `raw/` |
| Indicator table | On-demand, CVE-keyed normalized records with no secondary index |
| Ingest function | Writes only to the approved raw prefix |
| Normalize function | Reads only that prefix and writes normalized records only to the indicator table |
| Enrich function | Reads exactly one CVE-keyed item and publishes only known-exploited alerts to one topic |
| Function logs | Standard CloudWatch log groups with 14-day retention |
| Scheduler | Invokes only the ingestion function at the defined local schedule |
| EventBridge | Separates controlled lab events from the prepared Amazon Inspector package-finding path |

## Intentional omissions

- Live bucket, table, role, topic, account, and email values
- A public endpoint, API Gateway, VPC, cross-account access, or automatic remediation
- CloudTrail trails, data stores, Inspector activation, and organization delegation
- An SNS email subscription, to prevent personal contact data from being embedded in infrastructure source

## Validation status

The template is a source-controlled reference artifact. It is checked for structural YAML correctness only; it has not been packaged, deployed, or used to modify the active lab environment.

