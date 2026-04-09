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
  security/                 # Security controls documentation (ENISA TA alignment)
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
  Use the minimum set required. See `docs/security/permissions.md` for the reference table.
- **Actions pinning**: Pin third-party actions to a commit SHA with the version tag as a
  comment (e.g. `@abc1234def5678 # v3`). Dependabot is configured to keep these pins
  up-to-date automatically. Do not pin to a mutable version tag alone.
  SHA pinning implements ENISA TA §4.2.3 (Integrity Enforcement) and §4.2.6 (Pinning Versions).
- **Security baseline**: Every caller example must set `permissions: {}` at the top level,
  then grant per-job permissions explicitly.
  This implements ENISA TA §4.2.4 (Source/Access Control).
- **New third-party actions**: Before adding any new action, evaluate it against the
  [action selection criteria](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria)
  (ENISA TA §4.1).

### Documentation (`docs/`)

- Written in Markdown and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
- Each reusable workflow has a corresponding documentation file under `docs/workflows/`. Grouped
  workflows (ansible, container, python) live at `docs/workflows/<category>/<name>.md`; standalone
  workflows live directly at `docs/workflows/<name>.md` (e.g. `mkdocs.md`, `pre-commit.md`,
  `semantic-release.md`).
- Use [MkDocs code annotations](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-annotations)
  (`# (N)` inside code blocks with numbered explanations below) to explain individual YAML keys.
- Usage examples must always include `permissions: {}` at the workflow level and explicit
  per-job permissions matching the reference table in `docs/security/permissions.md`.
- Update `mkdocs.yml` `nav:` whenever a new documentation page is added.
- Security documentation lives in `docs/security/`. Each sub-page maps to a group of ENISA TA
  controls (see `docs/security/index.md` for the compliance matrix).

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
4. Update `docs/security/permissions.md` with the new workflow's required permissions.
5. Evaluate all third-party actions against the
   [action selection criteria](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria)
   and document the evaluation in the PR.

### Updating an existing workflow

1. Edit the workflow YAML.
2. Keep the documentation in sync (inputs table, permissions table, usage example).

### Deprecating or removing a workflow

1. Open an `eol-workflow.yml` issue to announce intent and gather feedback.
2. Add a deprecation notice to the workflow YAML (as a comment) and to the docs page.
3. After the deprecation window (at least one minor release), remove the workflow file, its
   documentation page, its entry in `mkdocs.yml` `nav:`, and its row in `docs/security/permissions.md`.

### Pull Requests

All changes go through a pull request. The `.github/PULL_REQUEST_TEMPLATE.md` includes a
checklist to keep changes consistent across all workflow types. Key items:

- Workflow YAML created/updated
- Documentation created/updated
- Permissions table updated (`docs/security/permissions.md`)
- `mkdocs.yml` nav updated (for new docs pages)
- `AGENTS.md` updated (if conventions changed)
- All caller examples include `permissions: {}` at the workflow level
- All third-party actions pinned to a commit SHA with version tag comment (e.g. `@abc1234 # v3`)
- New third-party actions evaluated against the action selection criteria

## Security

Security controls for this repository are documented in `docs/security/` and derive from the
[ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers)
(v1.1, March 2026).

Key security conventions:

| Convention | ENISA TA Control |
|---|---|
| All `uses:` references pinned to full commit SHA | §4.2.3 Integrity Enforcement, §4.2.6 Pinning Versions |
| `permissions: {}` at workflow level + explicit per-job grants | §4.2.4 Source/Access Control |
| Dependabot for daily SHA-pin updates | §4.3.4 Monitor Outdated Versions |
| Trivy scans on container builds and schedule | §4.3.2 Automated Scanning, §4.3.1 SBOM-driven Monitoring |
| CycloneDX SBOM attached as cosign attestation | §4.2.1 SBOM Creation |
| Action selection criteria evaluated before adoption | §4.1.1–§4.1.6 Package Selection |

## Linting and Testing

### CI smoke tests

Every reusable workflow is smoke-tested on each PR to `main`. Smoke tests are split into two
files to keep permission scopes explicit and auditable:

- **`.github/workflows/smoke-test.yaml`** — test-only workflows; all jobs need at most
  `contents: read` + `security-events: write`. Safe for all PR sources.
