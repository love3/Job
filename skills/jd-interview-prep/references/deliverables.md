# Preparation Pack Deliverables

Read when mapping requirements, writing, and checking the final pack. Curriculum organization, depth, and content review follow [Learning design](learning-design.md). Internal teaching links are relative to the pack itself, not the skill source or temporary paths. Workspace handoffs may accurately reference facts and resume locations in that workspace. Tables below illustrate format only; replace their content with the actual JD and evidence.

## Layout and boundaries

```text
<company>-<role>-<date>/
├── README.md                     # Learning and demonstration entry point
├── artifacts/                    # Deliverables to read, practice, and demonstrate
│   ├── essential.md
│   ├── qa.md
│   ├── kb/
│   │   ├── 00-roadmap.md
│   │   └── <chapters organized by knowledge dependencies>
│   └── showcase/                 # When enabled; independent project repository
│       ├── README.md
│       └── <actual implementation and necessary documentation>
└── meta/                         # JD inputs, coverage, continuation, optional handoff
    ├── jd.md
    ├── coverage.md
    ├── progress.md
    ├── sources/                  # Original attachments only when needed
    └── resume-handoff.md          # Only for enabled resume integration
```

No-project requests do not need `artifacts/showcase/`; local-only projects still do. KB needs both a roadmap and substantive teaching chapters, expanding with the role's actual demands rather than treating a minimum file count as completion. The root README links core deliverables directly so readers need not inspect run records before studying.

### Required, conditional, and continued outputs

| File/directory | Creation condition and purpose |
| --- | --- |
| `meta/jd.md` | Required in every complete pack. Sole basis for the extracted JD, sources, numbered requirements, and inferences |
| `meta/coverage.md` | Required in every complete pack. Maps requirements to teaching, QA, practice, and factual gaps without repeating the body |
| `meta/progress.md` | Required in every complete pack, created before writing. Current status, decisions, actual verification, and next steps |
| `meta/resume-handoff.md` | Only when resume integration is configured or explicitly requested; do not create an empty handoff when resumes are omitted |
| `meta/sources/` | Preserve necessary original attachments as needed; cite directly readable stable sources in the JD instead of duplicating fact inventories |

All three required Meta files remain mandatory when the project is canceled. Do not omit them according to agent interpretation. Do not add redundant JSON requirement inventories, separate research journals, or tool transcripts by default. Continue by reading/updating existing files rather than regenerating the pack. Skill maintenance and ordinary conceptual answers do not create formal packs.

### Relative links

Resolve links from **the containing file's directory**. Root README links `artifacts/essential.md`; Essential links `kb/00-roadmap.md`, `qa.md`, and `showcase/README.md`. A JD reference from artifacts is `../meta/jd.md`; from a KB chapter it is `../../meta/jd.md`. Coverage links from meta use `../artifacts/...`.

## Sources, requirements, and coverage tables

`meta/jd.md` records company, role, level, sources and faithful extraction, access time, uncertainties, user background/constraints, and adopted settings. Mark missing facts unknown; do not infer user competence.

Use the following requirement-table headers. The ID is an independent value in the first column, unique per table row; the same identifier may recur in prose:

```markdown
| ID | Source type | JD requirement / supplemental capability | Priority |
| --- | --- | --- | --- |
| JD-001 | Explicit | Actual requirement from this JD | P0 |
| INF-001 | Inferred | Necessary prerequisite, with the inference explained | P1 |
```

Use only `Explicit` and `Inferred`, corresponding to `JD-*` and `INF-*`, and P0/P1/P2 priorities. Preserve explicit meaning and justify additions. Record years, education, and industry experience instead of deleting them to improve coverage.

`meta/coverage.md` uses the fixed headers below. Its ID set, types, and priorities must match `meta/jd.md`; the requirement column may summarize without changing meaning:

```markdown
| ID | Type | Priority | Requirement | Essential | KB | QA | Practice evidence / gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JD-001 | Explicit | P0 | Actual requirement | [Mechanism and self-test](../artifacts/essential.md) | [Teaching](../artifacts/kb/01-topic.md) | [Question and follow-ups](../artifacts/qa.md) | [Implementation and verification](../artifacts/showcase/README.md) |
```

