---
name: bilingual-resume
description: "Create paired English and Chinese HTML/PDF resumes from verified experience, including role-specific versions, general resumes, and explicitly requested bilingual base maintenance. Use independently or after a JD preparation pack; not for ordinary translation, JD learning materials, or general career advice."
---

# Bilingual Resume

Create resumes from traceable facts, producing English first and then semantically consistent Chinese. Run independently or continue a JD preparation pack without depending on a particular workspace or fixed source file. Read the [workflow, Design System, and acceptance requirements](references/resume-workflow.md) when executing. Use this skill's [renderer](scripts/render-pdf.py) for HTML to PDF.

## Content and writing rules

- **First principles:** Start from the problems the role actually needs to solve. Select verifiable experience and explain the person's contribution, implementation mechanism, and results or tradeoffs. An inference about a role cannot become personal experience.
- **A coherent narrative:** Organize the resume around a capability relevant to the target role. Give each sentence one purpose, using supported action, mechanism, and result; remove repetition, empty adjectives, and irrelevant details. Quantify only real measurements. Without numbers, state the scope and verifiable deliverables.
- **ATS readability:** Use standard sections, a single column, and extractable text. Incorporate supported role keywords naturally into skills and experience. Do not stuff keywords, hide text, or promise an ATS score.
- **Factual and bilingual consistency:** Do not invent tenure, proficiency, titles, contributions, or impact. Keep participation, dates, metrics, and causality consistent across languages. Preserve explicitly confirmed content and design preferences without turning one person's preferences into universal requirements.

## Inputs and settings

- The required input is verifiable experience. When a base exists, read its body directly rather than creating another fact inventory. Without a base, use the resume or experience text supplied by the user and create HTML with the Design System. Ask only about consequential gaps or conflicts that affect the result.
- JD text, screenshots, files, links, or a pack's `meta/resume-handoff.md` support role-specific tailoring. Without a target role, create a general bilingual resume; do not generate a JD knowledge base or showcase.
- Read private sources and preferences only when supplied by the user or explicitly identified by an applicable, already loaded workspace. Do not infer a user's identity or search for private configuration from the skill's installation path. Default to a derived version; modify a base in place only when base maintenance is explicitly requested.
- For a new task, apply the current request, then supplied or loaded user preferences, then the skill's defaults. On continuation, apply the current request, then the settings already confirmed in `changes.md` and the user's edits, then preferences, then defaults. A changed preference must not silently reset an existing task. A one-time instruction applies to that task; persist preferences only when the user explicitly asks.

## Execution

1. Identify role-specific, general, or explicitly requested base-maintenance mode. Read experience, applicable preferences, and role input. On continuation, first inspect existing notes, user edits, and linked progress; preserve completed work.
2. Choose a `case-id` and new output directory for a role-specific or general version. Base maintenance uses the specified files. Map role requirements to factual evidence and exclude unconfirmed personal contributions.
3. Create English HTML with fact-based emphasis. Render and verify it, then create Chinese with matching facts, scope, dates, metrics, and terminology.
4. Verify each PDF is one A4 page, has extractable text, and passes visual review. Record actual results and fix failures. Mark missing dependencies or rendering failures as incomplete.
5. Deliver both languages' HTML/PDF and the actual verification results. Derived versions also include `changes.md`. When continuing a JD handoff, retain its case-id and write back resume paths and independent status. An independent task requires neither a handoff nor another skill.

## Facts and completion boundaries

- The base body is the long-term source of experience; PDFs are derived artifacts. The user's current explicit confirmation takes precedence, and source conflicts require clarification. Locate evidence with files, sections, or short necessary quotations. A derived version does not automatically update the base.
- Teaching examples, model interview answers, inferences, and automatically generated projects cannot become personal experience.
- If participation in a new showcase is unconfirmed, exclude it from the base and resume. List it as a candidate in the version notes and continue using established experience rather than stopping by default to wait for confirmation.
- Deliver locally by default. Do not place resumes or private materials in showcase repositories. A resume failure preserves completed JD work, while the combined task still has outstanding work.
