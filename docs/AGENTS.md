# Agent Instructions: docs/

## Purpose

This directory contains the [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
source for the documentation site published at
[radiorabe.github.io/actions](https://radiorabe.github.io/actions/).

The documentation explains how to use every reusable workflow in `.github/workflows/`, with
copy-pasteable YAML snippets, annotated input tables, and permission references.

## Directory Layout

```
docs/
  index.md              # Home page (uses custom template, intentionally minimal)
  getting-started.md    # Quickstart and security baseline instructions
  permissions.md        # Reference table: workflow → required permissions
  workflows/
    index.md            # Workflow category overview table
    ansible/
      index.md          # Ansible category landing page
      release.md        # release-ansible-collection.yaml docs
      test.md           # test-ansible-collection.yaml docs
    container/
      index.md          # Container category landing page
      release.md        # release-container.yaml docs
      schedule.md       # schedule-trivy.yaml docs
    python/
      index.md          # Python category landing page
      release.md        # release-python-poetry.yaml docs
      test.md           # test-python-poetry.yaml docs
    mkdocs.md           # release-mkdocs.yaml docs
    pre-commit.md       # test-pre-commit.yaml docs
    semantic-release.md # semantic-release.yaml docs
  css/
    style.css           # Custom theme overrides
  overrides/
    home.html           # Custom home page template
```

## Page Structure for Each Workflow

Every workflow documentation page follows this structure:

```markdown
# <Category>: <Action>

One-sentence description of what the workflow does.

## Usage

Create a `.github/workflows/<name>.yaml` file:

```yaml title=".github/workflows/<name>.yaml"
name: ...

on: ...

permissions: {} # (1)

jobs:
  <job-name>:
    permissions:
      <permission>: <level> # (2)
    uses: radiorabe/actions/.github/workflows/<file>.yaml@v0.0.0
    with:
      <input>: <value> # (N)
```

1. Deny all permissions at the workflow level as a secure baseline.
2. Explanation for this permission grant.
N. Explanation for this input.

## Inputs

| Input | Description | Required | Default |
|---|---|---|---|
| ... | ... | ... | ... |
```

## Key Conventions

- **Always** include `permissions: {}` at the top-level of every usage example. This is the
  security baseline. Follow it with per-job permission grants using only the minimum required.
- **Code annotations**: Use MkDocs Material
  [code annotations](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#adding-annotations)
  – append `# (N)` comments to YAML lines and provide matching numbered explanations immediately
  after the fenced code block.
- **Version placeholder**: Examples reference `@v0.0.0`. This reminds readers to substitute the
  actual current release tag. Do not use `@main` or `@latest`.
- **Inputs table**: Every workflow page must have an `## Inputs` section even if there are no
  required inputs. Mark required inputs as `**Yes**` in the Required column.
- **Secrets table**: Add a `## Secrets` section when the workflow accepts secrets.

## Navigation

After adding a new page, register it in `mkdocs.yml` under the `nav:` key. Follow the existing
indentation and grouping pattern. Regenerating the nav automatically is not supported.

## Local Preview

```bash
pip install mkdocs-material mkdocs-section-index mkdocs-llmstxt
mkdocs serve
```

Open `http://127.0.0.1:8000` to preview changes before committing.

## llms.txt

The documentation site generates an `llms.txt` index at build time via the `llmstxt` MkDocs
plugin configured in `mkdocs.yml`. The output is published at:

- [radiorabe.github.io/actions/llms.txt](https://radiorabe.github.io/actions/llms.txt)

External `llms.txt` references for documentation tooling used here:

- [docs.github.com/llms.txt](https://docs.github.com/llms.txt) – GitHub Pages deployment and GitHub Actions
- [docs.docker.com/llms.txt](https://docs.docker.com/llms.txt) – Docker and container image concepts
