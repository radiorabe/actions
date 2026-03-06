# Agent Instructions: radiorabe/actions

## Repository Purpose

This repository contains [reusable GitHub Actions workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
that Radio Bern RaBe uses for CI/CD across all its projects. Workflows cover container image
releases, Python/Poetry testing and publishing, Ansible collection releases, MkDocs
documentation deployment, pre-commit checks, Trivy security scanning, and semantic versioning.

The full documentation is published at [radiorabe.github.io/actions](https://radiorabe.github.io/actions/).

## Repository Structure

```
.github/workflows/          # Reusable workflow definitions (the actual product)
.github/ISSUE_TEMPLATE/     # Structured issue templates (bug, new-workflow, update, EOL)
.github/PULL_REQUEST_TEMPLATE.md  # PR checklist for all change types
docs/                       # MkDocs source for the published documentation site
  workflows/                # One .md file per reusable workflow
  css/                      # Custom MkDocs theme styles
  overrides/                # MkDocs theme overrides
mkdocs.yml                  # MkDocs configuration
catalog-info.yaml           # Backstage component descriptor
```

## Conventions

### Workflow Files (`.github/workflows/`)

- **Naming**: `<verb>-<subject>.yaml` – e.g. `release-container.yaml`, `test-python-poetry.yaml`. The file `semantic-release.yaml` is an explicit exception to mirror the upstream tool name.
- **Trigger**: All reusable workflows include `on: workflow_call` so they can be called from other workflows.
- **Permissions**: Declare `permissions:` on **every job**, not at the workflow level.
  Use the minimum set required. See `docs/permissions.md` for the reference table.
- **Actions pinning**: Pin third-party actions to a released version tag (e.g. `@v3`).
  Dependabot is configured to keep all version tags up-to-date automatically — do not
  replace tags with commit SHAs.
- **Security baseline**: Every caller example must set `permissions: {}` at the top level,
  then grant per-job permissions explicitly.

### Documentation (`docs/`)

- Written in Markdown and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
- Each reusable workflow has a corresponding documentation file under `docs/workflows/`. Grouped
  workflows (ansible, container, python) live at `docs/workflows/<category>/<name>.md`; standalone
  workflows live directly at `docs/workflows/<name>.md` (e.g. `mkdocs.md`, `pre-commit.md`,
  `semantic-release.md`).
- Use [MkDocs code annotations](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-annotations)
  (`# (N)` inside code blocks with numbered explanations below) to explain individual YAML keys.
- Usage examples must always include `permissions: {}` at the workflow level and explicit
  per-job permissions matching the reference table in `docs/permissions.md`.
- Update `mkdocs.yml` `nav:` whenever a new documentation page is added.

### Conventional Commits and Versioning

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification. Releases are automated by go-semantic-release on every push to `main`:

- `feat:` – new workflow or new input → **minor** version bump
- `fix:` – bug fix in a workflow → **patch** bump
- `docs:`, `ci:`, `chore:` – no release unless combined with the above
- `BREAKING CHANGE:` footer on any type → **major** bump

All work happens on feature branches. Open a PR to `main`; do not manually create version tags.

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

### Issue Templates

Use the structured issue templates when opening requests. Choose the right template from
`.github/ISSUE_TEMPLATE/`:

| Template | When to use |
|---|---|
| `bug-report.yml` | A workflow behaves incorrectly or fails unexpectedly |
| `new-workflow.yml` | Proposing a new reusable workflow |
| `update-workflow.yml` | Requesting a new input, version bump, or behavior change |
| `eol-workflow.yml` | Proposing deprecation or removal of a workflow |

### Adding a new reusable workflow

1. Create `.github/workflows/<verb>-<subject>.yaml` with `on: workflow_call`.
2. Add a corresponding documentation file: grouped workflows go in
   `docs/workflows/<category>/<name>.md`; standalone workflows go directly in
   `docs/workflows/<name>.md`.
3. Register the new page in `mkdocs.yml` under `nav:`.
4. Update `docs/permissions.md` with the new workflow's required permissions.

### Updating an existing workflow

1. Edit the workflow YAML.
2. Keep the documentation in sync (inputs table, permissions table, usage example).

### Deprecating or removing a workflow

1. Open an `eol-workflow.yml` issue to announce intent and gather feedback.
2. Add a deprecation notice to the workflow YAML (as a comment) and to the docs page.
3. After the deprecation window (at least one minor release), remove the workflow file, its
   documentation page, its entry in `mkdocs.yml` `nav:`, and its row in `docs/permissions.md`.

### Pull Requests

All changes go through a pull request. The `.github/PULL_REQUEST_TEMPLATE.md` includes a
checklist to keep changes consistent across all workflow types. Key items:

- Workflow YAML created/updated
- Documentation created/updated
- Permissions table updated (`docs/permissions.md`)
- `mkdocs.yml` nav updated (for new docs pages)
- `AGENTS.md` updated (if conventions changed)
- All caller examples include `permissions: {}` at the workflow level
- New third-party actions pinned to a released version tag

## Linting and Testing

No automated test suite. Preview docs locally:

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
mkdocs serve
```

## llms.txt

- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt) – this repo (auto-generated at build time)
- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Actions and the GitHub platform
- [docs.docker.com/llms.txt](https://docs.docker.com/llms.txt) – Docker build and container image tooling

Tool docs (no llms.txt available):

- [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material/) – MkDocs Material theme
- [trivy.dev](https://trivy.dev/) – Trivy security scanner
- [docs.sigstore.dev](https://docs.sigstore.dev/) – cosign and Sigstore signing
- [python-poetry.org/docs](https://python-poetry.org/docs/) – Poetry Python package manager
- [pre-commit.com](https://pre-commit.com/) – pre-commit framework
- [go-semantic-release.xyz](https://go-semantic-release.xyz/) – go-semantic-release
