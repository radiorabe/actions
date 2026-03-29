# Security: Permissions

These reusable workflows enforce [least-privilege](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) by explicitly declaring the minimum `permissions` each workflow job requires. GitHub Actions enforces the intersection of caller and callee permissions, so the effective permissions for a called workflow are **no more** than what the calling job grants.

## Implementing Least Access

1. **Restrict default token permissions** in your repository's Settings → Actions → General → Workflow permissions. Select **"Read repository contents and packages permissions"** to use `contents: read` and `packages: read` as the default instead of the broader write default.
1. **Set `permissions: {}`** at the top of every calling workflow to start from a baseline of no permissions, then grant only what each job needs at the job level. Every example in this documentation already follows this pattern.
1. **Keep job-level permissions tightly scoped.** The table below lists the minimum permissions each reusable workflow requires. Only grant what is listed; the reusable workflow itself will not request anything beyond these.

## Permissions Reference

| Reusable Workflow                 | Required `permissions`                                                           |
| --------------------------------- | -------------------------------------------------------------------------------- |
| `release-ansible-collection.yaml` | `contents: read`                                                                 |
| `release-container.yaml`          | `contents: read`, `packages: write`, `security-events: write`, `id-token: write` |
| `release-mkdocs.yaml`             | `contents: write`                                                                |
| `release-python-poetry.yaml`      | `contents: write`                                                                |
| `schedule-trivy.yaml`             | `packages: write`, `security-events: write`, `id-token: write`                   |
| `semantic-release.yaml`           | `contents: read`                                                                 |
| `test-ansible-collection.yaml`    | `contents: read`                                                                 |
| `test-github-actions.yaml`        | `contents: read`, `security-events: write`                                       |
| `test-pre-commit.yaml`            | `contents: read`                                                                 |
| `test-python-poetry.yaml`         | `contents: read`                                                                 |

For further reading see GitHub's [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) guide.
