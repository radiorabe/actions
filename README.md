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

jobs:
  release-ansible-collection:
    uses: radiorabe/actions/.github/workflows/release-ansible-collection.yaml@v0.0.0
    secrets:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }} # (1)
```

1. The `GALAXY_API_KEY` is shared across our repos and can be enabled for your
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

jobs:
  test-ansible-collection:
    uses: radiorabe/actions/.github/workflows/test-ansible-collection.yaml@v0.0.0
```

### Container Images

There are actions to cover the full lifecycle of a typical container image.

#### Container: Release

To build, scan, and sign a container image , create this `.github/workflows/release.yaml`:

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  pull_request:
  push:
    branches:
      - main
    tags:
      - '*'

jobs:
  release-container:
    uses: radiorabe/actions/.github/workflows/release-container.yaml@v0.0.0
    with:
      image: 'ghcr.io/radiorabe/<name>' # (1)
      name: <name> # (2)
      display-name: <display-name> # (3)
      tags: <tags> # (4)
      cosign-verify: true # (5)
      cosign-certificate-oidc-issuer: [issues] # (6)
      cosign-certificate-identity-regexp: [regexp] # (7)
      cosign-base-image-only: [true] # (8)
      dockerfile: [Dockerfile] # (9)
      context: [.] # (10)
      build-args: "" # (11)
      platforms: "linux/amd64,linux/arm64" # (12)
      docker-daemon-config: | # (13)
        {
          "features": {
            "containerd-snapshotter": true
          }
        }
```

1. Replace this with the actual name of the image, usually something like the
   name of your repo with maybe a `container-image-` prefix removed.
2. Replace the name with the stem of the image
3. Put a human friendly string into display-name.
4. Tags are usually `minimal rhel9 rabe` plus additional tags for the image
   at hand.
5. Enable image scanning. This only needs to be disabled for base image that
   we don't sign ourself.
6. Defaults to GitHub as an issuer and only needs tuning in special cases.
7. The default `https://github.com/radiorabe/.*` allows signatures from all
   of our orga, add a more specific regexp if you feel the need.
8. Pass `--base-image-only` to cosign if you are copying binaries from a
   source image that isn't signed with cosign.
9. Specify the path to the Dockerfile if it isn't in the root of the repository.
10. Specify the context directory for Docker build.
11. Build ARGs for the conatimer image build, formatted as `KEY=value` and
   separated by newlines if more than one arg is needed.
12. Pass a comma separated list of platforms to build multi-platform images.
    Used with `linux/amd64,linux/arm64` to build arm compatible images.
13. Required if building multi-platform images with `platforms` so the docker
    daemon can export the built images for further processing.

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

jobs:
  schedule-trivy:
    uses: radiorabe/actions/.github/workflows/schedule-trivy.yaml@v0.0.0
    with:
      image-ref: 'ghcr.io/radiorabe/<name>:latest' # (1)
```

1. Replace this with the actual name of the image, usually something like the
   name of your repo with maybe a `container-image-` prefix removed.

### Pre Commit

Create the main `.github/workflows/test.yaml` file for a project that supports [pre-commit](https://pre-commit.com/):

```yaml title=".github/workflows/test.yaml"
name: Lint and Test

on:
  pull_request:
    branches:
      - main

jobs:
  pre-commit:
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
```

This runs pre-commit with black and isort installed. If you need more tools you can install them with `pip`.

```yaml title=".github/workflows/test.yaml"
jobs:
  pre-commit:
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
    with:
      requirements: black isort
```

### Python

Our Python workflows use [Poetry](https://python-poetry.org/) for installing dependencies, [pytest](https://pytest.org/) for testing, and Poetry for publishing to [pypi](https://pypi.org/).

#### Python: Poetry Pytest

Create the main `.github/workflows/test.yaml` file for an ansible collection repo:

```yaml title=".github/workflows/test.yaml"
name: Lint and Test

on:
  pull_request:
    branches:
      - main

jobs:
  test-python-poetry:
    uses: radiorabe/actions/.github/workflows/test-python-poetry.yaml@v0.0.0
```

Configure your `pyproject.toml` to run pytest and you are good to go.

#### Python: Poetry Release

Create this `.github/workflows/release.yaml

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  pull_request:
  push:
    branches: [main]
  release:
    types: [created]

jobs:
  python-poetry:
    uses: radiorabe/actions/.github/workflows/release-python-poetry.yaml@v0.0.0
    secrets:
      RABE_PYPI_TOKEN: ${{ secrets.RABE_PYPI_TOKEN }} # (1)
```

1. The `RABE_PYPI_TOKEN` is shared across our repos and can be enabled for your
   repo by a GitHub organisation admin.

Configure your `pyproject.toml` for releasing and your `mkdocs.yml` to generate proper documentation and you are good to go.

### Mkdocs

For repos that contain documentation built with mkdocs that do not use the poetry action.

Create a `.github/workflows/release.yaml` file with the following content:

```
name: Release

on:
  push:
    main
  pull_request:

jobs:
  release-mkdocs:
    uses: radiorabe/actions/.github/workflows/release-mkdocs.yaml@v0.0.0
```

Add a `mkdocs.yaml` config and `docs/` directory and you are good to go.

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

jobs:
  semantic-release:
    uses: radiorabe/actions/.github/workflows/semantic-release.yaml@v0.0.0
    secrets:
      RABE_ITREAKTION_GITHUB_TOKEN: ${{ secrets.RABE_ITREAKTION_GITHUB_TOKEN }} # (1)
```

1. The `RABE_ITREAKTION_GITHUB_TOKEN` is shared across our repos and can be enabled for your
   repo by a GitHub organisation admin.

## License

These reuseable workflows are free software: you can redistribute them and/or modify them under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
