# Contributing to Job

English | [简体中文](CONTRIBUTING.zh-CN.md)

Contributions can improve teaching, resume reasoning and layout, reproducible tooling, tests, or documentation. Start with an issue for substantial behavior changes; small focused fixes can go directly to a pull request. Use either English or Chinese for discussion.

## Working on a change

1. Fork and clone the repository; use a branch for your change. Read [AGENTS.md](AGENTS.md). Skill source lives only in `skills/`.
2. Use synthetic JD inputs and fictional resume facts in temporary directories. Do not modify real bases or publish showcase repositories as a test side effect.
3. Describe the concrete problem, resulting behavior, and actual validation in your PR. For teaching changes, include an input and a short before/after example; structure checks alone do not prove better teaching.
4. Run the checks below, inspect the staged diff and complete public history, and remove temporary files before submitting. Do not force-add ignored personal files.

## Checks

From the repository root, with Python 3.10+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_preferences.py config/preferences.example.yaml
.venv/bin/python -m unittest discover -s scripts/tests
python3 -m unittest discover -s skills/jd-interview-prep/scripts/tests
python3 scripts/check_public_tree.py
```

If you have personal settings, also run `.venv/bin/python scripts/validate_preferences.py`. Review their meaning privately; never attach them verbatim to an issue. The public-tree check reads the Git index; stage reviewed public changes before using it as a pre-commit check. CI checks the committed tree. It catches known private paths and local home paths, not all possible personal data or secrets.

For resume content/layout or rendering changes, install `skills/bilingual-resume/scripts/requirements.txt` and system Google Chrome. Render synthetic English/Chinese HTML with the skill's renderer, check one-page A4 and extracted text, then inspect both pages visually. Source-path-only changes do not require re-rendering personal resumes.

For skill behavior changes, test representative requests independently: default settings, an explicit override, and continuation after settings change. Cite the instruction or output that supports the observed choice. Do not report unexecuted project tests or model integrations as passing. Existing pack checks accept English and Chinese mapping vocabulary.

## Documentation and preferences

English is the canonical language for `AGENTS.md`, skill instructions, and execution references. Keep `README.md`/`README.zh-CN.md` and both contribution guides semantically aligned, including commands and paths. Do not add a second automatically loaded instruction translation. Request/output languages remain independent of documentation language.

Add user settings only when they serve an actual task. Update the public example, validator, tests, and both README files together when the configuration contract changes. Use module `notes` for natural-language preferences; do not build a growing enum for every writing choice. Current instructions and confirmed case settings still take precedence.

## Privacy and examples

Keep personal preferences, `Resume/private/`, real preparation packs, and resume variants out of commits, issues, logs, and screenshots. Do not submit real employer-confidential inputs or credentials. Public examples must be deliberately synthetic and reviewed in `examples/`; do not unignore your private output directory to share one. Preserve existing user edits and all source-read-only boundaries.

Contributed original code and documentation use the repository's [MIT license](LICENSE). Identify any third-party material and its license so it can be reviewed before inclusion.