For Chinese outputs, equivalent headers are accepted: requirement table `ID | 来源类型 | JD 要求/补充能力 | 优先级`; coverage `ID | 类型 | 优先级 | 要求 | Essential | KB | QA | 实践证据/差距`. Types `明确`/`推断` are equivalent to `Explicit`/`Inferred`; English types are case-insensitive. These are bilingual output contracts, independent of the language of the skill instructions.

Core requirements link appropriate Essential teaching, preferably a section. Supporting or extended requirements may use `Non-core: <specific reason>` in that column, explaining why they do not belong to the core thread. KB and QA still need actual treatment or a factual-gap response: `Non-core` does not exempt those columns. Difficulty, lack of project implementation, or an existing KB link is insufficient grounds to exclude a key role requirement. Decide preparation priority separately from textbook order; do not automatically include/exclude an entire priority level.

For non-learning items such as education or years, use `Non-learning item: <specific reason>` and provide an honest QA/gap response. Practice links actual project files, verification, or exercises. Use `Gap: <specific reason>` for unproven capability, `Pending: <reason and next step>` for unfinished work, or `Unverified: <reason>` for unverified work. With no project, write `Omitted: user canceled the project` and still link suitable KB exercises. Chinese equivalents are `非核心：`, `非学习项：`, `差距：`, `待完成：`, `未验证：`, and `已省略：`, always followed by a concrete reason.

For compound requirements, identify each sub-capability's teaching/QA anchors in the same row, or add concise mappings by existing requirement ID after the table. Do not insert prose between table rows, change identifiers, or create duplicate management files. A broad chapter link must not hide untreated sub-capabilities.

Coverage is navigation and a factual record, not a mastery score. Blank columns, placeholder links, and “covered” do not replace content. Existing links do not establish sufficient depth. Content review checks specific treatment, acceptance goals, and practice claims. Disclose genuine blockers in both the entry point and progress.

## artifacts/essential.md: an independent core textbook

Essential helps time-limited readers establish core understanding of the role, mechanisms, tradeoffs, and failures. Start with a concise overview, relationships, and reading route, then independently teach the core topics from zero. Examples, self-tests, and reference reasoning do not depend on the project. Topic selection, layered reading, self-contained examples, and evidence-based review follow learning design; other deliverables cannot patch missing explanations in this body.

## KB: from prerequisites to role-level depth

`artifacts/kb/00-roadmap.md` presents the knowledge landscape, core thread, prerequisite recovery, chapter index, exercise goals, and acceptance methods. Each chapter states requirement links, learning goals, prerequisites, and precise entry points. Unknown background means beginner treatment; unknown deadlines do not justify invented schedules. Systematic study does not presuppose Essential or a running project.

Develop the body through topics and understanding dependencies. Learning design defines standards for normal processes, complete examples, variations, reference reasoning, diagnosis, and design choices. Key knowledge outside the project still needs teaching and practice; JD frameworks cannot be replaced by a preferred showcase stack. Length, code volume, file count, and source count are not depth metrics. Distinguish applicable versions/sources, observed results, and expectations.

## QA: clear spoken answers and defensible follow-ups

Organize `artifacts/qa.md` by the role's core topics and a prioritized route. Foundations, mechanisms, scenarios, project, and behavior may be category labels. Train every explicit JD requirement and each sub-capability in compound requirements, or provide an honest factual-gap response. Prioritize depth in important topics; actual needs determine question count.

Each question includes an identifier such as `Q-001`, JD IDs, assessment target, concise spoken answer, reasoned deep answer, follow-ups with reference answers, common mistakes, and precise teaching links. Project questions additionally cite actual evidence. Short answers respond directly; deep answers explain causes, conditions, and choices. General technical/scenario answers are independent of the showcase. Follow learning design for progressive questioning, review routes, and candidate questions for the interviewer.

