# Pre-Commit

Runs [pre-commit](https://pre-commit.com/) checks. By default installs black, isort, and
flake8 before running pre-commit.

## Usage

Create a `.github/workflows/test.yaml` file:

```yaml title=".github/workflows/test.yaml"
name: Lint and Test

on:
  pull_request:
    branches:
      - main

permissions: {} # (1)

jobs:
  pre-commit:
    permissions:
      contents: read # (2)
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Grant only the minimum permissions this workflow requires.

## Additional Python Packages

If you need more tools, install them with the `requirements` input:

```yaml title=".github/workflows/test.yaml"
jobs:
  pre-commit:
    permissions:
      contents: read # (1)
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
    with:
      requirements: black isort # (2)
```

1. Grant only the minimum permissions this workflow requires.
2. Space-separated list of additional Python packages to install before running pre-commit.

To skip the pip install step entirely (for example when no Python tools are referenced in your
`.pre-commit-config.yaml`), pass an explicit empty string to override the default:

```yaml title=".github/workflows/test.yaml"
jobs:
  pre-commit:
    permissions:
      contents: read
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
    with:
      requirements: ""
```

## Inputs

| Input | Description | Required | Default |
|---|---|---|---|
| `requirements` | Space-separated list of Python packages to install with pip; pass `""` to skip pip install and override the default | No | `black isort flake8` |