- **`.github/workflows/smoke-test-release.yaml`** — release/publish workflows that internally
  declare elevated permissions (`packages: write`, `id-token: write`). Comments on every
  elevated permission explain the grant and note that the relevant steps are gated on
  non-PR events inside the called workflow.

Both files call the **local** (current-branch) version of each workflow using
`uses: ./.github/workflows/...` so in-flight changes are validated before merge.

| Smoke test job | File | Workflow under test | Test strategy |
|---|---|---|---|
| `smoke-pre-commit` | `smoke-test.yaml` | `test-pre-commit.yaml` | Run against `.pre-commit-config.yaml` with `requirements: ""` |
| `smoke-test-github-actions` | `smoke-test.yaml` | `test-github-actions.yaml` | Run zizmor SAST on this repo's workflows |
| `smoke-test-python-poetry` | `smoke-test.yaml` | `test-python-poetry.yaml` | Run `pytest` via `tests/python/pyproject.toml` |
| `smoke-test-ansible-collection` | `smoke-test.yaml` | `test-ansible-collection.yaml` | Lint `tests/ansible/` (minimal collection fixture) |
| `smoke-semantic-release` | `smoke-test.yaml` | `semantic-release.yaml` | `dry: true` — compute next version, create nothing |
| `smoke-release-container` | `smoke-test-release.yaml` | `release-container.yaml` | Build `tests/container/Dockerfile` (`FROM ghcr.io/radiorabe/ubi10-minimal`); no push on PRs |
| `smoke-release-python-poetry` | `smoke-test-release.yaml` | `release-python-poetry.yaml` | `poetry publish --build --dry-run` via `tests/python/pyproject.toml` |
| `smoke-release-ansible-collection` | `smoke-test-release.yaml` | `release-ansible-collection.yaml` | Build `tests/ansible/` with `publish: false` |
| `smoke-schedule-trivy` | `smoke-test-release.yaml` | `schedule-trivy.yaml` | Scan `ghcr.io/radiorabe/ubi10-minimal`; `upload-sarif: false`, `attest: false` |

Workflows **not** smoke-tested and why:
- `release-mkdocs.yaml` — self-tests via its own `on: pull_request` trigger in this repo
- `test-ansible-collection.yaml` inputs (`flake8`, `black`) always run on the whole repo root; they are implicitly exercised by the `smoke-test-ansible-collection` job

### Test fixtures

```
tests/
  container/
    Dockerfile        # FROM ghcr.io/radiorabe/ubi10-minimal — input for smoke-release-container
  ansible/
    galaxy.yml        # Minimal Ansible collection descriptor (namespace: radiorabe, name: smoke_test)
    README.md         # Required by ansible-galaxy collection build
    CHANGELOG.md      # Required by ansible-lint galaxy profile
    meta/
      runtime.yml     # Required by ansible-lint galaxy profile
  python/
    pyproject.toml    # Minimal Poetry project (packages = []) for Python smoke tests
    poetry.lock       # Lock file required by actions/setup-python cache: poetry
    tests/
      test_smoke.py   # Trivial pytest used by smoke-test-python-poetry
.pre-commit-config.yaml  # Minimal pre-commit hooks; also the real lint gate for this repo
```

### Making workflows smoke-testable

When adding or updating a reusable workflow, ensure it can be smoke-tested:

- **Required secrets**: use `required: false` for secrets that are only needed for
  production operations (publish, sign, release). The smoke test won't have them.
- **Upload / push side-effects**: add boolean inputs (`upload-sarif`, `attest`, `publish`,
  `dry`, etc.) so smoke tests can disable irreversible side-effects.
- **Working directory**: if the workflow operates on repository-specific files (e.g.,
  `galaxy.yml`), add a `path` input (default: `.`) so the smoke test can point to a
  fixture under `test/`.
- **Permissions**: add the job to the right smoke-test file:
  - `smoke-test.yaml` if the called workflow's jobs need only `contents: read` or `security-events: write`
  - `smoke-test-release.yaml` if the called workflow's jobs declare `packages: write`, `id-token: write`, or other elevated grants — add an explanatory comment for each elevated permission
- **zizmor**: run `zizmor --pedantic .` and fix or suppress all findings before merging.

### Docs preview

```bash
python3 -m venv .venv
.venv/bin/pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
.venv/bin/mkdocs serve
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
