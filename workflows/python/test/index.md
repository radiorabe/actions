# Python: Test (Poetry)

Runs [pytest](https://pytest.org/) via [Poetry](https://python-poetry.org/) against the specified Python version. The latest `3.x` release is always tested additionally as an allowed failure.

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
  test-python-poetry:
    permissions:
      contents: read # (2)
    uses: radiorabe/actions/.github/workflows/test-python-poetry.yaml@v0.0.0
    with:
      version: '3.12' # (3)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Grant only the minimum permissions this workflow requires.
1. The `version` input specifies the Python version to test against (defaults to `3.12`). The latest `3.x` is always tested additionally as an allowed failure.

Configure your `pyproject.toml` to run pytest and you are good to go.

## Inputs

| Input     | Description                    | Required | Default |
| --------- | ------------------------------ | -------- | ------- |
| `version` | Python version to test against | No       | `3.12`  |
