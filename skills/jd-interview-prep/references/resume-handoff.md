# Handoff to Bilingual Role-specific Resumes

Read only when workspace instructions or the user requests resume integration. This skill is independent. Without explicitly provided fact sources and destinations, do not search broadly for or modify personal files. Obtain the workspace root from loaded instructions or explicit input, never from the skill installation path.

## Handoff file

Create `meta/resume-handoff.md` only when integration is needed; do not copy the whole KB. Record at least:

- Paths to the pack root, `meta/jd.md`, `meta/coverage.md`, `meta/progress.md`, and root README. Resolve handoff links from its directory and use these paths for writeback.
- Case-id: reuse the pack root directory name, preserving it on continuation. The containing `meta` directory is not the case-id. Include company, role, JD source, and links to relevant `JD-*` requirements.
- Available English/Chinese bases or supplied experience, plus an explicit resume destination. Include the workspace root and adopted preferences when available; otherwise mark them unavailable. User text is a valid source, and the resume skill can create HTML without a base using its Design System. Prefer relative links; accurately record absolute paths for external files.
- Relevant source files/sections, only necessary short quotations, and unmet requirements. Do not copy bases, create fact identifiers, or promote `INF-*` inferences into personal experience.
- `artifacts/showcase/` path, verified repository if published, actual implementation and check records, accepted online demo and simulation scope when applicable, unverified limitations, and known user participation or “unknown.” Explicitly state omission or absence of a project.
- Candidate resume wording, associated requirements, evidence, participation status, and limitations. Passing automated tests proves artifact behavior, not personal contribution or proficiency.
- Separate interview-material, implementation/verification, source-publication, online-demo, and resume states, with next steps. Public source or an accessible Pages demo does not prove user participation.

Only projects with explicitly established user participation may enter a role-specific resume. Editing the base additionally requires an explicit maintenance request. Keep unknown candidates in the handoff and resume `changes.md`; do not label them confirmed or block a resume based on established experience.

## Invocation and status

1. Mark the resume not started/in progress in `meta/progress.md` and save the handoff without redoing completed interview material.
2. Load the installed `bilingual-resume` entry point or the workspace-provided skill. Pass experience, handoff, destination, and available bases/preferences without requiring one fixed source layout. If unavailable, accurately mark resume integration blocked rather than claiming overall completion.
3. Use the user's or workspace's destination, otherwise the resume skill's independent output rule. Record the chosen location and reuse the case-id. The resume skill owns output/rendering requirements; preserve user edits on continuation.
4. Inspect actual bilingual files and status. Write links into the pack root README and independent resume status into the handoff-specified progress file. Run structural validation on the pack root to check new relative links.
5. If rendering or factual review fails, preserve interview outputs, completed versions, and next steps. Do not call the entire integrated task complete. For interview-only requests, record resume omission by user instruction and do not invoke the resume skill.

Do not publish the handoff, personal facts, resumes, or changes record in the showcase. Personal background informs resume selection by default; preserve beginner-level teaching unless the user requests a different learning baseline.
