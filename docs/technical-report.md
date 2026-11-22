# Technical security report

Repository: https://github.com/noodle-ing/Mini-VulnFinBot

## Scope and method

The CI pipeline runs unit and AI boundary tests, source scanners, dependency scanning, image scanning, and a ZAP baseline scan against the running container. The assistant uses a deterministic mock. Record the GitHub Actions run URL and actual counts below after the pipeline has completed; scanner findings must not be invented before reports exist.

| Security tool | Findings from completed run | Severity | Recommended action |
| --- | --- | --- | --- |
| Bandit | 0 local findings; confirm in CI | None observed | Recheck after code changes |
| Semgrep | 0 on main; 1 before and 0 after on demo branch | High in demo | Replace `eval()` with safe parsing |
| pip-audit | 2 advisory entries for pytest 8.4.2 before dependency update; 0 after updating to pytest 9.x | High until fixed | Keep pytest on a patched release |
| Trivy | Pending CI report | Pending | Update base image and affected OS/Python packages |
| OWASP ZAP | Pending CI report | Pending | Review headers and information disclosure findings |
| AI security tests | Mock cases documented in `reports/ai-security-report.md` | Application-level only | Test a controlled real model before claiming prompt-injection resistance |

## Demonstration evidence

1. Add the Actions run URL and screenshot of completed jobs.
2. Add screenshots showing the six downloaded report files and representative findings.
3. The isolated `demo/semgrep-remediation` branch contains `reports/semgrep-before.json` (1 finding) and `reports/semgrep-after.json` (0 findings). Commits `8c014e7` and `cc573ed` show the change.
4. Local scan date: 2026-11-22. Semgrep 1.186.0 reported 1 finding before and 0 after. Record versions from the final CI run too, since vulnerability databases change.

## Prioritization

Remediate confirmed critical and high vulnerabilities first, considering exploitability and whether the affected component is reachable. Then review medium and low findings. A scanner alert requires manual validation; a clean report does not prove the application is secure.
