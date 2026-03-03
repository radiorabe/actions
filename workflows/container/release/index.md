# Container Image: Release

Builds, scans with Trivy, signs with cosign, and pushes a container image to a registry.

## Usage

Create a `.github/workflows/release.yaml` file:

.github/workflows/release.yaml

```
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
```

1. Deny all permissions at the workflow level as a secure baseline.
1. Required to check out code.
1. Required to push the built image to the registry.
1. Required to upload Trivy scan results to the GitHub Security tab.
1. Required for keyless image signing and attestation with cosign via GitHub OIDC.
1. Replace this with the actual name of the image, usually the name of your repo with maybe a `container-image-` prefix removed.
1. Replace the name with the stem of the image.
1. Put a human-friendly string into display-name.
1. Tags are usually `minimal rhel9 rabe` plus additional tags for the image at hand.

As a last step, it is recommended to add `trivy.*` to both your `.gitignore` and `.dockerignore` files so Trivy can't interfere with multi-stage builds.

## Inputs

| Input                                | Description                                                        | Required | Default                                       |
| ------------------------------------ | ------------------------------------------------------------------ | -------- | --------------------------------------------- |
| `image`                              | Image to build and push (e.g. `ghcr.io/radiorabe/myimage`)         | **Yes**  | —                                             |
| `name`                               | Value for the `name` label                                         | **Yes**  | —                                             |
| `display-name`                       | Value for the `io.k8s.display-name` label                          | **Yes**  | —                                             |
| `tags`                               | Value for the `io.openshift.tags` label                            | **Yes**  | —                                             |
| `cosign-verify`                      | Enable cosign verification of the base image                       | No       | `true`                                        |
| `cosign-certificate-oidc-issuer`     | Issuer used for keyless signature verification                     | No       | `https://token.actions.githubusercontent.com` |
| `cosign-certificate-identity-regexp` | Regex to verify the subject against                                | No       | `https://github.com/radiorabe/.*`             |
| `cosign-base-image-only`             | Pass `--base-image-only` to cosign dockerfile verify               | No       | `false`                                       |
| `dockerfile`                         | Path to the Dockerfile                                             | No       | `Dockerfile`                                  |
| `context`                            | Context directory for Docker build                                 | No       | `.`                                           |
| `build-args`                         | Build ARGs (`KEY=value` separated by newlines)                     | No       | `""`                                          |
| `platforms`                          | Comma-separated list of platforms (e.g. `linux/amd64,linux/arm64`) | No       | `linux/amd64`                                 |
| `docker-daemon-config`               | Docker daemon config JSON (required for multi-platform builds)     | No       | —                                             |
| `push-default-branch`                | Push the image when the default branch is pushed                   | No       | `false`                                       |
| `pre-script`                         | Script to run before interacting with the Dockerfile               | No       | `""`                                          |

## Multi-Platform Builds

To build images for multiple CPU architectures, set `platforms` and provide a `docker-daemon-config`:

.github/workflows/release.yaml

```
    uses: radiorabe/actions/.github/workflows/release-container.yaml@v0.0.0
    with:
      image: 'ghcr.io/radiorabe/<name>'
      name: <name>
      display-name: <display-name>
      tags: <tags>
      platforms: "linux/amd64,linux/arm64"
      docker-daemon-config: |
        {
          "features": {
            "containerd-snapshotter": true
          }
        }
```
