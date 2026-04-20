# Ansible Collection: Test

Lints an Ansible collection with ansible-lint and ruff.

## Usage

Create the main `.github/workflows/test.yaml` file for an Ansible collection repo:

.github/workflows/test.yaml

```
name: Lint and Test

on:
  pull_request:
    branches:
      - main

permissions: {} # (1)

jobs:
  test-ansible-collection:
    permissions:
      contents: read # (2)
    uses: radiorabe/actions/.github/workflows/test-ansible-collection.yaml@v0.0.0
    with:
      path: '.' # (3)
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Grant only the minimum permissions this workflow requires.
1. Optionally set `path` to run ansible-lint in a specific subdirectory (defaults to `.`, i.e. the repository root).

## Inputs

| Input  | Description                 | Required | Default |
| ------ | --------------------------- | -------- | ------- |
| `path` | Path to run ansible-lint in | No       | `.`     |
