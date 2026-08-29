# CISA KEV Ingestion Lambda

This dependency-free Python Lambda handler retrieves the public CISA Known Exploited Vulnerabilities (KEV) JSON feed and saves a raw, checksummed copy in the private S3 archive.

## Deployment configuration

| Setting | Value |
| --- | --- |
| Runtime | Python 3.14 |
| Handler | `lambda_function.lambda_handler` |
| Execution role | The dedicated ingestion role created for this lab |
| Memory | 256 MB |
| Timeout | 30 seconds |
| VPC | None; the function needs outbound HTTPS access to the public feed |

Set this environment variable in the Lambda console only; do not commit its value:

| Variable | Purpose |
| --- | --- |
| `RAW_BUCKET` | Private raw-data bucket name |

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `SOURCE_URL` | Official CISA KEV JSON endpoint | Allows an approved source-URL override |
| `LOG_LEVEL` | `INFO` | Python log level |

## Security behavior

- Makes a single outbound HTTPS request to the public CISA source.
- Limits a source response to 10 MiB and validates that it is JSON with the expected `vulnerabilities` array.
- Stores only under the S3 `raw/` prefix and requests SSE-S3 encryption.
- Does not log the raw payload, bucket name, credentials, or the full source response.
- Returns safe operational metadata: object key, catalog version, checksum, and byte count.

## Manual validation event

Use an empty JSON event such as `{}` for the initial manual invocation. A successful run creates one object below the `raw/cisa-kev/` prefix. Do not add the resulting object or raw feed to this repository.

## Validation status

The handler was deployed and successfully manually invoked in the lab. Execution-specific output, raw object contents, logs, checksums, and identifiers are intentionally not retained in this repository.

