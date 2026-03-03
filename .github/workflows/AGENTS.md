# Agent Instructions: .github/workflows/

## Purpose

This directory contains all reusable GitHub Actions workflows for Radio Bern RaBe. Each file
is a self-contained, callable workflow invoked via `uses: radiorabe/actions/.github/workflows/<file>@<tag>`.

## File Naming

```
<verb>-<subject>.yaml
```

Allowed verbs:

| Verb | When to use |
|---|---|
| `release-` | Builds an artifact and publishes/deploys it |
| `test-` | Runs linting, unit tests, or other quality checks |
| `schedule-` | Intended to run on a time-based schedule |

## Workflow Skeleton

```yaml
name: <Human Readable Name>

on:
  workflow_call:
    inputs:
      <input-name>:
        description: '<what this input does>'
        required: <true|false>
        default: '<default value>'   # omit when required: true
        type: <string|boolean|number>
    secrets:
      <SECRET_NAME>:
        description: '<what this secret is used for>'
        required: <true|false>

jobs:
  <job-name>:
    runs-on: ubuntu-latest

    permissions:
      <permission>: <read|write>   # only what this job actually needs

    steps:
      - name: Checkout
        uses: actions/checkout@v6
      # ...
```

## Permissions Rules

- **Never** set `permissions:` at the workflow level; only on individual jobs.
- Start from zero and add only what the job strictly requires.
- Consult `docs/permissions.md` to verify the documented set matches the actual set.
- When adding or removing a permission, update `docs/permissions.md` in the same commit.

## Actions Pinning

- Pin all third-party actions to a **released version tag** (`@v3`, `@v3.10.1`, etc.).
- Do **not** pin to commit SHAs – RaBe Dependabot is configured to auto-update version tags.
- First-party actions (`actions/checkout`, `actions/setup-python`, etc.) follow the same rule.

## Security Practices

- Treat all `inputs.*` values as untrusted strings when constructing shell commands.
  Prefer passing values through environment variables rather than interpolating directly.
- Avoid `run: ${{ inputs.something }}` patterns that allow arbitrary code execution.
  The `pre-script` input in `release-container.yaml` is a deliberate exception; keep it
  minimal and document the risk.
- Use `if: github.event_name != 'pull_request'` guards before any step that pushes,
  signs, or publishes to prevent secrets exposure from fork PRs.

## Container Workflows Specifics

- `release-container.yaml` follows the build → scan (Trivy) → push → sign (cosign) → attest
  pipeline. Do not reorder these stages.
- Trivy results are stored in `trivy.json` and converted to SARIF and CycloneDX before upload.
  The intermediate files (`trivy.*`) should be listed in `.gitignore` and `.dockerignore` of
  consuming repos.

## Adding a New Workflow

1. Create `.github/workflows/<verb>-<subject>.yaml` following the skeleton above.
2. Add `docs/workflows/<category>/<name>.md` documenting it (see `docs/AGENTS.md`).
3. Register the page in `mkdocs.yml` `nav:`.
4. Add the workflow to the permissions reference table in `docs/permissions.md`.

## llms.txt

The documentation site generates an `llms.txt` index at:

- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt)

External `llms.txt` references for tools used in the workflow steps:

- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Actions, OIDC tokens, and security hardening
- [docs.docker.com/llms.txt](https://docs.docker.com/llms.txt) – Docker build, multi-platform builds, and image management
