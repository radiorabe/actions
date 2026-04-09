# Semantic Release

Automates releases using [go-semantic-release](https://go-semantic-release.xyz). Runs on each push to `main` and creates new tags and GitHub releases based on conventional commits.

## Usage

Create a `.github/workflows/semantic-release.yaml` file:

.github/workflows/semantic-release.yaml

```
name: Semantic Release

on:
  push:
    branches:
      - main
      - release/*

permissions: {} # (1)

jobs:
  semantic-release:
    permissions:
      contents: read # (2)
    uses: radiorabe/actions/.github/workflows/semantic-release.yaml@v0.0.0
    secrets:
      RABE_ITREAKTION_GITHUB_TOKEN: ${{ secrets.RABE_ITREAKTION_GITHUB_TOKEN }} # (3)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Grant only the minimum permissions this workflow requires. Repository write access is handled via the dedicated `RABE_ITREAKTION_GITHUB_TOKEN` secret rather than the default `GITHUB_TOKEN`.
1. The `RABE_ITREAKTION_GITHUB_TOKEN` is shared across our repos and can be enabled for your repo by a GitHub organisation admin.

## Inputs

| Input | Description                                                             | Required | Default |
| ----- | ----------------------------------------------------------------------- | -------- | ------- |
| `dry` | Run in dry-run mode (determine next version without creating a release) | No       | `false` |

## Secrets

| Secret                         | Description                                          | Required               |
| ------------------------------ | ---------------------------------------------------- | ---------------------- |
| `RABE_ITREAKTION_GITHUB_TOKEN` | GitHub token with write access for creating releases | Only when `dry: false` |

Note

When `RABE_ITREAKTION_GITHUB_TOKEN` is not supplied, the workflow falls back to the built-in `GITHUB_TOKEN`. In dry-run mode this is sufficient. For actual releases, the dedicated PAT is required because it has the write permissions needed to create tags and GitHub Releases.
