# Contributing

This guide explains how to report issues, propose changes, and submit pull requests for the
reusable workflows in this library.

## Reporting Issues

Use the structured issue templates to open requests. GitHub will show you the template chooser
when you click **New issue** in the repository.

| Template | When to use |
|---|---|
| [Bug Report](https://github.com/radiorabe/actions/issues/new?template=bug-report.yml) | A workflow behaves incorrectly or fails unexpectedly |
| [New Workflow](https://github.com/radiorabe/actions/issues/new?template=new-workflow.yml) | You want to add a new reusable workflow to the library |
| [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) | A workflow needs a new input, a tool version bump, or a behavior change |
| [EOL / Deprecate](https://github.com/radiorabe/actions/issues/new?template=eol-workflow.yml) | A workflow should be deprecated or removed |

## Workflow Lifecycle

### Adding a New Workflow

1. Open a [New Workflow](https://github.com/radiorabe/actions/issues/new?template=new-workflow.yml)
   issue to discuss the proposal before writing code.
2. Create `.github/workflows/<verb>-<subject>.yaml` with `on: workflow_call`.
   Follow the `<verb>-<subject>` naming convention (e.g. `test-go-modules`).
3. Add a documentation file:
    - Grouped workflows (ansible, container, python): `docs/workflows/<category>/<name>.md`
    - Standalone workflows: `docs/workflows/<name>.md`
4. Register the new page in `mkdocs.yml` under `nav:`.
5. Add the workflow to the permissions table in `docs/permissions.md`.
6. Update `AGENTS.md` if the repository structure or conventions change.
7. Submit a pull request — the [PR template](https://github.com/radiorabe/actions/compare)
   includes a full checklist.

### Updating a Workflow

1. Open an [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml)
   issue for non-trivial changes to discuss the approach first.
2. Edit the workflow YAML under `.github/workflows/`.
3. Keep the documentation in sync: inputs table, permissions table, and usage example.
4. For breaking changes, include a migration path in the docs and add a `BREAKING CHANGE:` footer
   to the commit message to trigger a major version bump.

### Deprecating or Removing a Workflow

1. Open an [EOL / Deprecate](https://github.com/radiorabe/actions/issues/new?template=eol-workflow.yml)
   issue to announce intent and gather feedback from users.
2. Add a deprecation notice to the workflow YAML (as a comment) and to the docs page.
3. After the deprecation window (at least one minor release), remove the workflow file, its
   documentation page, its entry in `mkdocs.yml`, and its row in `docs/permissions.md`.

## Pull Requests

All changes go through a pull request to `main`. The
[PR template](https://github.com/radiorabe/actions/compare)
prompts you through the required checklist:

- Workflow YAML created or updated
- Documentation created or updated
- Permissions table updated
- `mkdocs.yml` nav updated (for new pages)
- `AGENTS.md` updated (if conventions changed)
- All caller examples include `permissions: {}` at the workflow level
- New third-party actions pinned to a released version tag

Releases are automated by
[go-semantic-release](https://go-semantic-release.xyz/)
on every push to `main`. Use
[Conventional Commits](https://www.conventionalcommits.org/)
in your commit messages:

| Prefix | Effect |
|---|---|
| `feat:` | New workflow or new input → minor version bump |
| `fix:` | Bug fix → patch bump |
| `docs:`, `ci:`, `chore:` | No release on its own |
| `BREAKING CHANGE:` footer | Major version bump |

## Downstream Projects

The issue templates and PR template in this repository are designed for managing this shared
library. Downstream projects that adopt these workflows may benefit from applying similar
templates in their own repositories to standardise how they manage CI/CD configuration changes.

Copy and adapt the files from `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`
to your project, adjusting the workflow list to those you actually use.

Similarly, add a [Dependabot](https://docs.github.com/en/code-security/dependabot) configuration
to keep workflow version pins up to date automatically:

```yaml title=".github/dependabot.yaml"
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    commit-message:
      prefix: "ci: "
```

See [Getting Started](getting-started.md) for full setup instructions.
