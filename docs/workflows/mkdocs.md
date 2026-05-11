# MkDocs: Release

!!! warning "Deprecated"
    This workflow is deprecated. Downstreams are encouraged to explore switching to the
    [Zensical release workflow](zensical.md), which is the modern replacement built by
    the creators of Material for MkDocs. Zensical is compatible with existing `mkdocs.yml`
    configuration and the switch requires minimal changes. See the [Zensical docs](zensical.md)
    for migration guidance.

Builds and deploys [MkDocs](https://www.mkdocs.org/) documentation to GitHub Pages. Use this
for repos that contain documentation built with MkDocs but do not use the
[Python Poetry release workflow](python/release.md).

## Usage

Create a `.github/workflows/release.yaml` file:

```yaml title=".github/workflows/release.yaml"
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
2. Required to push the `gh-pages` branch for documentation deployment.

Add a `mkdocs.yml` config and `docs/` directory and you are good to go.
