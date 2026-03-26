# AIS DEVIL 😈Power Smoothie Maker: 😼CI Edition

Welcome to the **AIS Power Smoothie Maker: CI Edition**! Ready to automate your blending process?
This exercise will guide you through setting up a Continuous Integration pipeline, showing you why 
automated testing is crucial and how GitHub Actions can ensure your smoothie shop runs smoothly by 
catching bugs before they hit the blender.

Maximising your learning effect: Copy & paste the code snippets in this exercise, but make sure to 
READ THROUGH the code snippets carefully and slowly. Understanding what you are pasting is key to 
a great learning experience. If you want to go one step further, then explain the code you've pasted
to your peer (or to an imaginary rubber duck 🐥 in case you work alone).

## 🛫 Getting Started

We will build upon the `final` codebase of the previous exercise.

### 1. Fork the Repository

‼️You've already forked this repository before. We, however, want to start with a completely fresh 
fork to ensure that no previous configurations interfere with our CI setup. 

1. In your previous fork (`https://github.com/<YOUR USERNAME>/ais-dev2il-ais-power-smoothie-maker`), go to **Settings / General** and scroll 
down to the **Danger Zone**. Now hit **Leave fork network**.
2. Let's fork fresh! Go to [https://github.com/peterrietzler/ais-dev2il-ais-power-smoothie-maker](https://github.com/peterrietzler/ais-dev2il-ais-power-smoothie-maker)
and fork the repository. Change the name to `ais-dev2il-ais-power-smoothie-maker-ci` and change the description to 
"Reliable smoothie blending using CI".
**Important**: Uncheck "Copy the `main` branch only". We need the `final` branch!
3. Now redo step 1 with the new repo in order to make it independent.

> Forking creates a personal copy of someone else's project on your own 
> GitHub account, allowing you to freely work on it without requiring 
> access rights to the original repository. This is especially important  
> in open source development! Everybody can start contributing right away to 
> open-source projects completely independent of the original repository. 
> You can then create pull requests that merge the code back into the
> original repository.

### 2. Prepare Your Branch
We want to bring the code from the `final` branch into our `main` branch so we can start building the CI pipeline on top of it.

1. Clone your repository and open it in PyCharm.
2. Ensure you are on the `main` branch:
   ```bash
   git checkout main
   ```
3. Merge the `final` branch into `main`:
   ```bash
   git merge origin/final
   ```
4. Push the changes to `main`:
   ```bash
   git push
   ```

Now your `main` branch is ready to go!

---

## 🧪 Building a Basic CI Pipeline

### 🎯 Goal

We want to ensure that every change to our code is automatically tested. By the end of this exercise, you will have a fully automated CI pipeline that:
1. Runs tests on every push 
2. Have Chuck Norris protecting your `main` branch from broken code
3. Checks code quality (Level Up)
4. Provides test reports (Level Up)

### Step 1: Create the Workflow File

GitHub Actions looks for workflow definitions in the `.github/workflows` directory.
Create the file: `.github/workflows/ci.yml`.

### Step 2: Define Triggers
We want the pipeline to run whenever code is pushed to the `main` branch or when a Pull Request is opened against `main`.

Add the following to your `ci.yml`:

```yaml
name: CI

on:
  # Run on pushes to the main branch
  push:
    branches: [ "main" ]
  # Run on pull requests targeting the main branch
  pull_request:
    branches: [ "main" ]
```

### Step 3: Define the Test Job

Now, let's define the job that runs the tests. We need to:
1. Check out the code.
2. Install `uv` on the build agent.
3. Install Python.
4. Install dependencies.
5. Run the tests.

Append this to `ci.yml` (probably copy, paste & read through carefully is a good choice here):

```yaml
jobs:
  test:
    name: Build & Test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    # Install uv
    - name: Install uv
      uses: astral-sh/setup-uv@v5
      with:
        # Enables caching of uv's virtual environments between runs.
        enable-cache: true

    # Set up Python using the .python-version file
    - name: Set up Python
      run: uv python install

    # Install dependencies
    - name: Install the project
      run: uv sync --frozen

    # Run tests
    - name: Run tests
      run: uv run pytest
```

