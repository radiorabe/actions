# Container Image: Schedule

Scans the latest container image with Trivy at regular intervals and attaches a security attestation to the image.

## Usage

Create a `.github/workflows/schedule.yaml` file:

.github/workflows/schedule.yaml

```
name: Scheduled tasks

on:
  schedule:
    - cron:  '13 12 * * *'
  workflow_dispatch:

permissions: {} # (1)

jobs:
  schedule-trivy:
    permissions:
      packages: write # (2)
      security-events: write # (3)
      id-token: write # (4)
    uses: radiorabe/actions/.github/workflows/schedule-trivy.yaml@v0.0.0
    with:
      image-ref: 'ghcr.io/radiorabe/<name>:latest' # (5)
      timeout: '5m0s' # (6)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Required to push attestations to the registry.
1. Required to upload Trivy scan results to the GitHub Security tab.
1. Required for keyless attestation signing with cosign via GitHub OIDC.
1. Replace this with the actual name of the image.
1. Optionally set `timeout` to change the scan timeout duration (defaults to `5m0s`).

## Inputs

| Input          | Description                                                       | Required | Default |
| -------------- | ----------------------------------------------------------------- | -------- | ------- |
| `image-ref`    | Image reference to scan (e.g. `ghcr.io/radiorabe/myimage:latest`) | **Yes**  | —       |
| `timeout`      | Scan timeout duration                                             | No       | `5m0s`  |
| `upload-sarif` | Upload Trivy scan results to the GitHub Security tab              | No       | `true`  |
| `attest`       | Attach a cosign vulnerability attestation to the scanned image    | No       | `true`  |

## Minimal caller (scan only, no upload or attestation)

When `upload-sarif: false` and `attest: false` are set, only `contents: read` is required:

.github/workflows/schedule.yaml

```
jobs:
  schedule-trivy:
    permissions:
      contents: read # (1)
    uses: radiorabe/actions/.github/workflows/schedule-trivy.yaml@v0.0.0
    with:
      image-ref: 'ghcr.io/radiorabe/<name>:latest'
      upload-sarif: false # (2)
      attest: false # (3)
```

1. Only `contents: read` is required when upload and attestation are disabled.
1. Skip uploading scan results to the GitHub Security tab.
1. Skip attaching a cosign vulnerability attestation to the image.
