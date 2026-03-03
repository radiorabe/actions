# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD ♻️

## Usage

See below for copy-pasteable examples of the provided actions.

The examples use `@v0.0.0` as the target version of the action. You NEED to replace that with the current tag of this repository and also create the following `.github/dependabot.yaml`.

```yaml title=".github/dependabot.yaml"
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    commit-message:
      prefix: "ci: "
```

If you need multiple actions to happen then it's up to you to combine them as needed. Please add an example if you use the same combo more than once.

### Ansible Collections

We have workflows for testing Ansible collections on GitHub Actions and for releasing your Ansible collections to [Galaxy](https://galaxy.ansible.com).

#### Ansible: Release

Create the main `.github/workflows/release.yaml` file for an ansible collection repo:

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

#### Ansible: Test

Create the main `.github/workflows/test.yaml` file for an ansible collection repo:

```yaml title=".github/workflows/test.yaml"
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
2. Grant only the minimum permissions this workflow requires.
3. Optionally set `path` to run ansible-lint in a specific subdirectory (defaults to `.`, i.e. the repository root).

### Container Images

There are actions to cover the full lifecycle of a typical container image.

#### Container: Release

To build, scan, and sign a container image, create this `.github/workflows/release.yaml`:

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  pull_request:
  push:
    branches:
      - main
    tags:
      - '*'

permissions: {} # (1)

jobs:
  release-container:
    permissions:
      contents: read # (2)
      packages: write # (3)
      security-events: write # (4)
      id-token: write # (5)
    uses: radiorabe/actions/.github/workflows/release-container.yaml@v0.0.0
    with:
      image: 'ghcr.io/radiorabe/<name>' # (6)
      name: <name> # (7)
      display-name: <display-name> # (8)
      tags: <tags> # (9)
      cosign-verify: true # (10)
      cosign-certificate-oidc-issuer: [issues] # (11)
      cosign-certificate-identity-regexp: [regexp] # (12)
      cosign-base-image-only: [true] # (13)
      dockerfile: [Dockerfile] # (14)
      context: [.] # (15)
      build-args: "" # (16)
      platforms: "linux/amd64,linux/arm64" # (17)
      docker-daemon-config: | # (18)
        {
          "features": {
            "containerd-snapshotter": true
          }
        }
      push-default-branch: false # (19)
      pre-script: "" # (20)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Required to check out code.
3. Required to push the built image to the registry.
4. Required to upload Trivy scan results to the GitHub Security tab.
5. Required for keyless image signing and attestation with cosign via GitHub OIDC.
6. Replace this with the actual name of the image, usually something like the
   name of your repo with maybe a `container-image-` prefix removed.
7. Replace the name with the stem of the image
8. Put a human friendly string into display-name.
9. Tags are usually `minimal rhel9 rabe` plus additional tags for the image
   at hand.
10. Enable image scanning. This only needs to be disabled for base image that
   we don't sign ourself.
11. Defaults to GitHub as an issuer and only needs tuning in special cases.
12. The default `https://github.com/radiorabe/.*` allows signatures from all
   of our orga, add a more specific regexp if you feel the need.
13. Pass `--base-image-only` to cosign if you are copying binaries from a
   source image that isn't signed with cosign.
14. Specify the path to the Dockerfile if it isn't in the root of the repository.
15. Specify the context directory for Docker build.
16. Build ARGs for the container image build, formatted as `KEY=value` and
   separated by newlines if more than one arg is needed.
17. Pass a comma separated list of platforms to build multi-platform images.
    Used with `linux/amd64,linux/arm64` to build arm compatible images.
18. Required if building multi-platform images with `platforms` so the docker
    daemon can export the built images for further processing.
19. Push the image when the default branch (typically `main`) is pushed to the registry.
20. Run a script before interacting with the Dockerfile.

As a last step, it is recommended to add `trivy.*` to both your `.gitignore`
and `.dockerignore` files so trivy can't interfere with multi-stage builds.

#### Container: Schedule

To scan the latest container image with trivy at regular intervals, create this `.github/workflows/schedule.yaml`:

```yaml title=".github/workflows/schedule.yaml"
name: Scheduled tasks

on:
  schedule:
    - cron:  '13 12 * * *'
  workflow_dispatch:

permissions: {} # (1)

jobs:
  schedule-trivy:
    permissions:
      packages: write # (2)
      security-events: write # (3)
      id-token: write # (4)
    uses: radiorabe/actions/.github/workflows/schedule-trivy.yaml@v0.0.0
    with:
      image-ref: 'ghcr.io/radiorabe/<name>:latest' # (5)
      timeout: '5m0s' # (6)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Required to push attestations to the registry.
3. Required to upload Trivy scan results to the GitHub Security tab.
4. Required for keyless attestation signing with cosign via GitHub OIDC.
5. Replace this with the actual name of the image, usually something like the
   name of your repo with maybe a `container-image-` prefix removed.
6. Optionally set `timeout` to change the scan timeout duration (defaults to `5m0s`).

### Pre Commit

Create the main `.github/workflows/test.yaml` file for a project that supports [pre-commit](https://pre-commit.com/):

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

This runs pre-commit with black, isort and flake8 installed. If you need more tools you can install them with `pip`.

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

### Python

Our Python workflows use [Poetry](https://python-poetry.org/) for installing dependencies, [pytest](https://pytest.org/) for testing, and Poetry for publishing to [pypi](https://pypi.org/).

#### Python: Poetry Pytest

Create the main `.github/workflows/test.yaml` file for a Python poetry repo:

```yaml title=".github/workflows/test.yaml"
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
2. Grant only the minimum permissions this workflow requires.
3. The `version` input specifies the Python version to test against (defaults to `3.12`). The latest `3.x` is always tested additionally as an allowed failure.

Configure your `pyproject.toml` to run pytest and you are good to go.

#### Python: Poetry Release

Create this `.github/workflows/release.yaml`:

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
  python-poetry:
    permissions:
      contents: write # (2)
    uses: radiorabe/actions/.github/workflows/release-python-poetry.yaml@v0.0.0
    secrets:
      RABE_PYPI_TOKEN: ${{ secrets.RABE_PYPI_TOKEN }} # (3)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Required to push the `gh-pages` branch for documentation deployment.
3. The `RABE_PYPI_TOKEN` is shared across our repos and can be enabled for your
   repo by a GitHub organisation admin.

Configure your `pyproject.toml` for releasing and your `mkdocs.yml` to generate proper documentation and you are good to go.

### Mkdocs

For repos that contain documentation built with mkdocs that do not use the poetry action.

Create a `.github/workflows/release.yaml` file with the following content:

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

### Semantic Release

For repos that want to use [go-semantic-release](https://go-semantic-release.xyz):

Create this `.github/workflows/semantic-release.yaml`:

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

## Permissions

These reusable workflows enforce [least-privilege](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
by explicitly declaring the minimum `permissions` each workflow job requires. GitHub Actions enforces the
intersection of caller and callee permissions, so the effective permissions for a called workflow are
**no more** than what the calling job grants.

To implement least access in your downstream repositories:

1. **Restrict default token permissions** in your repository's Settings → Actions → General →
   Workflow permissions. Select **"Read repository contents and packages permissions"** to use
   `contents: read` and `packages: read` as the default instead of the broader write default.

2. **Set `permissions: {}`** at the top of every calling workflow to start from a baseline of no
   permissions, then grant only what each job needs at the job level. Every example in this README
   already follows this pattern.

3. **Keep job-level permissions tightly scoped.** The table below lists the minimum permissions
   each reusable workflow requires. Only grant what is listed; the reusable workflow itself will not
   request anything beyond these.

| Reusable Workflow | Required `permissions` |
|---|---|
| `release-ansible-collection.yaml` | `contents: read` |
| `release-container.yaml` | `contents: read`, `packages: write`, `security-events: write`, `id-token: write` |
| `release-mkdocs.yaml` | `contents: write` |
| `release-python-poetry.yaml` | `contents: write` |
| `schedule-trivy.yaml` | `packages: write`, `security-events: write`, `id-token: write` |
| `semantic-release.yaml` | `contents: read` |
| `test-ansible-collection.yaml` | `contents: read` |
| `test-pre-commit.yaml` | `contents: read` |
| `test-python-poetry.yaml` | `contents: read` |

For further reading see GitHub's [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) guide.

## License

These reusable workflows are free software: you can redistribute them and/or modify them under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
