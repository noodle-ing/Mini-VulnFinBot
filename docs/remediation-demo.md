# Scanner detection and remediation demo

The CI custom Semgrep rule in `security/semgrep/rules.yml` detects Python `eval()` calls. Keep the intentionally vulnerable sample out of the normal application and demonstrate it on a temporary branch.

From the repository root:

```bash
git switch -c demo/semgrep-remediation-repeat
mkdir -p reports
cat > app/demo_insecure.py <<'PY'
user_value = input("Expression: ")
print(eval(user_value))
PY
git add app/demo_insecure.py
semgrep scan --config security/semgrep/rules.yml --json --output reports/semgrep-before.json app/demo_insecure.py
```

Stage the example before scanning because Semgrep scans tracked files by default. The `before` report should contain `python-eval-user-input`. Replace the unsafe evaluation with safe literal parsing and capture the after report:

```bash
cat > app/demo_insecure.py <<'PY'
import ast

user_value = input("Expression: ")
print(ast.literal_eval(user_value))
PY
semgrep scan --config security/semgrep/rules.yml --json --output reports/semgrep-after.json app/demo_insecure.py
```

The `after` report should have no `python-eval-user-input` finding. Reports under `reports/` are ignored by Git during ordinary development, so force-add these two demonstration outputs plus a short note with the Semgrep version and finding counts to the temporary branch, then push it so Actions records the run:

```bash
git add -f reports/semgrep-before.json reports/semgrep-after.json
```

Do not merge this demo branch. Return to the clean branch when finished:

```bash
git switch main
git branch -D demo/semgrep-remediation-repeat
```

Save screenshots of the Actions run and reports for the final submission. The reports are generated at demo time because scanner output depends on the installed Semgrep version.
