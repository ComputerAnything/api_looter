# GitHub Actions Workflows

Automated security scanning and validation for every pull request.

---

## Table of Contents

- [Overview](#overview)
- [Workflow Files](#workflow-files)
- [PR Validation Workflow](#pr-validation-workflow)
- [Security Scanning Workflow](#security-scanning-workflow)
- [Dependabot Configuration](#dependabot-configuration)
- [Local Testing](#local-testing)

---

## Overview

This project uses **GitHub Actions** for continuous integration and security:

- ✅ **PR Validation** - Runs on every pull request
- ✅ **Security Scanning** - Weekly automated scans
- ✅ **Dependency Updates** - Dependabot auto-creates PRs for updates
- ✅ **Secret Detection** - Prevents accidental credential commits

---

## Workflow Files

### Location

All workflows are in `.github/workflows/`:

```
.github/
├── workflows/
│   ├── validate-pr.yml       # PR validation (runs on every PR)
│   └── security.yml           # Weekly security scans
└── dependabot.yml             # Dependency update config
```

### Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `validate-pr.yml` | Pull requests to `main` | Validate API changes, check security |
| `security.yml` | Weekly schedule (Monday 9 AM UTC) | CodeQL analysis, Snyk scanning |
| Dependabot | Weekly (Monday) | Auto-update dependencies |

---

## PR Validation Workflow

**File:** `.github/workflows/validate-pr.yml`

### What It Does

Every PR is automatically checked for:

1. **API Validation** - Runs `validate_apis.py`
   - ✅ HTTPS endpoints
   - ✅ No localhost/private IPs
   - ✅ All required fields present
   - ✅ Educational fields filled
   - ✅ No security issues

2. **Code Linting** - Runs Ruff
   - ✅ PEP 8 compliance
   - ✅ Unused imports
   - ✅ Code quality issues

3. **Security Scanning** - Runs Bandit
   - ✅ Python security issues
   - ✅ Hardcoded secrets
   - ✅ Unsafe function calls

4. **Secret Detection** - Runs TruffleHog
   - ✅ API keys leaked
   - ✅ Passwords in code
   - ✅ Private keys committed

### Workflow Configuration

```yaml
name: Validate Pull Request

on:
  pull_request:
    branches: [ main ]
    paths:
      - 'app/data.py'           # Only run if data.py changed
      - 'app/api_handlers.py'
      - 'app/**/*.py'
      - 'requirements.txt'

jobs:
  validate-apis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run API validation
        run: |
          python validate_apis.py
```

### When PR Checks Fail

**If validation fails:**

1. Check the workflow run logs in GitHub Actions
2. Fix the issues locally:
   ```bash
   python validate_apis.py
   ```
3. Commit and push the fixes
4. PR checks will re-run automatically

**Common failures:**

- ❌ **HTTP endpoint** - Change to HTTPS
- ❌ **Missing field** - Add `why_use`, `how_use`, etc.
- ❌ **Invalid endpoint** - Check domain is reachable
- ❌ **Localhost URL** - Use public API endpoint

---

## Security Scanning Workflow

**File:** `.github/workflows/security.yml`

### What It Does

**Runs weekly (Monday 9 AM UTC):**

1. **CodeQL Analysis**
   - Static code analysis
   - Detects security vulnerabilities
   - Supports Python, JavaScript

2. **Snyk Scanning** (if configured)
   - Dependency vulnerability scanning
   - Checks for known CVEs
   - Suggests fixes

3. **Container Scanning** (production)
   - Scans Docker images
   - Checks base images for vulnerabilities

### Workflow Configuration

```yaml
name: Security Scanning

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Mondays at 9 AM UTC
  workflow_dispatch:      # Manual trigger

jobs:
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

### Manual Trigger

You can manually run security scans:

1. Go to **Actions** tab in GitHub
2. Select **Security Scanning** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow**

---

## Dependabot Configuration

**File:** `.github/dependabot.yml`

### What It Does

Automatically creates PRs for:

- ✅ **Python dependencies** (requirements.txt)
- ✅ **GitHub Actions** (workflow files)
- ✅ **Docker** (base images)

### Configuration

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3
```

### Handling Dependabot PRs

**When Dependabot creates a PR:**

1. **Review the changes** - Check what's updated
2. **Check for breaking changes** - Read the changelog
3. **Test locally** (optional):
   ```bash
   # Checkout the PR branch
   gh pr checkout <PR-number>

   # Test the app
   pip install -r requirements.txt
   python run.py
   ```
4. **Merge if safe** - Dependabot PRs are usually safe to merge

**Auto-merge minor updates:**

You can enable auto-merge for patch/minor updates:

```bash
# In PR, run:
gh pr merge --auto --squash
```

---

## Local Testing

### Run Validation Locally

Before pushing, test validation locally:

```bash
# Validate APIs
python validate_apis.py

# Should output:
# ✅ Validation passed!
# Total APIs: 14
# All APIs meet security requirements
```

### Run Linting Locally

```bash
# Install ruff
pip install ruff

# Check for issues
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

### Run Security Scan Locally

```bash
# Install bandit
pip install bandit

# Scan for security issues
bandit -r app/ -f screen

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json
```

### Check for Secrets Locally

```bash
# Using TruffleHog (requires Docker)
docker run --rm -v "$PWD:/path" trufflesecurity/trufflehog:latest filesystem /path --only-verified

# Using git-secrets (alternative)
git secrets --scan
```

---

##CI/CD Best Practices

### For Contributors

1. **Always run validation locally first:**
   ```bash
   python validate_apis.py
   ```

2. **Test your changes:**
   ```bash
   python run.py
   # Visit http://localhost:8000 and test
   ```

3. **Keep PRs focused:**
   - One API per PR
   - Don't mix API additions with refactoring

4. **Watch for CI failures:**
   - Check GitHub Actions logs if PR fails
   - Fix locally and push again

### For Maintainers

1. **Review Dependabot PRs weekly**
   - Don't let them pile up
   - Test major version updates

2. **Monitor Security Scanning results**
   - Check for new vulnerabilities
   - Address critical issues within 7 days

3. **Keep workflows updated**
   - Update action versions quarterly
   - Test workflow changes in branches first

---

## Workflow Badges

Add these badges to `README.md`:

```markdown
![Validate PR](https://github.com/ComputerAnything/api_looter/actions/workflows/validate-pr.yml/badge.svg)
![Security Scan](https://github.com/ComputerAnything/api_looter/actions/workflows/security.yml/badge.svg)
```

---

## Troubleshooting

### Workflow Not Running

**Check:**
- Is the file in `.github/workflows/`?
- Is the YAML syntax valid? (use yamllint)
- Does the trigger match? (e.g., PR to `main`)
- Are workflows enabled in repository settings?

### Validation Failing

```bash
# See exact error in GitHub Actions logs
# Then run locally to debug:
python validate_apis.py

# Check specific API:
python
>>> from app.data import APIS
>>> print(APIS[14])  # Check API at index 14
```

### CodeQL Failing

**Common issues:**
- Code has actual security vulnerability → fix the code
- False positive → add `.github/codeql/codeql-config.yml` to exclude
- Action version outdated → update to latest

### Dependabot PRs Failing

**If Dependabot PR fails validation:**
1. Checkout the PR branch
2. Update the dependency manually
3. Test locally
4. Push to the PR branch (if you have permissions)
5. Or close the PR and create manual update

---

## Adding New Workflows

### Template for New Workflow

```yaml
name: Your Workflow Name

on:
  pull_request:
    branches: [ main ]

jobs:
  your-job:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Your step
        run: |
          echo "Do something"
```

### Testing New Workflows

1. Create in a feature branch
2. Open a test PR
3. Watch workflow run
4. Iterate until working
5. Merge to main

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)

---

*Last Updated: January 2026*
