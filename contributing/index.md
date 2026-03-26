# Contributing

This guide explains how to report issues, propose changes, and submit pull requests for the reusable workflows in this library.

## Security Review

All changes that introduce or update a third-party action, change permissions, or affect the security posture of the library must be reviewed against the controls documented in [docs/security/](https://radiorabe.github.io/actions/security/index.md).

### When the security docs apply

| Change type            | Required review                                                                                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New third-party action | Full [action selection criteria](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria) evaluation; document in issue or PR                                                                            |
| Updated SHA pin        | Confirm the new SHA is reachable from a signed release tag                                                                                                                                                                            |
| Permission change      | Verify against [Permissions](https://radiorabe.github.io/actions/security/permissions/index.md) reference; justify any increase                                                                                                       |
| Vulnerability fix      | Follow the [mitigation steps](https://radiorabe.github.io/actions/security/vulnerability-management/#mitigation-steps) and [VEX process](https://radiorabe.github.io/actions/security/vulnerability-management/#vex-and-notification) |
| Any other change       | Check the PR checklist for the two new security items                                                                                                                                                                                 |

### Quarterly ENISA alignment review

Once per quarter, a maintainer should open an [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) issue with type **Security improvement** to:

1. Check the [EUVD](https://euvd.enisa.europa.eu/) and [OSV.dev](https://osv.dev/) for new advisories affecting actions used in this library.
1. Verify all open Dependabot alerts have been reviewed and are within the response time thresholds in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#prioritisation).
1. Update the [compliance matrix](https://radiorabe.github.io/actions/security/#controls-compliance-matrix) if any control status has changed.
1. Review and triage any `security`-labelled open issues.

## Reporting Issues

Use the structured issue templates to open requests. GitHub will show you the template chooser when you click **New issue** in the repository.

| Template                                                                                        | When to use                                                             |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [Bug Report](https://github.com/radiorabe/actions/issues/new?template=bug-report.yml)           | A workflow behaves incorrectly or fails unexpectedly                    |
| [New Workflow](https://github.com/radiorabe/actions/issues/new?template=new-workflow.yml)       | You want to add a new reusable workflow to the library                  |
| [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) | A workflow needs a new input, a tool version bump, or a behavior change |
| [EOL / Deprecate](https://github.com/radiorabe/actions/issues/new?template=eol-workflow.yml)    | A workflow should be deprecated or removed                              |

## Workflow Lifecycle

### Adding a New Workflow

1. Open a [New Workflow](https://github.com/radiorabe/actions/issues/new?template=new-workflow.yml) issue to discuss the proposal before writing code.
1. Create `.github/workflows/<verb>-<subject>.yaml` with `on: workflow_call`. Follow the `<verb>-<subject>` naming convention (e.g. `test-go-modules`).
1. Add a documentation file:
   - Grouped workflows (ansible, container, python): `docs/workflows/<category>/<name>.md`
   - Standalone workflows: `docs/workflows/<name>.md`
1. Register the new page in `mkdocs.yml` under `nav:`.
1. Add the workflow to the permissions table in `docs/security/permissions.md`.
1. Update `AGENTS.md` if the repository structure or conventions change.
1. Submit a pull request — the [PR template](https://github.com/radiorabe/actions/compare) includes a full checklist.

### Updating a Workflow

1. Open an [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) issue for non-trivial changes to discuss the approach first.
1. Edit the workflow YAML under `.github/workflows/`.
1. Keep the documentation in sync: inputs table, permissions table, and usage example.
1. For breaking changes, include a migration path in the docs and add a `BREAKING CHANGE:` footer to the commit message to trigger a major version bump.

### Deprecating or Removing a Workflow

1. Open an [EOL / Deprecate](https://github.com/radiorabe/actions/issues/new?template=eol-workflow.yml) issue to announce intent and gather feedback from users.
1. Add a deprecation notice to the workflow YAML (as a comment) and to the docs page.
1. After the deprecation window (at least one minor release), remove the workflow file, its documentation page, its entry in `mkdocs.yml`, and its row in `docs/security/permissions.md`.

## Pull Requests

All changes go through a pull request to `main`. The [PR template](https://github.com/radiorabe/actions/compare) prompts you through the required checklist:

- Workflow YAML created or updated
- Documentation created or updated
- Permissions table in `docs/security/permissions.md` updated
- `mkdocs.yml` nav updated (for new pages)
- `AGENTS.md` updated (if conventions changed)
- All caller examples include `permissions: {}` at the workflow level
- All third-party actions pinned to a commit SHA with version tag comment (e.g. `@abc1234 # v3`)
- New third-party actions reviewed against the [action selection criteria](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria)

Releases are automated by [go-semantic-release](https://go-semantic-release.xyz/) on every push to `main`. Use [Conventional Commits](https://www.conventionalcommits.org/) in your commit messages:

| Prefix                    | Effect                                         |
| ------------------------- | ---------------------------------------------- |
| `feat:`                   | New workflow or new input → minor version bump |
| `fix:`                    | Bug fix → patch bump                           |
| `docs:`, `ci:`, `chore:`  | No release on its own                          |
| `BREAKING CHANGE:` footer | Major version bump                             |

## Downstream Projects

The issue templates and PR template in this repository are designed for managing this shared library. Downstream projects that adopt these workflows may benefit from applying similar templates in their own repositories to standardise how they manage CI/CD configuration changes.

Copy and adapt the files from `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` to your project, adjusting the workflow list to those you actually use.

Similarly, add a [Dependabot](https://docs.github.com/en/code-security/dependabot) configuration to keep workflow SHA pins up to date automatically:

.github/dependabot.yaml

```
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    commit-message:
      prefix: "ci: "
```

See [Getting Started](https://radiorabe.github.io/actions/getting-started/index.md) for full setup instructions.
