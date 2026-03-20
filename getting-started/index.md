# Getting Started

## Usage

The examples on this site use `@v0.0.0` as the target version of the action. You **must** replace that with the current tag of this repository.

To keep your dependencies up to date automatically, create a `.github/dependabot.yaml` file:

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

Dependabot keeps SHA-pinned action references up to date automatically. When it opens a PR you will see the commit SHA change alongside the version tag comment, for example `@abc1234 # v3` → `@def5678 # v4`.

If you need multiple actions in the same repository, combine them as needed. Please add an example to the docs if you use the same combination more than once.

## Security

These reusable workflows enforce [least-privilege](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) by explicitly declaring the minimum `permissions` each workflow job requires.

To implement least access in your downstream repositories:

1. **Restrict default token permissions** in your repository's Settings → Actions → General → Workflow permissions. Select **"Read repository contents and packages permissions"** to use `contents: read` and `packages: read` as the default.
1. **Set `permissions: {}`** at the top of every calling workflow to start from a baseline of no permissions, then grant only what each job needs at the job level.
1. **Pin actions to commit SHAs** rather than mutable version tags. Every workflow in this library pins its third-party actions to a specific commit SHA with the version tag as an inline comment (e.g. `uses: actions/checkout@abc1234 # v4.2.0`). Dependabot keeps these pins current. Use the same pattern in your own workflows.
1. **Immutable releases** — releases in this repository are [immutable](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository). Once a GitHub Release is published it cannot be edited or deleted. When you pin to a released tag or its underlying commit SHA you can be confident the content will never silently change.

See the [Permissions](https://radiorabe.github.io/actions/permissions/index.md) page for a full reference of what each workflow requires.

## Issue and Pull Request Templates

To make managing your CI/CD configuration easier, add the issue templates and PR template from this repository to your own project. They provide structured forms for reporting workflow bugs, requesting updates, and tracking version changes.

Copy the files from `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md` in this repository and adapt the workflow list to the ones you actually use.

See the [Contributing](https://radiorabe.github.io/actions/contributing/index.md) guide for the full workflow lifecycle and how these templates are used to maintain this library.
