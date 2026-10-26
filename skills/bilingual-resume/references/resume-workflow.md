# Bilingual resume workflow and acceptance requirements

## 1. Inputs and responsibilities

Read the supplied experience, available base, and role input according to the current request and applicable workspace instructions. Ask only when consequential experience, contact details, or wording conflicts cannot be resolved from the supplied materials. Do not store personal experience in the skill. Apply preferences supplied by the user or an already loaded workspace; do not search for private configuration from the skill's installation path.

For new tasks, precedence is the current request, then supplied or loaded preferences, then public defaults. On continuation, the current request comes first, followed by the task's confirmed settings and user edits, then preferences, then defaults. Do not silently change an existing task because a preference file changed. Persist a preference only when the user explicitly requests it.

Role input may be a JD directly or a pack's `meta/resume-handoff.md`; a general resume does not require a target role. When using an existing handoff, read:

- the `case-id`, role source, requirement identifiers, and explanations;
- the locations and relevant sections of bilingual bases or user experience materials, and any additional sources;
- project evidence, actual participation, candidate wording, and unconfirmed details;
- preparation-pack and resume output paths, and existing progress.

Check handoff references first. Fill gaps from explicitly identified pack or workspace sources. If the JD is unreadable, separate confirmed information from gaps rather than inventing requirements. A missing handoff does not prevent independent use.

For explicitly requested base maintenance, update the specified bilingual HTML and corresponding PDFs without creating a case-id or role directory. Do not assume a target role when none is provided. Apply the same factual, layout, and verification requirements; report sources, changes, and checks in the delivery response without requiring a new `changes.md`. The following case-id and directory rules apply to derived role-specific and general versions.

## 2. Case-id, outputs, and continuation

When a preparation pack exists, reuse its directory name as the `case-id`; do not replace the role identifier with a broad career-direction label.

For an independent role-specific task, use `<company>-<role>-<YYYY-MM-DD>`, omitting an unknown company. For a general resume without a target role, use `resume-<YYYY-MM-DD>`. Remove path separators and other invalid filename characters, and use the user's timezone for the date. Create a new directory by default; resolve collisions with `-2`, `-3`, and so on rather than silently reusing another role's directory.

A full target directory supplied by the user or handoff takes precedence. If only an output root is given, create a case-id subdirectory within it; otherwise use applicable workspace instructions. With neither, create `resume-variants/<case-id>/` under the current working directory. Do not write to a private workspace inferred from the skill's installation location.

For continuation, reuse the existing directory, inspect artifacts and `changes.md` first, and change only what this task requires. Preserve confirmed settings and user edits instead of resetting from the base or newly changed preferences. If an existing directory's ownership is unclear, clarify before reusing it.

Derived deliverables:

```text
<case-id>/
├── resume-en.html
├── resume-en.pdf
├── resume-zh.html
├── resume-zh.pdf
└── changes.md
```

Original reference PDFs remain read-only. Derived versions must not overwrite bases, other versions, or user edits.

## 3. Evidence selection and factual wording

In a derived version's `changes.md`, locate evidence by source path and section, HTML region, or a necessary short quotation, and associate it with role requirement identifiers. Do not create a second factual inventory. For base maintenance, put this information in the delivery response instead. Retain existing JD identifiers; independent role tasks may create simple identifiers, while a general resume needs no role mapping.

Honor a source of truth designated by the user or workspace, such as an English base body with semantically synchronized Chinese. Without such a designation, do not choose authority solely by language. Identify and clarify conflicting fields while continuing unaffected work. The user's current explicit confirmation takes precedence. Newly confirmed facts apply to the derived version unless the user also requests base maintenance. Without a base, use the supplied real materials directly.

Select existing body content for relevance to the target role. When maintaining a base, incorporate newly confirmed facts into its body and synchronize the other language and corresponding PDFs. Do not hide additional experience in nonprinting comments.

Showcase code, tests, and publication records alone cannot prove personal contribution or business results. Include a project only within the scope of explicit, supported participation; writing it into the base also requires an explicit base-maintenance request. Otherwise list it as a candidate in `changes.md`, explain the missing facts, and continue generating from established experience. If base maintenance has no such file, explain the candidate in the delivery response.

Do not treat planned learning, model interview answers, desired exercise benefits, JD inferences, or unmeasured performance figures as experience. State job titles and employment dates factually. A target role may be expressed as a career objective, never disguised as a position held. Use confirmed experience-year conventions rather than incrementing years from the current date.

Preserve contribution and proficiency qualifiers such as "co-designed" or "basic," along with approximation marks, numerators and denominators, units, and measurement definitions. Do not infer an unknown personal share, comparison baseline, precise month, patent ordering, or business scale.

Apply the skill's coherent narrative to the summary, skill ordering, and key experience. Mechanisms and causal claims require evidence too. ATS review checks that names, dates, skills, and experience are ordinary DOM text with a sensible reading order. Successful extraction does not prove compatibility with every ATS.

## 4. English first and the Design System

Read available base HTML in each language first. Preserve language-specific CSS, fonts, and layout differences rather than replacing Chinese styling with English CSS. Existing design and explicit user preferences take precedence over the defaults below; use them to supply a missing language version. Retain content required by confirmed preferences, such as specified patents or sections, instead of deleting it merely to fit the page.

Default baseline:

