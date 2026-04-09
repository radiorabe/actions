# Python: Release (Poetry)

Publishes a Python package to [PyPI](https://pypi.org/) using [Poetry](https://python-poetry.org/) and deploys [MkDocs](https://www.mkdocs.org/) documentation to GitHub Pages.

## Usage

Create a `.github/workflows/release.yaml` file:

.github/workflows/release.yaml

```
name: Release

on:
  pull_request:
  push:
    branches: [main]
  release:
    types: [created]

permissions: {} # (1)

jobs:
  python-poetry:
    permissions:
      contents: write # (2)
    uses: radiorabe/actions/.github/workflows/release-python-poetry.yaml@v0.0.0
    secrets:
      RABE_PYPI_TOKEN: ${{ secrets.RABE_PYPI_TOKEN }} # (3)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Required to push the `gh-pages` branch for documentation deployment.
1. The `RABE_PYPI_TOKEN` is shared across our repos and can be enabled for your repo by a GitHub organisation admin.

Configure your `pyproject.toml` for releasing and your `mkdocs.yml` to generate proper documentation and you are good to go.

## Secrets

| Secret            | Description                   | Required                 |
| ----------------- | ----------------------------- | ------------------------ |
| `RABE_PYPI_TOKEN` | PyPI API token for publishing | Only on `release` events |
