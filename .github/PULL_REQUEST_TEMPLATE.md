## Summary

<!-- Describe the change and link to the related issue. -->

Closes #

## Type of Change

- [ ] 🐛 Bug fix — patch version bump
- [ ] ✨ New workflow — minor version bump
- [ ] 🔧 Update existing workflow — patch or minor version bump
- [ ] 🗑️ EOL / deprecate workflow
- [ ] 📖 Documentation only
- [ ] 🔒 Security improvement
- [ ] 🤖 Dependency / tooling update

## Checklist

- [ ] Workflow YAML is created or updated under `.github/workflows/`
- [ ] Documentation is created or updated under `docs/workflows/`
- [ ] Permissions table in `docs/permissions.md` is updated
- [ ] `mkdocs.yml` nav is updated (required when a new docs page is added)
- [ ] `AGENTS.md` is updated (required when repository structure or conventions change)
- [ ] All caller examples include `permissions: {}` at the workflow level with explicit per-job permissions
- [ ] Any new third-party actions are pinned to a released version tag (e.g. `@v3`)
- [ ] For breaking changes: migration guidance is included in the docs and commit message contains `BREAKING CHANGE:`
- [ ] For EOL: deprecation notice is added to the workflow YAML and docs