| Dimension | Design requirement |
| --- | --- |
| Page | One A4 page, 210 × 297 mm; zero `@page` margin; content padding 14 mm top, 15 mm left/right, and 10 mm bottom; body line-height 1.36 |
| Fonts | English: `Inter, "Helvetica Neue", Arial, sans-serif`; Chinese: `"PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif`; use available fallbacks |
| Sizes | Name 24 pt; section headings 9.5 pt; body 10 pt; contact/date and other secondary details 9 pt; education 9.5 pt |
| Colors | Body `#1a2332`, secondary `#4a5568`, accent `#0f4c81`, divider `#d8dde3` |
| Sections | A 3 px dark-blue left border on headings, no underline; margins 8 px above and 4 px below; left padding 9 px |
| Structure | Single-column body; header contains only name and contact details, no separate role title; company and role share a line, with dates right-aligned; education appears later |
| Density | List-item bottom margin 1.5 px; experience/project bottom margin 8 px; skill-row vertical padding 3 px |
| Decoration | No portrait, icons, or large color blocks; compact skill alignment must preserve sensible text-extraction order |

The summary, skill order, key experience, and projects are priority tailoring areas, not the only editable areas. Other content may change when supported by facts. The implementation does not require special HTML comment markers.

Produce English HTML first, render and verify it, then create Chinese. Keep standard technical spellings. Chinese need not be a sentence-by-sentence translation, but scope, participation, dates, figures, project status, and causality must match. Check corresponding sections and key facts across languages.

One A4 page is an acceptance requirement. When content is too long, first remove early experience, project details, and repetition with low relevance to the target role, then tighten wording. Preserve the capability narrative, important facts, and explicit user requirements. Do not pass page-count checks through unreadable fonts, hidden text, or clipping.

## 5. HTML to PDF and verification

Use this skill's renderer:

```text
python3 <skill-dir>/scripts/render-pdf.py <input.html> <output.pdf>
```

The Python dependencies are listed in [scripts/requirements.txt](../scripts/requirements.txt). Install them in an available environment; no virtual environment inside the working directory is required. Prefer system Chrome and do not automatically download Playwright browsers. Honor an environment-provided runtime or explicitly specified browser first. If dependencies remain unavailable, identify the actual missing `playwright`, `pypdf`, or system Chrome component and available alternatives without claiming PDF verification passed.

The renderer returns 0 only for exactly one A4 page with extractable text, and replaces the target PDF only after successful verification. Failure preserves an existing target; do not present it as a successful new render. A reported `REVIEW` file is diagnostic only. Multiple pages, non-A4 geometry, empty extracted text, missing dependencies, and rendering errors are failures.

After machine checks, inspect the page image of each PDF separately for clipped edges, overlapping body text, footer overflow, missing glyphs, unusual line breaks, and readability. When available, use an applicable PDF skill for rendering review; otherwise use available PDF rendering or viewing tools. No particular plugin is mandatory. Text extraction alone cannot replace visual inspection.

Also check that extracted names, contact details, dates, key terms, and patents are complete, and that factual scope matches between languages. If visual review cannot be completed, retain deliverable HTML and actually generated PDFs, but label the corresponding status "pending visual review" rather than verified.

Chinese extraction may contain Unicode compatibility radicals. NFKC may assist keyword checks, but also inspect the original extracted text and visible glyphs. Normalization cannot replace checks for missing glyphs, lost text, or reading order.

After any HTML change affecting content or layout, repeat rendering and necessary checks for the affected language. Both languages must pass before the pair is complete. Do not repeat unrelated checks without a new output-affecting change or unresolved concern.

## 6. Version notes and JD writeback

`changes.md` is the derived version's current explanation and continuation entrypoint, not a copy of the base, entire JD, or knowledge base. Record at least:

- case-id, applicable role source, mode (role-specific or general), input sources, output paths, and settings used;
- selected base sections or user-supplied sources, linked requirement identifiers, significant changes, and their reasons;
- confirmed participation in new projects, included wording and evidence, and excluded candidates with missing facts;
- separate English and Chinese render commands, page count, A4 geometry, text extraction, and visual-review results;
- current resume status, outstanding work, next step, and confirmation that the base stayed unchanged.

When a JD pack's `meta/resume-handoff.md` exists, use its recorded pack root to link the resume directory from the pack's root `README.md`, and record independent resume status and remaining work in `meta/progress.md`. The case-id remains the pack root's directory name. If writeback is required but permission is missing, record the blocker. Do not regenerate completed Essential, KB, QA, or showcase content. Without a pack, an independent task maintains only resume artifacts and does not invoke the JD skill merely to write back.

A resume failure does not change completed interview-material status. A combined task with an incomplete resume cannot be marked entirely complete. Do not invoke this skill when the user explicitly requests interview preparation only.

## 7. Delivery and evaluation boundaries

Link both languages' HTML/PDF and version notes at delivery, with actual verification results and remaining blockers. Do not add personal bases, resumes, JDs, or private materials to a showcase, or publish remote resources automatically.

For evaluation or skill maintenance, use isolated temporary facts, bases, JDs, and outputs. Check that a new role does not overwrite an old one, continuation preserves user edits, unconfirmed participation stays out of the resume, bilingual facts match, and multi-page PDFs fail. Never modify a real base or create remote repositories in the name of testing.
