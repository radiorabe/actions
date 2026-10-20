# Java: Release (Maven)

Builds and publishes a Java package to [GitHub Packages](https://github.com/features/packages) using [Maven](https://maven.apache.org/).

## Usage

Create a `.github/workflows/release.yaml` file:

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  pull_request:
  push:
    branches: [main]
  release:
    types: [created]

permissions: {} # (1)

jobs:
  release-java-mvn:
    permissions:
      contents: read
      packages: write # (2)
    uses: radiorabe/actions/.github/workflows/release-java-mvn.yaml@v0.0.0
    with:
      path: .
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Required for publishing artifacts to GitHub Packages.

## Inputs

| Input | Description | Required | Default |
|---|---|---|---|
| `java-version` | Java version to use | No | `21` |
| `java-distribution` | Java distribution to use | No | `temurin` |
| `path` | Path to the directory containing `pom.xml` | No | `.` |
| `deploy` | Deploy to GitHub Packages when true; otherwise run `verify` only | No | `true` |

## Secrets

| Secret | Description | Required |
|---|---|---|
| `GITHUB_TOKEN` | GitHub Actions token used for package publish | Only when `deploy: true` |