- Scenario answers identify assumptions, analysis, alternatives, and verification, rather than implying one universal correct solution.
- Check every project feature, number, and test-scope claim. KB ideal designs, standalone exercises, and generic test lists are not current implementation evidence. Label unimplemented capabilities as extensions, not existing features.
- Behavioral questions use real user facts; with insufficient facts provide a situation/task/action/result framework and honest phrasing. Label hypothetical examples so they cannot be mistaken for user experience.
- A mock-interview sequence or self-assessment criteria may supplement, not replace, complete answers.

## Showcase: inspectable evidence

First define target users, business loop, deeply demonstrated capabilities, observable behavior, minimum acceptance scenarios, and simplifications. Then actually implement them; fragments and design documents alone are not a complete project. Use independent exercises for core capabilities outside the project rather than reducing teaching depth.

`artifacts/showcase/README.md` explains value, prerequisites, dependencies, installation/startup, demo data, a step-by-step demonstration, expected output, and test commands, plus a verified online link and simulation scope when published. Technology selection and optional Pages/local modes follow [Showcase workflow](showcase-workflow.md). Split other material when useful:

- Design tradeoffs: modules/data flow, key decisions, alternatives, limitations, and JD capability mappings.
- Verification evidence: actual environment/versions, commands, dates, results, and coverage boundaries. Claims trace to implementation or checks. Give reasons for unrun checks; do not present expectations as measurements or copy unperformed scenarios from templates.
- Demo script: show the complete loop, explain key design, present verification, and disclose limitations.
- Project follow-ups may stay in local `artifacts/qa.md`; the published project has necessary run/design documentation and never depends on local learning material or Meta files.

Meaningfully verify critical business and error-prone paths, without tests for an arbitrary coverage target. Distinguish test, performance, and business-impact evidence. Label simulated data; missing external credentials may lead to a local demonstration, never a false claim of real integration.

For nontechnical roles, use inspectable reports, analytical models, or operational plans with sources, methods, evaluation criteria, and limitations. Do not force unrelated software.

Publication follows [GitHub workflow](github-workflow.md) only when enabled.

## Entry point, progress, and validation

Root `README.md` first explains the role's core work, capability thread, and priorities, then offers core-understanding, systematic-learning, and integrated-practice routes. Link Essential, KB roadmap, QA, project, and any verified online demo. Core reading does not require running a project. Show dependencies and recovery points for systematic learning; practice enters implementation afterward. Route goals and acceptance follow learning design. Then provide Meta navigation and centralize real-experience gaps, unfinished work, source publication, and online-demo status.

`meta/progress.md` preserves cross-session facts as concise current status, key decisions, verification summaries, and next steps, not a history of tool output:

- Inputs, user overrides/adopted preferences, and unanswered but nonblocking assumptions.
- Independent states for documents, implementation, project verification, source publication, and online demo: not started / in progress / complete / blocked / omitted, with reasons. Pages completion means online acceptance, not merely a successful deployment command.
- Completed files, important decisions, content-review method/specific gaps/revision checks, actual commands/dates/results, and evidence locations. Separate generating material from reviewing learning quality.
- Confirmed GitHub account, repository URL, branch, and SHA when publishing. For Pages, separately record actual URL, workflow run, deployed commit, and browser result. Explain unpublished/unverified states instead of inventing unknown fields.
- Blockers, incomplete work, and executable next steps. Inspect user edits before continuation.

When resume integration is required, follow [Resume handoff](resume-handoff.md) to create `meta/resume-handoff.md` with actual progress paths and maintain independent bilingual-resume status, verification, and links. Resume status does not rewrite interview-material status. An interview-only request records the resume as omitted by user instruction.

Run `python3 scripts/validate_pack.py PACK_DIR` with the pack root. Add `--no-project` for a canceled project or `--portfolio` for nontechnical reports, never both. A default technical project needs a non-document implementation file; portfolio mode allows a nonempty report, PDF, image, etc. beyond README. The script checks required files, relative file links, requirement IDs, type/priority consistency, and coverage columns. It does not check internet links, fragment anchors, teaching quality, artifact authenticity, code execution, user mastery, source pushes, or online deployment.

If publication is blocked or writing remains unfinished, deliver usable work and consistently disclose the state in the entry point, progress, and final response. File counts, empty sections, template markers, or a structure pass cannot stand in for complete delivery.
