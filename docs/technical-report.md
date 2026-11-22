# Technical security report

Repository: https://github.com/noodle-ing/Mini-VulnFinBot

## Scope and method

The CI pipeline runs unit and AI boundary tests, source scanners, dependency scanning, image scanning, and a ZAP baseline scan against the running container. The assistant uses a deterministic mock. Record the GitHub Actions run URL and actual counts below after the pipeline has completed; scanner findings must not be invented before reports exist.

| Security tool | Findings from completed run | Severity | Recommended action |
| --- | --- | --- | --- |
| Bandit | Pending CI report | Pending | Review each code finding; replace unsafe APIs |
| Semgrep | Pending CI report | Pending | Remove any `eval()` usage; see remediation demo |
| pip-audit | Pending CI report | Pending | Upgrade affected Python packages to patched versions |
| Trivy | Pending CI report | Pending | Update base image and affected OS/Python packages |
| OWASP ZAP | Pending CI report | Pending | Review headers and information disclosure findings |
| AI security tests | Mock cases documented in `reports/ai-security-report.md` | Application-level only | Test a controlled real model before claiming prompt-injection resistance |

## Demonstration evidence

1. Add the Actions run URL and screenshot of completed jobs.
2. Add screenshots showing the six downloaded report files and representative findings.
3. Add before/after Semgrep report counts and the remediation diff from the isolated demo branch.
4. Record the scanner versions and date, since vulnerability databases change.

## Prioritization

Remediate confirmed critical and high vulnerabilities first, considering exploitability and whether the affected component is reachable. Then review medium and low findings. A scanner alert requires manual validation; a clean report does not prove the application is secure.
