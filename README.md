# Mini-VulnFinBot

A small financial assistant API built with Python 3.12 and Flask. It currently returns a deterministic mock budgeting tip. The repository demonstrates pytest, GitHub Actions, Bandit, Semgrep, pip-audit, Docker, Trivy, and OWASP ZAP. No LLM or external financial service is connected.

## Architecture

`app/__init__.py` creates the Flask app; `app/routes.py` handles `/health` and `/api/chat`; `run.py` is the local entry point. `tests/` contains API and AI security boundary tests. `security/semgrep/rules.yml` holds the custom static rule. `.github/workflows/security-pipeline.yml` builds, tests, scans, and uploads reports.

## Install and run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

On Windows activate with `.venv\Scripts\activate`. The app listens on `http://127.0.0.1:5000` locally.

```bash
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/api/chat -H 'Content-Type: application/json' -d '{"message":"How can I manage my monthly budget?"}'
```

The health response is `{"status":"healthy"}`. The chat response is `{"response":"You can start by tracking your income and expenses."}`. Invalid requests receive JSON errors and appropriate HTTP status codes. Messages are limited to 2,000 characters. User messages are not logged.

## Tests and scanners

```bash
pytest -v
pip install bandit semgrep pip-audit
mkdir -p reports
bandit -r app -f json -o reports/bandit-report.json
semgrep scan --config security/semgrep/rules.yml --json --output reports/semgrep-report.json app
pip-audit -r requirements.txt -f json -o reports/dependency-report.json
docker build -t vulnfinbot:latest .
docker run --rm -p 8000:8000 vulnfinbot:latest
trivy image --format json --output reports/trivy-report.json vulnfinbot:latest
```

For a local ZAP scan, start the container, verify `http://127.0.0.1:8000/health`, then run the command used in the workflow. Docker host networking differs by operating system; the CI command is configured for an Ubuntu runner.

## CI pipeline and reports

On push and pull request, GitHub Actions installs dependencies and runs pytest, Bandit, the custom Semgrep rule, pip-audit, Docker build, Trivy, and ZAP baseline. The workflow uploads `reports/` as the `vulnfinbot-security-reports` artifact even if a later step fails. Open the run in **GitHub → Actions → Security CI Pipeline → Artifacts** to download reports. Reports are kept for 30 days.

The six expected reports are `bandit-report.json`, `semgrep-report.json`, `dependency-report.json`, `trivy-report.json`, `zap-report.json`, and `ai-security-report.md`. Scanner JSON files are generated during CI and ignored by Git. [AI security report](reports/ai-security-report.md) explains the limits of the mock. [Technical report](docs/technical-report.md) records findings and remediation. [Remediation demo](docs/remediation-demo.md) explains the isolated vulnerable pattern demonstration.

## Security findings and remediation

Review the generated reports for actual findings after each pipeline run. In this small mock app, the custom Semgrep rule should find no `eval()` calls in `app/`. The demo branch introduces one controlled `eval()` example and replaces it with `ast.literal_eval()`. Dependency and image findings vary with package and base-image versions; update affected versions and rebuild. ZAP may identify missing HTTP security headers; assess each finding in context and configure headers before production use. A real LLM would need separate prompt-injection and tool-authorization tests.
