# GitHub Actions: Test

Runs [zizmor](https://github.com/zizmorcore/zizmor) static analysis security testing (SAST) on GitHub Actions workflow files. Results are uploaded to the repository's security tab as a SARIF report when GitHub Advanced Security is available.

## Usage

Create a `.github/workflows/test.yaml` file:

.github/workflows/test.yaml

```
name: Lint and Test

on:
  pull_request:
    branches:
      - main

permissions: {} # (1)

jobs:
  test-github-actions:
    permissions:
      contents: read # (2)
      security-events: write # (3)
    uses: radiorabe/actions/.github/workflows/test-github-actions.yaml@v0.0.0
    with:
      persona: "regular" # (4)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Grant read access to check out the repository contents.
1. Grant write access to upload SARIF results to the GitHub Advanced Security tab.
1. Select a zizmor persona.

## Inputs

| Input          | Description                                                                        | Required | Default   |
| -------------- | ---------------------------------------------------------------------------------- | -------- | --------- |
| `persona`      | Auditing persona: `regular`, `pedantic`, or `auditor`                              | No       | `regular` |
| `min-severity` | Minimum severity to report: `unknown`, `informational`, `low`, `medium`, or `high` | No       | `""`      |
