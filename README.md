# Job

English | [简体中文](README.zh-CN.md)

Turn a job description into an interview learning pack, and real experience into matching English/Chinese resumes. Job provides two independent agent skills and a workspace that can connect them. Contributions to teaching quality, reproducible examples, tooling, and documentation are welcome.

## Start here

1. Clone this repository and open it as your agent's workspace. Ask the agent to read [AGENTS.md](AGENTS.md). File access is required; screenshots need vision/OCR, source verification needs internet access, and project checks need the relevant runtime.
2. Optionally copy `config/preferences.example.yaml` to `config/preferences.yaml`. Edit only the settings you need. The personal file is ignored; the example never becomes active automatically.
3. For resumes, supply real experience or put your own bases/reference files in `Resume/private/` and configure their paths. No private files are included in the clone. Bases stay read-only unless you explicitly request maintenance.
4. Invoke a skill with one of the requests below. You can use any request language; preparation output follows that language unless configured otherwise. Resumes are always an English/Chinese pair.

| Workflow | Example request |
| --- | --- |
| Interview only | “Use $jd-interview-prep with this JD. Prepare me from the core concepts; do not update my resume.” |
| Resume only | “Use $bilingual-resume with my supplied experience and this JD. Generate matching English/Chinese resumes.” |
| Connected workflow | “Prepare fully for this JD and tailor both resume languages using my configured sources.” |

The skills are [jd-interview-prep](skills/jd-interview-prep/SKILL.md) and [bilingual-resume](skills/bilingual-resume/SKILL.md). Agents without automatic skill discovery can read these entrypoints and their relative references. You may install/copy each complete skill directory using your client's skill mechanism; do not assume a single entrypoint file contains all rules. Standalone skills use explicitly supplied settings and do not search this clone for personal data.

## What is public and what stays local

```text
Job/
├── AGENTS.md                       # Shared workspace rules
├── skills/                         # Canonical skill source, scripts, tests
├── config/
│   ├── preferences.example.yaml    # Public optional template
│   └── preferences.yaml            # Ignored personal settings
├── JD/preparations/
│   ├── README.md                   # Tracked directory guide
│   └── <case-id>/                  # Ignored learning packs
└── Resume/
    ├── private/                    # Ignored bases and reference materials
    └── variants/
        ├── README.md               # Tracked directory guide
        └── <case-id>/              # Ignored HTML/PDF and version records
```

A preparation pack has a root README, `artifacts/` (independent Essential, systematic KB, QA, and an optional showcase), and `meta/` (required JD, coverage, and progress records, plus conditional sources/handoff). Structure checks do not establish teaching depth or project correctness. The resume workflow uses confirmed facts, not tutorial answers or automatically generated project claims.

Showcases are built **locally by default**. Select `showcase.publish: public` or `private`, or explicitly request publication, to publish a separate showcase repository. `pages` defaults to `true` for suitable static demos after publication is enabled; set it to `false` to disable deployment. Pages does not host a backend. Private source does not guarantee a private site ([GitHub documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)): verify the audience first, and require explicit user authorization for a public demo before exposing private-source content publicly. Otherwise omit Pages or record it pending. Keep source visibility unchanged. Backend flows remain reproducible locally. Only reviewed showcase content is published, not the preparation pack or resume.

Private settings, sources, JD inputs, and outputs are ignored, including the standalone skills' default root-level `preparations/` and `resume-variants/` outputs. `.gitignore` does not remove files already committed or prevent force-adding them. The public-tree check rejects known private paths and local home paths; it is not a comprehensive personal-data or secret scanner. Review every contribution. Deliberately public examples must use synthetic facts and belong in a separately reviewed `examples/` contribution.

## Preferences

The [template](config/preferences.example.yaml) lists all supported settings. Paths are relative to the Job root. `language: auto` follows the request; a language tag such as `zh-CN` fixes preparation output. `resume.enabled` controls the connected JD-to-resume workflow, not explicit standalone resume requests.

`showcase.enabled: false` skips the project and all its publication while retaining teaching and any enabled resume handoff. `frontend: auto` and `backend: auto` mean no fixed stack preference; `prefer_config` needs a concrete frontend to override the JD.

`frontend_policy: prefer_jd` gives explicit JD technology priority. With `prefer_config`, the chosen frontend can differ from the JD; teaching and QA still cover the actual requirement. A preferred backend is used when the JD leaves the choice open. Free-text `notes` hold conditional or writing preferences. Preferences cannot remove factual or verification requirements.

For a new task, current instructions override preferences, which override public defaults. On continuation, the task's confirmed settings and user edits also take precedence over changed preferences. Only an explicit request to remember a preference updates the YAML. Do not store credentials or duplicate resume facts in it.

## Dependencies and checks

Use Python 3.10+ and Git. Keep dependencies outside private output directories; for example, from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_preferences.py
.venv/bin/python scripts/validate_preferences.py config/preferences.example.yaml
.venv/bin/python -m unittest discover -s scripts/tests
python3 -m unittest discover -s skills/jd-interview-prep/scripts/tests
python3 -m unittest discover -s skills/bilingual-resume/scripts/tests
python3 scripts/check_public_tree.py
```

The default preference check skips a missing personal file successfully; an explicitly supplied missing file fails. Configuration validation checks syntax/types/options, not the meaning of free-text policies. The pack validator needs only Python's standard library:

```sh
python3 skills/jd-interview-prep/scripts/validate_pack.py /absolute/path/to/pack
# Add --no-project when the user has disabled the showcase.
```

Resume rendering additionally needs system Google Chrome and the skill's dependencies:

```sh
.venv/bin/python -m pip install -r skills/bilingual-resume/scripts/requirements.txt
.venv/bin/python skills/bilingual-resume/scripts/render-pdf.py /absolute/path/to/resume.html /absolute/path/to/resume.pdf
```

The renderer replaces the destination only after a nonblank, exactly one-page A4 PDF passes its checks. `REVIEW` files diagnose failures and are not verified deliveries. Inspect extracted text and the visible pages in both languages before claiming completion. Optional features need their own project runtimes or authenticated GitHub access; cloning Job does not install them.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) ([中文](CONTRIBUTING.zh-CN.md)). English is the canonical language for executable instructions; the README and contribution guide are maintained in both languages. Documentation language does not force artifact language. License: [MIT](LICENSE).
