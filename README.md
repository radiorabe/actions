# RaBe GitHub Actions

These are the [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that RaBe uses for CI/CD ♻️

## Usage

See below for copy-pasteable examples of the provided actions.

If you need multiple actions to happen then it's up to you to combine them as needed. Please add an example if you use the same combo more than once.

🔥 Until dependabot supports updating `jobs.call-workflow.uses`, we recommend using `@main` in all the examples below. This has been requested in [dependabot/dependabot-core@4327](https://github.com/dependabot/dependabot-core/issues/4327). You know the drill, go 👍 the issue to help us out. We'll switch back to using tagged releases once that is resolved.

### Ansible Collections

For repos that want to publish Ansible collections to [Galaxy](https://galaxy.ansible.com).

Create the main `.github/workflows/release.yaml` file for an ansible collection repo:

```yaml
# .github/workflows/release.yaml
name: Release

on:
  release:
    types:
      - published

jobs:
  call-workflow:
    uses: radiorabe/actions/.github/workflows/release-ansible-collection.yaml@main
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
    uses: radiorabe/actions/.github/workflows/semantic-release.yaml@main
    secrets:
      RABE_ITREAKTION_GITHUB_TOKEN: ${{ secrets.RABE_ITREAKTION_GITHUB_TOKEN }}
```
## License

These reuseable workflows are free software: you can redistribute them and/or modify them under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, version 3 of the License.

## Copyright

Copyright (c) 2022 [Radio Bern RaBe](http://www.rabe.ch)
