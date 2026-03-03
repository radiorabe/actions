# Java Maven: Release

Publishes a Java package to [GitHub Packages](https://docs.github.com/en/packages) using
[Maven](https://maven.apache.org/).

## Usage

Add a `distributionManagement` section to your `pom.xml`:

```xml title="pom.xml"
<project ...>
  ...
  <distributionManagement>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/radiorabe/YOUR-REPO</url>
    </repository>
  </distributionManagement>
</project>
```

Create a `.github/workflows/release.yaml` file:

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
  java-maven:
    permissions:
      contents: read # (2)
      packages: write # (3)
    uses: radiorabe/actions/.github/workflows/release-java-mvn.yaml@v0.0.0
    with:
      java-version: '21' # (4)
      java-distribution: 'temurin' # (5)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Required to check out the repository.
3. Required to publish the package to GitHub Packages.
4. We use LTS versions of Java that are available on RHEL-style distros.
5. The Temurin Java distribution is suitable for deployment purposes.

## Inputs

| Input | Description | Required | Default |
|---|---|---|---|
| `java-version` | Java version to use | No | `21` |
| `java-distribution` | Java distribution to use (see [supported distributions](https://github.com/actions/setup-java?tab=readme-ov-file#supported-distributions)) | No | `temurin` |