**Let's break down what's happening here:**

`uses: actions/checkout@v4`: This is a standard GitHub Action that retrieves your code so the runner can work with it. You can find the documentation 
of the action at https://github.com/actions/checkout.

`uses: astral-sh/setup-uv@v5`: This action sets up `uv` on the build agent. You can find the documentation at
https://github.com/marketplace/actions/astral-sh-setup-uv

`enable-cache: true`: This caches `uv`'s virtual environment. If your dependencies haven't changed, 
the pipeline reuses the previous environment instead of downloading everything again. This speeds up 
your feedback loop significantly!

`run: uv python install`: Ensures the correct Python version (from your `.python-version` file) is ready. 
This runs the CLI command exactly as you would run it locally.

`uv sync --frozen`: Installs your project dependencies. The `--frozen` flag is crucial for CI: it ensures we 
install **exactly** the versions specified in `uv.lock`, guaranteeing that what we test is identical to what 
we built locally.

`uv run pytest`: No more explanations needed here, right? 

💡 GitHub comes with of a lot of built in actions. You can go to https://github.com/actions to explore them. There's
also a marketplace of further actions available at https://github.com/marketplace?type=actions.

⚠️ The actions that you use are **executed** on the build agents. This means that they can do things there, 
including accessing secrets, modifying files, etc. Always ensure that you trust the actions you use!

Commit and push your changes. The action starts running immediately! Go to the **Actions** tab to see it in action.
Take a couple of minutes and do a dive into the logs. Explore the different steps and understand what is happening.

Make a test fail (e.g., change an expected value in `test_main.py`), commit and push your changes and see
what happens. After you did this, it might also be the right time to check your mailbox ;)

### Step 4: Protect the Main Branch

> **Fact:** Chuck Norris protects his `main` branch with a roundhouse kick. Mere mortals like us use GitHub branch protection rules instead.

1. Go to **Settings** -> **Branches**.
2. Click **Add branch protection rule**.
3. **Branch name pattern**: `main`.
4. Check **Require a pull request before merging**.
   - Check **Require approvals** and require 1 approval.
5. Check **Require status checks to pass before merging**.
   - Search for `Build & Test` (the name of our job) and select it.
5. Check **Require branches to be up to date before merging**.
6. Check **Do not allow bypassing the above settings**.
6. Click **Create**.

Now, nobody (including you!) can push directly to `main` anymore. 
In order to be able to merge, you need to 
- create a new branch to work on
- merge all recent changes from `main` and solve conflicts
- create a pull request
- have the last commit on your branch successfully pass all the test
- have an approval from at least one team mate on your pull request

This ensures that our trunK is always safe and sound!

### 🚀 Level Up

Basic testing is great, but we can do better. Let's add code linting, test reports, and more triggers.

### Challenge 1: Smooth out the Ruff edges (Linting)

