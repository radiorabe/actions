# Ansible Collection: Release

Builds and optionally publishes an Ansible collection to [Galaxy](https://galaxy.ansible.com).

## Usage

Create the main `.github/workflows/release.yaml` file for an Ansible collection repo:

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  release:
    types:
      - published

permissions: {} # (1)

jobs:
  release-ansible-collection:
    permissions:
      contents: read # (2)
    uses: radiorabe/actions/.github/workflows/release-ansible-collection.yaml@v0.0.0
    with:
      publish: true # (3)
    secrets:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }} # (4)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Grant only the minimum permissions this workflow requires.
3. Set `publish` to `false` to skip publishing the collection to Galaxy (defaults to `true`).
4. The `GALAXY_API_KEY` is shared across our repos and can be enabled for your
   repo by a GitHub organisation admin.

The collections we publish with this can be found on [our Galaxy page](https://galaxy.ansible.com/radiorabe).

## Inputs

| Input | Description | Required | Default |
|---|---|---|---|
| `publish` | Enable publishing collection to Galaxy | No | `true` |

## Secrets

| Secret | Description | Required |
|---|---|---|
| `GALAXY_API_KEY` | Ansible Galaxy API key | Yes |
