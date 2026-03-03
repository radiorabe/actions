# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD ♻️

📖 **Full documentation: [radiorabe.github.io/actions](https://radiorabe.github.io/actions/)**

## Quick Examples

### Container Image Release

```yaml title=".github/workflows/release.yaml"
name: Release

on:
  pull_request:
  push:
    branches:
      - main
    tags:
      - '*'

permissions: {}

jobs:
  release-container:
    permissions:
      contents: read
      packages: write
      security-events: write
      id-token: write
    uses: radiorabe/actions/.github/workflows/release-container.yaml@v0.0.0
    with:
      image: 'ghcr.io/radiorabe/<name>'
      name: <name>
      display-name: <display-name>
      tags: <tags>
```

### Python Poetry Test

```yaml title=".github/workflows/test.yaml"
name: Lint and Test

on:
  pull_request:
    branches:
      - main

permissions: {}

jobs:
  test-python-poetry:
    permissions:
      contents: read
    uses: radiorabe/actions/.github/workflows/test-python-poetry.yaml@v0.0.0
```

### Pre-Commit

```yaml title=".github/workflows/test.yaml"
name: Lint and Test

on:
  pull_request:
    branches:
      - main

permissions: {}

jobs:
  pre-commit:
    permissions:
      contents: read
    uses: radiorabe/actions/.github/workflows/test-pre-commit.yaml@v0.0.0
```

For all available workflows and their full configuration options, see the
[documentation](https://radiorabe.github.io/actions/).

## License

These reusable workflows are free software: you can redistribute them and/or modify them under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
