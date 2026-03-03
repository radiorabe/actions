# MkDocs: Release

Builds and deploys [MkDocs](https://www.mkdocs.org/) documentation to GitHub Pages. Use this for repos that contain documentation built with MkDocs but do not use the [Python Poetry release workflow](https://radiorabe.github.io/actions/workflows/python/release/index.md).

## Usage

Create a `.github/workflows/release.yaml` file:

.github/workflows/release.yaml

```
name: Release

on:
  push:
    branches:
      - main
  pull_request:

permissions: {} # (1)

jobs:
  release-mkdocs:
    permissions:
      contents: write # (2)
    uses: radiorabe/actions/.github/workflows/release-mkdocs.yaml@v0.0.0
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Required to push the `gh-pages` branch for documentation deployment.

Add a `mkdocs.yml` config and `docs/` directory and you are good to go.
