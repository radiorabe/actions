# Security

This section documents how the reusable workflows in this library implement the security controls recommended by the [ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers) (v1.1, March 2026, CC BY 4.0).

Although the ENISA advisory focuses on traditional package managers (npm, pip, Maven, etc.), its controls map directly to GitHub Actions workflows: **every referenced third-party action is a package**, and the **GitHub Marketplace / repository reference system is the registry**. The same risks apply — dependency confusion, supply chain injection, compromised maintainers — and the same mitigations work.

## Threat Model

| ENISA Risk                           | GitHub Actions Equivalent                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------------ |
| Insertion of malicious packages      | A third-party action is replaced or injected with malicious code in a new commit     |
| Compromised legitimate package       | An action maintainer's account is hijacked and a backdoored version is published     |
| Typosquatting                        | An action with a name similar to a trusted one (e.g. `actons/checkout`) is published |
| Namespace / Dependency Confusion     | An action published in a public namespace shadows an intended private one            |
| Discontinued / unmaintained packages | An abandoned action receives no security fixes                                       |

## Controls Compliance Matrix

All controls from ENISA TA §4 are mapped below. Status: ✅ Implemented · ⚠️ Partial · ❌ Gap · N/A Not applicable

### §4.1 Package Selection

| Control                        | Description                                                | Status | Reference                                                                                                                                                     |
| ------------------------------ | ---------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4.1.1 Trusted Source           | Use official registries; prefer provenance metadata        | ✅     | SHA pins enforce exact commit; Dependabot keeps them current                                                                                                  |
| 4.1.2 Known Vulnerabilities    | Check vulnerability databases before adopting a dependency | ⚠️     | Dependabot alerts exist; pre-adoption scanning not yet automated — see [#194](https://github.com/radiorabe/actions/issues/194)                                |
| 4.1.3 Signing & Integrity      | Use cryptographic signing to verify integrity              | ✅     | SHA pinning is cryptographic integrity for actions; cosign + SLSA for containers                                                                              |
| 4.1.4 Maintainer Reputation    | Select packages from reputable, verified maintainers       | ⚠️     | Criteria documented in [Supply Chain](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria); process gap for automated checks |
| 4.1.5 Popularity & Maintenance | Community adoption, recent activity, commit history        | ⚠️     | Criteria documented in [Supply Chain](https://radiorabe.github.io/actions/security/supply-chain/#action-selection-criteria)                                   |

### §4.2 Package Integration

| Control                              | Description                                          | Status | Reference                                                                               |
| ------------------------------------ | ---------------------------------------------------- | ------ | --------------------------------------------------------------------------------------- |
| 4.2.1 SBOM Creation                  | Generate a Software Bill of Materials                | ❌     | This repository does not generate a SBOM for the generated workflows and their contents |
| 4.2.2 Vulnerability Checks           | Enforce security gates in CI/CD                      | ✅     | Trivy scans container images; build fails on HIGH/CRITICAL findings                     |
| 4.2.3 Integrity Enforcement          | Enforce hash or lockfile verification                | ✅     | All actions pinned to commit SHA (`@<sha> # vN.N.N`)                                    |
| 4.2.4 Source Enforcement             | Restrict to trusted registries; validate source URLs | ✅     | SHA pinning prevents substitution; no un-pinned registry fallback                       |
| 4.2.5 Installation Script Prevention | Disable/restrict scripts during installation         | N/A    | GitHub Actions has no equivalent install-script mechanism                               |
| 4.2.6 Pinning Versions               | Fix dependency versions; use lockfiles               | ✅     | Every third-party action reference is pinned to a commit SHA; Dependabot maintains them |

### §4.3 Package Monitoring

| Control                           | Description                                                  | Status | Reference                                                                                                                                                                                                   |
| --------------------------------- | ------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4.3.1 SBOM-driven Monitoring      | Leverage SBOM data to automate vulnerability correlation     | ❌     | This repo does not create/consume SBOMs                                                                                                                                                                     |
| 4.3.2 Automated Scanning in CI/CD | Continuously scan dependencies                               | ❌     | The contents of this repo are not automatically scanned                                                                                                                                                     |
| 4.3.3 Track CVEs / Advisories     | Monitor EUVD, OSV.dev, GitHub Advisories                     | ⚠️     | Dependabot covers GitHub Advisory Database; manual EUVD/OSV monitoring documented in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#advisory-monitoring) |
| 4.3.4 Monitor Outdated Versions   | Check for newer versions                                     | ✅     | Dependabot opens PRs daily for outdated SHA pins                                                                                                                                                            |
| 4.3.5 Set Alerts                  | Alerts for new CVEs, deprecated releases, maintainer changes | ⚠️     | Dependabot covers CVE/version alerts; no automated maintainer-change detection — see [#194](https://github.com/radiorabe/actions/issues/194)                                                                |

### §4.4 Vulnerability Mitigation

| Control                 | Description                                         | Status | Reference                                                                                                                                                               |
| ----------------------- | --------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4.4.1 Assess            | CVSS, EPSS, KEV metrics; reachability analysis      | ⚠️     | Process documented in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#assessment); no automated reachability tool yet |
| 4.4.2 Prioritise        | Risk thresholds (CVSS ≥ 7.0, EPSS, KEV)             | ✅     | Thresholds documented in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#prioritisation)                              |
| 4.4.3 Mitigate          | Upgrade, temporary controls, removal                | ✅     | Steps documented in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#mitigation-steps)                                 |
| 4.4.4 Document & Notify | Release notes, GHSA advisories, notify stakeholders | ⚠️     | Process documented in [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/#notification); full automation not yet in place |

## Sections

- [Supply Chain Security](https://radiorabe.github.io/actions/security/supply-chain/index.md) — action selection, SHA pinning, provenance, SBOM (§4.1, §4.2)
- [Vulnerability Management](https://radiorabe.github.io/actions/security/vulnerability-management/index.md) — scanning, monitoring, assessment, mitigation (§4.3, §4.4)
- [Permissions](https://radiorabe.github.io/actions/security/permissions/index.md) — least-privilege token permissions

## Quarterly Review

To stay aligned with the ENISA TA and the evolving threat landscape, this library follows a **quarterly security review cadence**:

1. Check the [ENISA EU Vulnerability Database (EUVD)](https://euvd.enisa.europa.eu/) and [OSV.dev](https://osv.dev/) for new advisories affecting actions used in this library.
1. Review Dependabot alerts and ensure no open HIGH/CRITICAL findings are older than 30 days without a tracked issue.
1. Re-evaluate the compliance matrix above — update status as controls are implemented or gaps are found.
1. Review open issues tagged `security` and ensure they have owners and timelines.

The quarterly review should be tracked with an [Update Workflow](https://github.com/radiorabe/actions/issues/new?template=update-workflow.yml) issue using the **Security improvement** update type.

## Attribution

Security controls in this section are derived from the [ENISA Technical Advisory for Secure Use of Package Managers](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers), v1.1, March 2026. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
