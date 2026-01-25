# AIS DEVIL 😈Power Smoothie Maker: 😼CI Edition

Welcome to the **AIS Power Smoothie Maker: CI Edition**! Ready to automate your blending process?
This exercise will guide you through setting up a Continuous Integration pipeline, showing you why 
automated testing is crucial and how GitHub Actions can ensure your smoothie shop runs smoothly by 
catching bugs before they hit the blender.

Maximising your learning effect: You are going to use PyCharm in this exercise. PyCharm has excellent 
code completion features that will help you a lot. If you type and use the code completion instead of 
copy & pasting  everything, your brain will grasp it deeper and you thus have a better learning experience.
You can also always use `CTRL + SPACE` to trigger code completion at your current cursor position.

## 🛫 Getting Started

We will build upon the `final` codebase of the previous exercise.

### 1. Fork the Repository

‼️You've already forked this repository before. We, however, want to start with a completely fresh 
fork to ensure that no previous configurations interfere with our CI setup. 

1. In your previous fork (https://github.com/<<YOUR USERNAME>>/ais-dev2il-ais-power-smoothie-maker), go to **Settings / General** and scroll 
down to the **Danger Zone**. Now hit **Leave fork network**.
2. Let's fork fresh! Go to [https://github.com/peterrietzler/ais-dev2il-ais-power-smoothie-maker](https://github.com/peterrietzler/ais-dev2il-ais-power-smoothie-maker)
and fork the repository. Change the name to `ais-dev2il-ais-power-smoothie-maker-ci` and change the description to 
"Reliable smoothie blending using CI".
**Important**: Uncheck "Copy the `main` branch only". We need the `final` branch!

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

Now, nobody (including you!) can push directly to `main` without first merging `main` into the branch, 
passing tests and a review.

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
It should show you something like "All checks passed!".

Try to introduce a linting error (e.g., an unused import or an unused variable) and see how 
`ruff` catches it. Keep the change, so that we can see how this integrates with our CI pipeline. 

> **Note:** `uvx` acts like a temporary runner. Instead of installing `ruff` permanently into your project, 
> `uvx` downloads it on-the-fly, runs it in an isolated environment, and then discards it. This keeps your 
> project clean and lightweight

Update your `ci.yml`. Add this step **before** the "Run tests" step:

```yaml
    # Check code formatting and lint
    - name: Check code
      run: uvx ruff check . --output-format=github
```

> **Tip:** The `--output-format=github` flag is magic! It formats the errors so GitHub can read them. 
> This means you'll see the linting errors directly annotated in the action summary on GitHub, not just in the logs.

Now, **commit and push** your changes. 
Since you added a linting error earlier, your pipeline should **fail**! 🛑
Go to the **Actions** tab, examine the failure, and see how Ruff reports the issue (check the logs and the summary).

Once you've seen the error, **fix the code** in PyCharm, push again, and watch the pipeline turn green! 🟢

> **Pro Tip 1:** Do you want even faster feedback ? PyCharm inspects your code as you type and highlights linting issues in real-time. Just 
> open _Problems_ view, select the _File_ tab, open `main.py` and see how PyCharm shows you issues immediately! You can even configure it to 
> use `ruff` as the linter. Add `ruff` as dev dependency to your project open the PyCharm settings, search for "Ruff", enable it and see how
> it integrated with the _Problems_ view.

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