# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD.

## Usage

### Ansible Collections

For repos that want to publish Ansible collections to [Galaxy](https://galaxy.ansible.com).

Create the main `.github/workflows/release.yaml` file for an ansible collection repo:

```yaml
# .github/workflows/ci.yaml
name: Release

on:
  release:
    types:
      - published

jobs:
  call-workflow:
    uses: radiorabe/actions/.github/workflows/release-ansible-collection.yaml@v0.1.0
    secrets:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
```

The collections we publish with this can be found on [our Galaxy page](https://galaxy.ansible.com/radiorabe).

### Semantic Release

For repos that want to use [go-semantic-release](https://go-semantic-release.xyz):

```yaml
# .github/workflows/semantic-release.yaml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  call-workflow:
    uses: radiorabe/actions/.github/workflows/semantic-release.yaml@v0.1.0
    secrets:
      RABE_ITREAKTION_GITHUB_TOKEN: ${{ secrets.RABE_ITREAKTION_GITHUB_TOKEN }}
```
## License

This template collection is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
