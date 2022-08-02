# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD.

## Usage

### Ansible Collections

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
    uses: radiobern/actions/.github/workflows/release-ansible-collection.yaml@v0.1.0
    secrets:
      GALAXY_API_KEY: ${{ secrets.GALAXY_API_KEY }}
```

## License

This template collection is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
