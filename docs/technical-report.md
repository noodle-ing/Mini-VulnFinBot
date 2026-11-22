# Technical security report

Repository: https://github.com/noodle-ing/Mini-VulnFinBot

## Scope and method

The CI pipeline runs unit and AI boundary tests, source scanners, dependency scanning, image scanning, and a ZAP baseline scan against the running container. The assistant uses a deterministic mock. Findings below are from local scans on 2026-11-22; the linked GitHub Actions run contains the corresponding CI artifacts.

| Security tool | Findings from completed run | Severity | Recommended action |
| --- | --- | --- | --- |
| Bandit | 0 local findings | None observed | Recheck after code changes |
| Semgrep | 0 on main; 1 before and 0 after on demo branch | High in demo | Replace `eval()` with safe parsing |
| pip-audit | 2 advisory entries for pytest 8.4.2 before dependency update; 0 after updating to pytest 9.x | High until fixed | Keep pytest on a patched release |
| Trivy | Local image: 210 OS findings (50 high, 74 medium, 79 low, 7 unknown), 0 critical; 3 reported Python findings from inherited setuptools 70.3.0 SBOM | High findings remain | Review reachable packages and patched base images; validate SBOM against runtime |
| OWASP ZAP | Initial baseline: 3 alerts (medium, low, informational); final local baseline: 1 informational alert | Informational | Keep `no-store` for financial responses; document the accepted cache warning |
| AI security tests | Mock cases documented in `reports/ai-security-report.md` | Application-level only | Test a controlled real model before claiming prompt-injection resistance |

## Demonstration evidence

1. The [final GitHub Actions run](https://github.com/noodle-ing/Mini-VulnFinBot/actions/runs/45055842741) completed successfully and uploaded `vulnfinbot-security-reports`.
2. The [workflow screenshot](screenshots/actions-success.png) shows a successful run and report artifact; the [issues screenshot](screenshots/issues-closed.png) shows all 10 tickets closed.
3. The isolated `demo/semgrep-remediation` branch contains `reports/semgrep-before.json` (1 finding) and `reports/semgrep-after.json` (0 findings). Commits `8c014e7` and `cc573ed` show the change. Semgrep 1.186.0 was used for the local comparison.

The repository URL is https://github.com/noodle-ing/Mini-VulnFinBot. Its existing name differs from the suggested `vulnfinbot-secure-pipeline` name in the lab handout. The first commit contained a README, so the historic empty-repository step cannot be demonstrated from this repository history.

## Container remediation evidence

The initial Trivy scan found 490 OS and 6 Python findings, including 6 critical OS findings. After upgrading Debian packages, pip and setuptools, the local scan found 210 OS and 3 Python findings with no critical findings. Trivy still lists setuptools 70.3.0 from an inherited SBOM, while the final container has only setuptools 84.2.1 installed in `site-packages`. Treat this discrepancy as a finding requiring manual review, and prioritize the remaining 50 high OS findings against available fixed versions.

The initial local ZAP baseline reported missing Content Security Policy, missing Permissions Policy, and cacheable responses. The API now sets the required policy directives and Cross-Origin-Resource-Policy, disables response caching, and serves `/` as well as `/health`. The final local baseline has no medium or low alerts; its sole informational alert says the responses cannot be cached. This is intentional for a financial assistant. The before/after JSON is reproducible with the workflow and local ZAP command.

## Prioritization

Remediate confirmed critical and high vulnerabilities first, considering exploitability and whether the affected component is reachable. Then review medium and low findings. A scanner alert requires manual validation; a clean report does not prove the application is secure.
