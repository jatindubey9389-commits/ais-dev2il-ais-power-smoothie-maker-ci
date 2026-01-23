# ais-dev2il-ais-power-smoothie-maker-ci
Reliable smoothie blending using CI

Notes
- Start with simple pipeline
- Configure the repository right away to not allow pushes to main 

Level up
- test reports 

Checks
- Forked Repos

docker run -v .:/path ghcr.io/gitleaks/gitleaks:latest dir path --report-path=- --report-format=csv
echo $?

pre-commit
- explain what a pre-commit hook is
- explain what the framework does 
- follow gitleak pre-commit instructions on github 
- ignore false positives via via comment in source code

explain what uvx is
is this already used in the last session ? 

3. The Documentation Trail (Compliance)
In a regulated environment (SOC2, ISO27001), you cannot just "ignore" a bug. You must document why.

The idiomatic way is to check in a file called SECURITY_VETTING.md or similar to your repo:

Vulnerability: CVE-2023-9999 (Unpatched) Dependency: some-package==1.2.3 Status: Risk Accepted. Reasoning: The vulnerability requires local file access which is impossible in our serverless environment. We will re-evaluate when v1.2.4 is released.
https://pypi.org/project/uv-secure/
What is CVSS ?

https://github.com/gitleaks/gitleaks-action
https://www.jit.io/resources/appsec-tools/the-developers-guide-to-using-gitleaks-to-detect-hardcoded-secrets
https://github.com/gitleaks/gitleaks

pre commit for uv-secure

Add Pro instructions for 
- Rebase ?? (complicated)
- Squash  (maybe easier ?)

repos:
  - repo: local
    hooks:
      - id: uv-secure
        name: uv-secure (Security Audit)
        entry: uvx uv-secure
        language: system
        # Only run if the lockfile or pyproject changes to save time
        files: ^(uv\.lock|pyproject\.toml)$
        pass_filenames: false
        always_run: false