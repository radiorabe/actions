# Security: Supply Chain

This page documents how the library implements the package **selection** and **integration**
controls from §4.1 and §4.2 of the
[ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers).

In this context "packages" means third-party GitHub Actions referenced in workflow files.

---

## Action Selection Criteria

*Implements ENISA TA §4.1.1 (Trusted Source), §4.1.4 (Maintainer Reputation),
§4.1.5 (Popularity & Maintenance), §4.1.6 (Secure Practices).*

Before adding any third-party action to a workflow, evaluate it against the following
criteria. All criteria should pass before the action is adopted. Document the evaluation in
the pull request or the associated [New Workflow](https://github.com/radiorabe/actions/issues/new?template=new-workflow.yml)
/ [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) issue.

### Trusted Source — §4.1.1

- [ ] The action is published under a **verified organisation account** (GitHub verified badge
      or a well-known project such as `actions/`, `docker/`, `sigstore/`, `aquasecurity/`,
      `github/`).
- [ ] The action repository is the **canonical upstream** — not a fork, mirror, or re-publish.
- [ ] The action's repository URL is the same one referenced in the workflow (`uses:` field).

### Known Vulnerabilities — §4.1.2

- [ ] The action and its dependencies have been checked against the
      [GitHub Advisory Database](https://github.com/advisories) and
      [OSV.dev](https://osv.dev/) for known CVEs.
- [ ] No unmitigated HIGH or CRITICAL advisories exist for the action at the version being
      pinned.

### Signing & Integrity — §4.1.3

- [ ] The action commit being pinned is **reachable from a signed release tag** in the upstream
      repository (i.e. the SHA is not an arbitrary commit between releases).
- [ ] For container-image actions, the image is signed with cosign and the signature is
      verifiable.

### Maintainer Reputation — §4.1.4

- [ ] The maintaining organisation or individual has a **public track record** of security
      responsiveness (past CVE disclosures, security advisories, or responsible disclosure
      policy).
- [ ] The action has been in active use in major open-source projects (evidence via GitHub
      dependency graph or documented adoption).
- [ ] No recent ownership transfers or significant maintainer-base changes have occurred
      without community disclosure.

### Popularity & Maintenance — §4.1.5

- [ ] The action repository shows **recent commit activity** (within the last 6 months for
      actively used dependencies; within 12 months for stable/mature ones).
- [ ] The action has **open issue responsiveness**: maintainers respond to security issues
      within a reasonable time.
- [ ] The number of downstream users (GitHub Marketplace installs, stars, network dependents)
      indicates broad adoption — but note that popularity metrics can be gamed; use them as
      one signal, not the sole criterion.

### Secure Practices — §4.1.6

- [ ] The action's own workflow files follow security best practices (pinned dependencies,
      least-privilege permissions, no `pull_request_target` with `write` permissions on
      untrusted input).
- [ ] The action does not request unnecessary permissions in its own `action.yml`.
- [ ] The action does not run `curl | bash` or equivalent unbounded remote execution during
      setup.

---

## SHA Pinning

*Implements ENISA TA §4.2.3 (Integrity Enforcement) and §4.2.6 (Pinning Versions).*

Every third-party action reference in this library is pinned to a **full commit SHA** with
the version tag as an inline comment:

```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

This provides two complementary controls in one line:

| What | How | ENISA Control |
|---|---|---|
| **Version pinning** | The SHA is immutable — unlike a version tag, it cannot be moved or deleted | §4.2.6 |
| **Integrity enforcement** | GitHub resolves the `uses:` reference by SHA; a different commit cannot be substituted | §4.2.3 |
| **Human readability** | The inline comment (`# v4.2.2`) shows which release the SHA corresponds to | — |

### Automation with Dependabot

Pinned SHAs are kept current automatically by Dependabot. When a new version of an action is
released, Dependabot opens a PR that updates both the SHA and the inline version comment.
This maintains the integrity guarantee without requiring manual tracking.

Configure Dependabot in your downstream repository:

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

### Never Use Mutable References

These reference styles are **prohibited** in this library because they do not provide
integrity guarantees:

| Prohibited | Reason |
|---|---|
| `uses: actions/checkout@v4` | Mutable tag — can be moved silently |
| `uses: actions/checkout@main` | Branch reference — changes on every commit |
| `uses: actions/checkout@latest` | Alias — no integrity guarantee |

---

## Package Source Enforcement

*Implements ENISA TA §4.2.4 (Package Source Enforcement).*

SHA pinning prevents source substitution: if an attacker replaces a published action with
malicious code at the same version tag, the SHA in our workflow will no longer match, and the
run will fail. This is the GitHub Actions equivalent of enforcing a trusted registry URL.

---

## SBOM Gap — §4.2.1 (SBOM Creation)

This library provides workflow definitions only; it does not itself publish container images.
Therefore, SBOM generation is a **gap** in this repository with respect to ENISA TA §4.2.1.

Callers can and should generate SBOMs in their own release pipeline when they run
`release-container.yaml` (or equivalent). The gap tracking status for this control is:

- **Status:** ❌ Gap
- **Mitigation:** Document in the caller README and ensure the image release workflow generates
  CycloneDX SBOMs and signs them with cosign.

!!! note "Future improvement"
    Automated SBOM generation for the action dependency graph (workflow references and transitive
    action dependencies) is still a planned improvement, as described in this repository's
    risks and compliance tracking.

---

## Installation Script Prevention

*ENISA TA §4.2.5 — Not Applicable.*

Traditional package managers (npm, pip) execute arbitrary scripts during installation
(`preinstall`, `postinstall`). GitHub Actions has no equivalent mechanism: an action is
either a Docker image, a JavaScript file, or a composite of shell steps — none of which
have an automatic install-script phase triggered by the `uses:` directive. This control is
therefore not applicable in the Actions context.

---

## Attribution

Controls in this page are derived from the
[ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers),
v1.1, March 2026. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
