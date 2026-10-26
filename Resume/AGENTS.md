# Resume workflow

- Load [the workspace rules](../AGENTS.md) first if needed, including active user preferences. Follow [bilingual-resume](../skills/bilingual-resume/SKILL.md).
- Read base and reference paths supplied by the user or configured under `resume`. `private/` is a local-only place for these files, not a required source database. With no base, use supplied real experience; never use configuration examples as facts.
- Respect the configured primary source language when present; otherwise resolve factual conflicts with the user rather than treating one language as inherently authoritative. Bases and original reference PDFs stay read-only unless base maintenance is explicitly requested.
- Write variants to `variants/<case-id>/`; reuse the JD case-id on handoff. Read `changes.md`, confirmed settings, and user edits before resuming. Do not reset a variant from its base.
- Produce matching English and Chinese HTML/PDF using the skill's renderer. Each PDF must pass the one-page A4, extracted-text, and visual checks. See the root README for dependencies and commands.
- Private source files, variants, and version records stay local. Run tests with temporary synthetic facts, not real resume sources.
