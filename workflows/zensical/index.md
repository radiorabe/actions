# Zensical: Release

Builds and deploys [Zensical](https://zensical.org/) documentation to GitHub Pages. [Zensical](https://zensical.org/) is a modern static site generator built by the creators of [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and is the recommended replacement for [release-mkdocs.yaml](https://radiorabe.github.io/actions/workflows/mkdocs/index.md).

Zensical is compatible with existing `mkdocs.yml` configuration files, so most projects can switch without any content or configuration changes. See the [Zensical compatibility guide](https://zensical.org/compatibility/) for details.

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
  release-zensical:
    permissions:
      contents: read # (2)
      pages: write # (3)
      id-token: write # (4)
    uses: radiorabe/actions/.github/workflows/release-zensical.yaml@v0.0.0
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Required to check out the repository.
1. Required to deploy to GitHub Pages via the Actions Pages API.
1. Required to authenticate with the GitHub Pages OIDC endpoint.

Add a `mkdocs.yml` config and `docs/` directory and you are good to go.

## Configuring GitHub Pages

This workflow deploys via the **GitHub Actions** Pages source (not the legacy `gh-pages` branch). Before the first deployment, set the Pages source for your repository:

1. Go to **Settings → Pages → Build and deployment → Source**.
1. Select **GitHub Actions**.

## Inputs

| Input          | Type      | Default | Description                                                                                                                                       |
| -------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `deploy`       | `boolean` | `true`  | Set to `false` to skip the upload and deployment steps (useful for dry-run testing).                                                              |
| `requirements` | `string`  | `""`    | Extra Python packages to install alongside Zensical (space-separated). Use this to add Zensical-compatible plugins required by your `mkdocs.yml`. |

## Installing extra plugins

If your `mkdocs.yml` uses plugins that need to be installed, pass them via the `requirements` input:

.github/workflows/release.yaml

```
jobs:
  release-zensical:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: radiorabe/actions/.github/workflows/release-zensical.yaml@v0.0.0
    with:
      requirements: "mkdocs-section-index mkdocs-llmstxt"
```