Linting checks for stylistic errors and bugs. We can use `ruff` for this. It is an extremely fast Python linter 
and code formatter. It's become the industry standard due to its speed and comprehensive rule set. 
You can find the documentation at [https://docs.astral.sh/ruff/](https://docs.astral.sh/ruff/).

Try it out on your local machine first: 
```bash
uvx ruff check .
```

> `uvx` acts like a temporary runner. Instead of installing `ruff` permanently into your project, 
> `uvx` downloads it on-the-fly, runs it in an isolated environment, and then discards it. This keeps your 
> project clean and lightweight

It should show you something like "All checks passed!".

🛑 Something didn't pass? 

🎨 Fix the liniting problems until everything is green! 🟩

If everything works fine out of the box, try to introduce a linting error (e.g., an unused import or an unused variable) and see how 
`ruff` catches it. (You can keep the change, so that we can see how this integrates with our CI pipeline)

Update your `ci.yml`. Add this step **before** the "Run tests" step:

```yaml
    # Check code formatting and lint
    - name: Check code
      run: uvx ruff check . --output-format=github
```

> The `--output-format=github` flag is magic! It formats the errors so GitHub can read them. 
> This means you'll see the linting errors directly annotated in the action summary on GitHub, not just in the logs.

Now, **commit and push** your changes. 
Since you added a linting error earlier, your pipeline should **fail**! 🛑
Go to the **Actions** tab, examine the failure, and see how Ruff reports the issue (check the logs and the summary).

Once you've seen the error, **fix the code** in PyCharm, push again, and watch the pipeline turn green! 🟢


> **Pro Tip 1:** Do you want even faster feedback ? PyCharm inspects your code as you type and highlights linting issues in real-time. Just 
> open _Problems_ view, select the _File_ tab, open `main.py` and see how PyCharm shows you issues immediately! You can even configure it to 
> use `ruff` as the linter. Add `ruff` as dev dependency to your project open the PyCharm settings, search for "Ruff", enable it and see how
> it integrated with the _Problems_ view.
> 
> **Pro Tip 2:** Tired of arguing about tabs vs. spaces or where to put that curly brace? Let the robot decide! 🤖 
> Ruff isn't just a critic; it's a cleaner. Run `uvx ruff format .` to instantly beautify your code.
> Even better: Configure PyCharm (Settings -> Tools -> Ruff) to use Ruff for formatting. Then, hit `Cmd + Option + L` (macOS) 
> or `Ctrl + Alt + L` (Windows/Linux), and watch your code align itself perfectly. Peace in our time! 🏳️

### Challenge 2: Serve Digestible Results (Test Reporting)

"_Reading Logs is like Chewing on Kale Stems_". Let's produce a nice summary of test results!

1. Update the "Run tests" step to generate a JUnit report:

```yaml
    # Run tests
    - name: Run tests
      run: uv run pytest --junitxml=junit.xml
```

This is going to create a file called `junit.xml` containing your test results. It's a standard format understood by many CI tools.

2. Add this step to publish a test summary **after** the "Run tests" step:

```yaml
    # Show test results in a developer friendly way
    - name: Create test result summary
      uses: test-summary/action@v2
      with:
        paths: "junit.xml"
      # ensure this runs even if tests fail
      if: always()
```

This action reads the `junit.xml` file and creates a nice summary of the test results, which you can view directly 
in the GitHub Actions UI.

Make one of your tests fail (e.g. by changing an expected value), commit and push your changes - and see how 
the action reports your results in a digestible way!

💡 Note that this is just a very simple way of reporting test results. There are many more advanced ways of doing this. You can e.g. 
generate HTML reports, append failing test results to pull requests, etc. You can explore the [marketplace](https://github.com/marketplace/actions) 
for more actions and possibilities to find something that fits your needs.

### Challenge 3: Midnight Blending & On-Demand Cravings (Schedules & Manual Triggers)

Sometimes you want to run tests on a schedule (Nightly builds) or manually.

Update the `on` section at the top of `ci.yml` to include `schedule` and `workflow_dispatch`:

```yaml
on:
  # Run on pushes to the main branch
  push:
    branches: [ "main" ]
  # Run on pull requests targeting the main branch
  pull_request:
    branches: [ "main" ]
  # Run every night at midnight UTC
  schedule:
    - cron: '0 0 * * *'
  # Allow developers to manually trigger the workflow from the GitHub Actions tab
  workflow_dispatch:
```

Commit your changes. You can now manually trigger the workflow from the **Actions** tab!

GitHub will also run the workflow every night at midnight UTC. If you want to see it in action right now, 
change the schedule to `*/5 * * * *`, which runs the workflow every 5 minutes (the minimum interval allowed 
by GitHub). After testing, remember to set it back to `0 0 * * *` to avoid excessive runs!

## 🛡️ Security Scans

Running tests is good, but is your code **secure**?
Modern applications rely on hundreds of external libraries. If one of them has a known vulnerability, 
hackers can exploit it. Also, we often accidentally leave "secrets" (API keys, passwords) in our code.

Let's automate the detection of these issues!

### Dependency Scanning with `uv-secure`

We use `uv-secure` to check if any of our dependencies have known security vulnerabilities (CVEs).

You can find the documentation at [https://github.com/owenlamont/uv-secure](https://github.com/owenlamont/uv-secure). 

⚠️ At the time of writing (January 2026), `uv-secure` is still in early development. It's a nice tool that makes it 
very easy to scan for vulnerabilities. We are going to use it here for educational purposes. However, for production use cases, 
consider using more established tools like pip-audit, snyk or Safety. 

#### 🧪 Experiment Locally

Let's reduce our tryout cycle lead time and start to experiment locally. Run
```bash
uvx uv-secure
```
Hopefully, everything's fine! ✅ 

❓**What actually happened here?**
`uv-secure` didn't look at your code, but at your *ingredients* (`uv.lock`). It compared the versions of your libraries against a global database of known security vulnerabilities.

**But wait...** You probably saw some red output! 🚨 As times passes, new vulnerabilities are discovered. While this
exercise might have been safe in January 2026, it doesn't mean it will stay that way forever.

If you don't see any red output, let's introduce a vulnerability for demonstration purposes.
Add the dependency `flask==0.5` to your `pyproject.toml`. This is an old version of Flask with 
known security issues. Run `uv sync` to make sure that `uv.lock` is up to date and let's do the 
security check again 💥 **Boom!**

Let's commit this for now, so that we can see how this integrates with our CI pipeline.

#### Add 🛡to CI Pipeline

Add a new job to your `ci.yml` file to check for vulnerabilities:

```yaml
  scan:
    name: Security Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install
      
      - name: Scan for vulnerable dependencies
        run: | 
          set -o pipefail
          echo "### 🛡️ Security Audit Results" >> $GITHUB_STEP_SUMMARY
          echo '```text' >> $GITHUB_STEP_SUMMARY
          uvx uv-secure --config=pyproject.toml | tee -a $GITHUB_STEP_SUMMARY
          echo '```' >> $GITHUB_STEP_SUMMARY 
```

Push this change to GitHub and watch your pipeline run. You'll see a new "Security Checks" job!

❓What is `set -o pipefile` doing ? GitHub determines if a step fails based on the exit code of the last command 
in the `run` block. If you pipe your output, then `tee` is the last command, and it usually exits with `0` (success).
By setting `set -o pipefail`, we ensure that if `uv-secure` fails (exits with a non-zero code), the entire step is 
marked as failed.

💡Want to have more information on a CVE ? You can look it up on https://osv.dev. 

#### Fix the Vulnerability

In a real-world scenario, you should upgrade `flask` to a safe version.

However, sometimes you can't upgrade immediately (e.g. due to compatibility issues). 
In this case, you must **document** that you are aware of the risk and have accepted it.

Open `pyproject.toml` and add this configuration to ignore one specific vulnerability:

```toml
[tool.uv-secure.vulnerability_criteria]
# Ignores only this specific vulnerability ID (Flask issue)
ignore_vulnerabilities = ["PYSEC-2019-179"]
```

You can also ignore entire packages: 

```toml
[tool.uv-secure.ignore_packages]
# Ignores all vulnerabilities for Flask version 0.5
Flask = ["==0.5"]
```

Run `uvx uv-secure` again. It should now pass! ✅

> **Compliance Tip:** In regulated environments (like ISO 27001), you are required to document availability 
> of fixes and reasons for not applying them. Ignoring it in the config file and adding the reasons there 
> as comments effectively serves as this documentation.

### 🚀 Level Up: Secret Scanning

Committing secrets (passwords, tokens, keys) to git is a huge security risk. Once it's in the history, 
anyone with access to the repo can see it, even if you delete the file later.

We will use `gitleaks` (https://github.com/gitleaks/gitleaks) to scan our code for secrets.

#### Add Secret Scanning to CI

Update the `scan` job in `ci.yml` and add this step at the end of the `steps`list:

```yaml
      - name: Scan for secrets
        uses: gitleaks/gitleaks-action@v2
        if: always()
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**What is `GITHUB_TOKEN` ?**: `GITHUB_TOKEN` is a special authentication token provided by GitHub Actions 
that allows the workflow to interact with the GitHub API. `gitleaks-action` uses it to comment on your 
pull requests (you can find more information [here](https://github.com/gitleaks/gitleaks-action?tab=readme-ov-file#environment-variables)). 
`GITHUB_TOKEN` is automatically created for each workflow run and has limited default permissions, which 
do dot include the permission to commont on pull requests. You therefore need to update the `scan` job in `ci.yml`
and grant this permission:
   ```yaml
     scan:
       name: Security Checks
       runs-on: ubuntu-latest
       permissions:
         pull-requests: write
       steps:
        ...
   ```

💡You can find more information on `GITHUB_TOKEN` and permissions [here](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).


Now let's leak a secret

1. Add a "fake" secret to `main.py`. For example:
   ```python
   my_secret = "hyddYR1i2srLYdKa" 
   ```
2. Commit and push.
3. 🛑 Watch the CI pipeline fail! Inspect the summary page and also your pull request. 

#### How to fix it?

Your secret has just leaked. To be 100% secure, you must assume that
it has been compromised and you need to rotate it (change it).

You, however, need to make sure that our pipeline passes again. Note that gitleaks won't just 
look at your latest commit, but also at the history. It will inspect all commits in your branch, 
so just removing the secret and committing again is not enough.

#### **Scenario A**

You've rotated the secret and it's okay that the secret stays in the history (not recommended, but sometimes necessary).

Follow the instructions, that the gitleaks action added to your pull request.

#### **Scenario B**

You've rotated the secret and you want to completely remove it from the git history (recommended). You have two options

##### Option Easy: Squash everything

This approach combines all your commits (the bad one and the fix) into a single, clean commit. Easy, but you **lose** all your previous 
commits on the branch.

1. Remove the secret from your code in `main.py`.
2. Commit the fix
   ```bash
   git add main.py
   git commit -m "Remove secret"
   ```
   Now you have a history that looks like: "... -> Add Secret -> Remove Secret". The secret is still in the history!
3. Reset to main (soft):
   This command moves the branch pointer back to `main`, but keeps all your changes in the staging area.
   ```bash
   git reset --soft main
   ```
4. Commit again
   Now create a fresh commit. Since the files in your working directory essentially contain "Code + Secret - Secret", the secret is gone!
   ```bash
   git commit -m "Add feature (clean)"
   ```
   Your branch now has a single commit, without the secret in the history.
5. Force Push
   Overwrite the history on the server
   ```bash
   git push --force
   ```

##### Option Hard: Rewrite History

If you want to keep your individual commits but just extract the secret from that one specific commit, you would need to use `git rebase -i`.
This is an advanced Git topic and out of scope for this exercise.

### 🚀 Level Up: Pre-commit Hooks

Fixing pipelines is slow. Waiting for the server to tell you "You failed" is annoying.
What if we could check for secrets and issues **before** we even commit?

Enter `pre-commit`. It's a framework that runs checks (hooks) before git allows you to make a commit.

#### Avoid Leakage of Secrets as Best as Possible

_"That ship has sailed."_ (or _"Das Kind ist in den Brunnen gefallen"_, as we say in German).
You've seen what a mess it is, once a secret is committed. Wouldn't it be better to avoid this in the first place?

A **pre-commit** is a mechanism (specifically a Git hook) that automatically runs checks on your code **before** a commit is finalized 
in your history. Think of it as a local gatekeeper:
- It runs locally: When you type `git commit`, the configured hooks run immediately on your machine.
- It blocks bad code: If a check fails (e.g., a secret is detected or code style is wrong), the commit is aborted.

Let's set this up to avoid that secrets don't even make it into git! 

Create a file named `.pre-commit-config.yaml` in the root of your project:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.0
    hooks:
      - id: gitleaks
```

We need to install the hook. This is a one-time setup per clone of the repository and must be done
manually (bye, bye 0-configuration 😢):
```bash
uvx pre-commit install
```
You should see: `pre-commit installed at .git/hooks/pre-commit`.

#### 3. Try it out!
Try adding the fake secret to `main.py` again and try to commit:
```bash
git add main.py
git commit -m "Add secret"
```

💥 **BAM!** The commit is blocked! Gitleaks caught you locally. No need to wait for CI.
Remove the secret and try committing again. It works!
