# Getting Started

## Usage

The examples on this site use `@v0.0.0` as the target version of the action. You **must**
replace that with the current tag of this repository.

To keep your dependencies up to date automatically, create a `.github/dependabot.yaml` file:

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

If you need multiple actions in the same repository, combine them as needed. Please add an
example to the docs if you use the same combination more than once.

## Security

These reusable workflows enforce
[least-privilege](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
by explicitly declaring the minimum `permissions` each workflow job requires.

To implement least access in your downstream repositories:

1. **Restrict default token permissions** in your repository's Settings → Actions → General →
   Workflow permissions. Select **"Read repository contents and packages permissions"** to use
   `contents: read` and `packages: read` as the default.

2. **Set `permissions: {}`** at the top of every calling workflow to start from a baseline of
   no permissions, then grant only what each job needs at the job level.

See the [Permissions](permissions.md) page for a full reference of what each workflow requires.
