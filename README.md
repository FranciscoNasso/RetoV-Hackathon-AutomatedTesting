# ExoHunter E2E — Automated Testing

This repository contains end-to-end tests for the ExoHunter frontend. Tests are written using:

- Playwright (browser automation)
- Behave (Gherkin BDD runner)
- Page Object Model (POM) under `src/pages`

The suite covers navigation (Explore/Download/Upload), downloading example CSVs, and uploading files to the prediction endpoint.

## Quick start — local (macOS / Linux)

1. Create and activate a Python virtualenv (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Install Playwright browsers (required for Playwright to run):

```bash
python -m playwright install --with-deps
# or if you prefer npm
# npx playwright install
```

4. Run the full Behave suite:

```bash
# run all features
behave

# or run a single feature
behave features/upload_file.feature
```

Notes:
- Tests use the synchronous Playwright API via a Behave `environment.py` fixture that exposes `context.page`.
- Some tests may perform network downloads from `https://exohunter.earth/` (example CSVs). If you are offline, the download steps may fallback to HTTP fetch; see the steps code for details.

## Project layout

- `features/` — Gherkin feature files and step implementations
   - `features/*.feature` — test scenarios
   - `features/steps/*.py` — step definitions
   - `features/environment.py` — Behave environment (Playwright setup)
- `src/pages/` — Page Objects (BasePage, HomePage, ExplorePage, DownloadPage, UploadPage)
- `src/utils/` — utilities (file helpers)
- `.github/workflows/ci.yml` — CI workflow (GitHub Actions)

## CI (`.github/workflows/ci.yml`) — summary

The repository includes a GitHub Actions workflow under `.github/workflows/ci.yml`. It runs on pushes and pull requests to `main`. The main steps are:

1. Checkout code (actions/checkout)
2. Setup Python (actions/setup-python)
3. Install dependencies from `requirements.txt`
4. Run Behave tests (the workflow currently runs with tags: `@smoke` and `@regression`)
5. Install Playwright browsers and optionally run Playwright tests (`npx playwright test`)

Below is a detailed explanation of the workflow and recommendations for improvements available in the README.

## Troubleshooting & tips

- If tests fail due to missing Playwright browsers: run `python -m playwright install` locally.
- If a test times out waiting for a selector, try running the test headful to observe behavior:

```bash
# run behave but keep browser visible — set HEADLESS=0 for environment or modify environment.py to launch headed
PLAYWRIGHT_HEADLESS=0 behave features/upload_file.feature
```

- Add an `after_scenario` screenshot capture in `features/environment.py` to collect evidence for failures.

## Next steps

- Add screenshot-on-failure and HTML capture to `features/environment.py`.
- Improve CI to cache Python deps and Playwright browsers to speed runs.
- Add an artifacts step to upload test results and screenshots to the workflow run.

Tell me which of these you'd like and I'll update the repo and re-run the tests.
# exohunter-e2e Automated Testing Project

This project is designed for automated testing of the ExoHunter website using Playwright, Behave, and the Page Object Model design pattern. The tests cover various user interactions, including exploring different pages, downloading files, and uploading files.

## Project Structure

```
exohunter-e2e
 features
 explore_pages.feature
 download_file.feature
 upload_file.feature
 environment.py
 steps
 explore_steps.py
 download_steps.py
 upload_steps.py
 src
 pages
 base_page.py
 home_page.py
 explore_page.py
 download_page.py
 upload_page.py
 utils
 file_helpers.py
 config.py
 .github
 workflows
 ci.yml
 .gitignore
 requirements.txt
 pyproject.toml
 README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd exohunter-e2e
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Tests**
   To execute the tests, use the following command:
   ```bash
   behave features/
   ```

## Usage Guidelines

- The `features` directory contains the Gherkin syntax files that define the test scenarios.
- The `src/pages` directory contains the Page Object Model classes that encapsulate the interactions with the web pages.
- The `src/utils` directory includes utility functions for file handling.
- The `.github/workflows/ci.yml` file defines the CI workflow for running tests automatically.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
