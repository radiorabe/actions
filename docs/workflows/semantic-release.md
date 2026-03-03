# Semantic Release

Automates releases using [go-semantic-release](https://go-semantic-release.xyz). Runs on each
push to `main` and creates new tags and GitHub releases based on conventional commits.

## Usage

Create a `.github/workflows/semantic-release.yaml` file:

```yaml title=".github/workflows/semantic-release.yaml"
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
2. Grant only the minimum permissions this workflow requires. Repository write access is handled
   via the dedicated `RABE_ITREAKTION_GITHUB_TOKEN` secret rather than the default `GITHUB_TOKEN`.
3. The `RABE_ITREAKTION_GITHUB_TOKEN` is shared across our repos and can be enabled for your
   repo by a GitHub organisation admin.

## Secrets

| Secret | Description | Required |
|---|---|---|
| `RABE_ITREAKTION_GITHUB_TOKEN` | GitHub token with write access for creating releases | Yes |
