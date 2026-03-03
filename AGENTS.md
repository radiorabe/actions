# Agent Instructions: radiorabe/actions

## Repository Purpose

This repository contains [reusable GitHub Actions workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that Radio Bern RaBe uses for CI/CD across all its projects. Workflows cover container image
releases, Python/Poetry testing and publishing, Ansible collection releases, MkDocs
documentation deployment, pre-commit checks, Trivy security scanning, and semantic versioning.

The full documentation is published at [radiorabe.github.io/actions](https://radiorabe.github.io/actions/).

## Repository Structure

```
.github/workflows/   # Reusable workflow definitions (the actual product)
docs/                # MkDocs source for the published documentation site
  workflows/         # One .md file per reusable workflow
  css/               # Custom MkDocs theme styles
  overrides/         # MkDocs theme overrides
mkdocs.yml           # MkDocs configuration
catalog-info.yaml    # Backstage component descriptor
```

## Conventions

### Workflow Files (`.github/workflows/`)

- **Naming**: `<verb>-<subject>.yaml` – e.g. `release-container.yaml`, `test-python-poetry.yaml`.
- **Trigger**: All workflows use `on: workflow_call` so they are reusable by caller workflows.
- **Permissions**: Declare `permissions:` on **every job**, not at the workflow level.
  Use the minimum set required. See `docs/permissions.md` for the reference table.
- **Actions pinning**: Pin third-party actions to a released version tag (e.g. `@v3`),
  not to a commit SHA.
- **Security baseline**: Every caller example must set `permissions: {}` at the top level,
  then grant per-job permissions explicitly.

### Documentation (`docs/`)

- Written in Markdown and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
- Each reusable workflow has a corresponding `docs/workflows/<category>/<name>.md` file.
- Use [MkDocs code annotations](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-annotations)
  (`# (N)` inside code blocks with numbered explanations below) to explain individual YAML keys.
- Usage examples must always include `permissions: {}` at the workflow level and explicit
  per-job permissions matching the reference table in `docs/permissions.md`.
- Update `mkdocs.yml` `nav:` whenever a new documentation page is added.

### Conventional Commits

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification used by go-semantic-release:

- `feat:` – new workflow or new input
- `fix:` – bug fix in a workflow
- `docs:` – documentation-only changes
- `ci:` – changes to the CI pipeline of this repository itself
- `chore:` – maintenance (dependency bumps, etc.)

## Workflows Provided

| File | Purpose |
|---|---|
| `release-ansible-collection.yaml` | Build and publish Ansible collections to Galaxy |
| `release-container.yaml` | Build, scan (Trivy), sign (cosign), push container images |
| `release-mkdocs.yaml` | Build and deploy MkDocs docs to GitHub Pages |
| `release-python-poetry.yaml` | Build and publish Python packages with Poetry |
| `schedule-trivy.yaml` | Scheduled Trivy vulnerability scan for published images |
| `semantic-release.yaml` | Automate releases with go-semantic-release |
| `test-ansible-collection.yaml` | Test Ansible collections |
| `test-pre-commit.yaml` | Run pre-commit hooks |
| `test-python-poetry.yaml` | Run pytest via Poetry |

## Making Changes

### Adding a new reusable workflow

1. Create `.github/workflows/<verb>-<subject>.yaml` with `on: workflow_call`.
2. Add corresponding documentation in `docs/workflows/<category>/<name>.md`.
3. Register the new page in `mkdocs.yml` under `nav:`.
4. Update `docs/permissions.md` with the new workflow's required permissions.

### Updating an existing workflow

1. Edit the workflow YAML.
2. Keep the documentation in sync (inputs table, permissions table, usage example).

### Documentation only

Edit the relevant file under `docs/`. No workflow changes are needed.

## Linting and Testing

There is no automated test suite for the workflows themselves. Documentation can be previewed
locally with:

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
mkdocs serve
```

Pre-commit hooks (if configured in a consuming repo) validate YAML syntax and formatting.

## llms.txt

The documentation site for this repository generates an `llms.txt` index at:

- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt)

External `llms.txt` references for tools used in these workflows:

- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Actions and the broader GitHub platform
- [docs.docker.com/llms.txt](https://docs.docker.com/llms.txt) – Docker build, push, and container image tooling
