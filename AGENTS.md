# Job workspace

Paths in this file are relative to the repository root. Skill source lives only in `skills/`.

## Routing and outputs

- For interview preparation, read [JD/AGENTS.md](JD/AGENTS.md). For resume work, read [Resume/AGENTS.md](Resume/AGENTS.md). Both skills also work independently outside this workspace.
- A complete JD workflow in this workspace produces `JD/preparations/<case-id>/`, then hands off to the resume skill for `Resume/variants/<same-case-id>/`. `resume.enabled: false` or an explicit interview-only request skips the handoff. Disabling the showcase does not disable teaching or resumes.
- If resume input is missing, finish the interview work and request the needed real experience; do not invent facts or mark the resume complete. Standalone resume work does not generate a preparation pack.
- User-specified modes and paths take precedence. Resume sources are read only when needed for resume work; they do not change the default beginner teaching approach.

## User preferences

If `config/preferences.yaml` exists, validate it with the Python environment that has `requirements-dev.txt` installed (see the commands in [README.md](README.md)), then read it before making task choices. See [the optional template](config/preferences.example.yaml) for supported fields. Never use the example as active settings. With no file, use the public defaults below. Resolve configured paths relative to this repository root, even though the YAML file lives in `config/`.

- `language: auto` follows the current request language. `frontend: auto` and `backend: auto` leave technology selection to the JD and project needs; `prefer_config` only overrides a JD framework when a concrete frontend is configured. `showcase.enabled: false` skips implementation and all showcase publication; validate that pack with `--no-project`. `resume.enabled` controls the connected JD handoff, not an explicit standalone resume request.
- New tasks: current user instructions, then loaded preferences, then public defaults.
- Continuations: current user instructions, then the task's confirmed settings and user edits, then preferences, then public defaults. Read the preparation pack's `meta/progress.md` or the resume's `changes.md` first. Changing the preference file must not silently change an existing task's stack, sources, or publication target.
- Only edit the preference file when the user explicitly asks to save a preference. One-off task instructions do not change it. Record settings actually used in the task's existing progress record, rather than copying the whole private configuration.
- Unknown or invalid settings are errors, not silently ignored options. Continue independent work while clarifying the affected choice. Preferences cannot turn examples into personal experience, remove JD learning coverage, or replace required verification.
- Outside this workspace, skills consume preferences explicitly supplied by the user or an already loaded workspace; never discover personal settings by walking from the skill installation path.

## Public defaults and boundaries

- Preparation language follows the user's request unless specified. Resume output remains a matching English/Chinese pair. Public documentation is maintained in English; the README and contribution guide have Chinese translations.
- Choose showcase technology from the JD and project needs. Preferred stacks may be supplied in YAML. `frontend_policy: prefer_jd` keeps explicit JD technology first; `prefer_config` uses the configured frontend even when the JD names another stack. Cover the JD's actual technology in teaching and QA in either case. A backend preference applies when the JD leaves the backend open; a current explicit user choice takes precedence.
- Build showcases locally by default. Only publish when the user or loaded settings explicitly selects `public` or `private`. `pages` defaults to `true` for suitable static demos after publication is enabled; `false` disables deployment. For private source, `pages: true` alone does not authorize a public site: verify the site audience using the [publication workflow](skills/jd-interview-prep/references/github-workflow.md). Confirm the authenticated owner and exact target before publishing. Keep the showcase in its own repository.
- Read only user-provided or configured resume sources. Maintain facts in the base documents, not a separate fact database. Bases and reference PDFs are read-only unless the user explicitly requests base maintenance. Generated projects require confirmed personal participation before they can become resume experience.
- Real resumes, JD inputs, learning packs, task records, and personal settings remain local. Only reviewed, deliberately public source, documentation, and synthetic examples belong in this repository. Publication of this repository does not authorize publication of private task outputs.

## Checks and contributions

Use the commands in [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md). Pack structure is checked by `validate_pack.py`; PDF output requires the resume renderer plus text and visual inspection. Structure checks do not prove teaching quality, project behavior, or publication. Test changes with temporary synthetic inputs, and remove temporary outputs after verification. Skill maintenance does not itself create real preparation packs, resumes, or showcase repositories.
