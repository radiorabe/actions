# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD ♻️

## Usage

See below for copy-pasteable examples of the provided actions.

The examples use `@main` as the target version of the action. You should replace that with the current tag of this repository and also create the following `.github/dependabot.yaml`.

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    commit-message:
      prefix: "chore(ci): "
```

If you need multiple actions to happen then it's up to you to combine them as needed. Please add an example if you use the same combo more than once.

### Ansible Collections

We have workflows for testing Ansible collectionis on GitHub Actions and for releasing your Ansible collections to [Galaxy](https://galaxy.ansible.com).

#### Ansible Collections: Release

Create the main `.github/workflows/release.yaml` file for an ansible collection repo:

```yaml
name: Release

on:
  release:
    types:
      - published

jobs:
  release-ansible-collection:
    uses: radiorabe/actions/.github/workflows/release-ansible-collection.yaml@main
    secrets:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
```

The collections we publish with this can be found on [our Galaxy page](https://galaxy.ansible.com/radiorabe).

#### Ansible Collections: Test

Create the main `.github/workflows/test.yaml` file for an ansible collection repo:

```yaml
name: Lint and Test

on:
  pull_request:
    branches:
      - main

jobs:
  test-ansible-collection:
    uses: radiorabe/actions/.github/workflows/test-ansible-collection.yaml@main
```

### Pre Commit

Create the main `.github/workflows/test.yaml` file for a project that supports [pre-commit](https://pre-commit.com/):

```yaml
name: Lint and Test

on:
  pull_request:
    branches:
      - main

jobs:
  pre-commit:
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@main
```

This runs pre-commit with black and isort installed. If you need more tools you can install them with `pip`:

```yaml
jobs:
  pre-commit:
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@main
    with:
      requirements: black isort
```

#### Python: Poetry Pytest

Create the main `.github/workflows/test.yaml` file for an ansible collection repo:

```yaml
name: Lint and Test

on:
  pull_request:
    branches:
      - main

jobs:
  test-python-poetry:
    uses: radiorabe/actions/.github/workflows/test-python-poetry.yaml@main
```

Configure your `pyproject.toml` to run pytest and you are good to go.

### Python: Poetry Release

Create this `.github/workflows/release.yaml

```yaml
name: Release

on:
  pull_request:
  push:
    branches: [main]
  release:
    types: [created]

jobs:
  python-poetry:
    uses: radiorabe/actions/.github/workflows/release-python-poetry.yaml@main
    secrets:
      RABE_PYPI_TOKEN: ${{ secrets.RABE_PYPI_TOKEN }}
```

Configure your `pyproject.toml` for releasing and your `mkdocs.yml` to generate proper documentation and you are good to go.


### Semantic Release

For repos that want to use [go-semantic-release](https://go-semantic-release.xyz):

Create this `.github/workflows/semantic-release.yaml`:

```yaml
name: Semantic Release

on:
  push:
    branches:
      - main
      - release/*

jobs:
  semantic-release:
    uses: radiorabe/actions/.github/workflows/semantic-release.yaml@main
    secrets:
      RABE_ITREAKTION_GITHUB_TOKEN: ${{ secrets.RABE_ITREAKTION_GITHUB_TOKEN }}
```

### Trivy

Create this `.github/workflows/schedule.yaml`:

```yaml
name: Scheduled tasks

on:
  schedule:
    - cron:  '13 12 * * *'
  workflow_dispatch:

jobs:
  schedule-trivy:
    uses: radiorabe/actions/.github/workflows/schedule-trivy.yaml@main
    with:
      image-ref: 'ghcr.io/radiorabe/<name>:latest'
```

## License

These reuseable workflows are free software: you can redistribute them and/or modify them under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
