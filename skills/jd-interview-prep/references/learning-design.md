# Role-centered Learning Design and Content Review

Read after the JD and before selecting a project or writing the pack; use again while writing and reviewing. File structure and mapping formats are in [Deliverables](deliverables.md). This reference governs learning outcomes across the pack, not fixed chapter, word, question, or scoring quotas.

## Derive the whole pack from the role's work

First ask what the role delivers, which judgments are difficult, and which capabilities accomplish the work. Select core problems, important support, and optional extensions, then arrange prerequisite dependencies. Express this in the existing JD, KB roadmap, and coverage map; do not create a duplicate capability inventory. Ground preparation priorities in the JD or necessary inference, not unsupported predictions such as “always asked” or “definitely examined deeply.”

Check compound responsibilities one component at a time. For example, “agents, data engineering, and business strategy” cannot be covered by one generic “AI applications” link. A stable JD identifier may map to several topics and anchors, but every sub-capability needs specific teaching, practice, and QA or an honest factual gap. A heading, keyword, or existing link does not establish learning.

For each important topic, state which process the reader should explain, which choice they should make, and which variation or failure they should handle. These goals determine depth and acceptance, not showcase technology, implemented features, or code volume. Explicitly required capabilities need teaching even when the project does not implement them; difficult parts cannot become a few “future extensions.” A demand for proficiency in a technology is not represented by a narrow example merely because that example fits the project: expand to the role's actual use and mechanisms.

User-supplied reference answers may reveal role focus, grouping, priorities, and candidate questions, but remain material to evaluate. Verify technical conclusions and remove unsupported employer facts, interview-frequency predictions, unnecessary tool collections, and fabricated experience. Do not promote every term in a reference to mandatory knowledge. Change the capability thread with the JD instead of fixing every curriculum around AI, agents, frontend development, or one project.

## How the outputs support learning together

| Output | Learning task | Relationship to other outputs |
| --- | --- | --- |
| Essential | Build core understanding under limited preparation time, including mechanisms and tradeoffs | Independently learnable; KB is for deeper study |
| KB | Systematically recover prerequisites, understand important mechanisms, practice, and transfer to new conditions | Close necessary prerequisites within the KB series; the project is not a textbook prerequisite |
| QA | Convert understanding into direct spoken explanations, progressive follow-ups, and scenario reasoning | Derived from learning goals; key answers trace to teaching |
| Showcase | Demonstrate actual implementation and verification of part of the role | Optional integrated practice for learning, not the source of the whole curriculum |

Keep shared concepts consistent while expanding each output for its purpose, rather than repeating one summary. Distinguish conceptual questions, teaching assumptions, actual implementation, and personal experience. Explain factual boundaries centrally at the entry point and relevant question groups; add specific reminders where needed without allowing repeated disclaimers to displace mechanisms and practice.

## Essential: an independent core textbook

Begin with a short overview of the role's problems, knowledge relationships, reading priorities, and selection tradeoffs; then supply an independently understandable body. An overview is not a substitute for teaching. Start core topics from zero, add the minimum necessary foundations where used, and reserve systematic prerequisites for KB. P0 does not require opening with a general foundations course. Do not promise a uniform time to mastery.

For each core topic explain the problem, key roles, inputs/outputs, process, design reasons, applicability, and failure causes. A definition, term list, or analogy cannot replace a mechanism. Worked examples need complete inputs, process, and expected results that can be traced on paper. Use code only when it aids understanding. If recommending a method for an important judgment, carry the example through to the judgment rather than naming a method or stopping at an intermediate result.

The body and basic self-tests must not depend on showcase interfaces, fields, code, runtime, or reading order. KB and QA offer further learning, not patches for missing core explanations. Put project practice only as an optional closing entry. Self-tests change conditions, compare designs, or diagnose faults and include reference reasoning; they must not merely repeat the previous sentence or first teach necessary knowledge in an answer. Organize by understanding dependencies, not mechanically repeated “purpose / essence / example” headings.

## KB: a systematic textbook the reader can follow

### Roadmap and prerequisites

`00-roadmap.md` first shows the role's knowledge landscape, core problems, and learning goals, then the main route and foundation branches for specific gaps. Explain what each chapter solves, where to recover necessary prerequisites, what to practice, and how to judge readiness for the next step. Readers can encounter the role's core before recovering clear dependencies; do not assume every generic foundation must be read before any business problem.

KB may depend on precisely linked prerequisite chapters in the same series. It may not assume Essential, a running showcase, or unstated prior knowledge. Explain first-use terms, symbols, and foundations needed by the current process where used. Link longer prerequisites exactly; avoid cycles, skipped steps, or “search for it yourself.” Separate the learning environment from the project environment so canceling the project still leaves systematic learning usable.

### Required depth for important topics

Teach the normal process first, then test understanding through failures and changed constraints. The reader should trace who receives what, executes what, how state or data changes, and when the process continues or ends. Definitions, architecture arrows, library names, or warnings alone are insufficient; long code cannot replace process explanations.

Walk a small scenario with complete inputs and assumptions through its entire chain, explaining the causal role of key steps. For multiple actors, asynchronous messages, decisions, or execution, show enough intermediate states and returned results. Do not hide the crucial step inside “call the model,” “execute the tool,” or “run the sandbox.” Compare role-relevant alternatives with sufficient selection conditions instead of deeply teaching only the project's chosen approach and reducing alternatives to names.

Move exercises from following a worked example to changing conditions, independently handling new inputs, and diagnosing failures. Reference answers explain why and how to verify; open questions state assumptions and judgment criteria. Normal flow, variation, and troubleshooting must assess the capability the topic claims to teach, not another topic's skill. Check transfer with different micro-scenarios or new conditions so the whole pack is more than an expanded design document for one project.

Technical exercises need input data, complete code or explicit paper steps, required environment/dependencies, run instructions, expected observations, and verification methods. Fragments may illustrate but cannot be called complete runnable examples. Longer implementations may live in separate exercise files under KB when useful, while the body still explains mechanisms. Conceptual analysis and design choices need not require code, credentials, or live services. Identify which actor a simulation replaces and what it can verify.

Distinguish actual measurements from expectations. Verify dependency versions, APIs, and specialist conclusions against official or primary sources; external links do not replace teaching. For senior roles, extend to scale, reliability, and design tradeoffs according to the JD instead of adding beginner terms or tools to simulate depth. Keep JD framework and technology requirements in teaching and exercises even when showcase preferences select something different.

## QA: from understanding to transferable spoken reasoning

Group questions around the role's core topics and prioritize the interview route. Foundations, mechanisms, scenarios, projects, and behavior may be category labels; do not mechanically put every foundation before the core. Move each group from direct questions to normal mechanisms, then change constraints, introduce failures, or compare alternatives. Questions come from capability goals, not chapter titles with question marks. Train every sub-capability in complex requirements.

Short answers directly answer the question; deep answers explain causes, conditions, and choices. When follow-ups alter conditions, reference answers must reason accordingly rather than repeat one boundary sentence. Key reasoning needs locatable grounding in Essential or KB. Repair missing teaching instead of introducing an important mechanism only in QA. General technical and scenario questions are answerable without the showcase. Project questions instead cite actual code and verification; label unimplemented design scenarios as hypothetical.

Preserve honest frameworks for experience questions without inventing contributions. Include appropriate questions about unknown JD context, such as current deliverables, division of responsibilities, or success criteria, without assuming internal employer architecture or team facts. Mock interviews and self-checks should reveal which explanatory step or judgment condition breaks, directing the reader to specific KB practice; a uniform points table is not a capability diagnosis.

## Practice selection and reading routes

First choose which core capabilities the project proves deeply and which behaviors and observations verify them; then select an implementation. Use standalone exercises for other core capabilities when project scope is limited. Disclose missing real dependencies or production experience without shrinking the teaching. Distinguish fixed scripts, deterministic stand-ins, and real dynamic decisions. A button, phase label, or project name is not evidence of a capability.

The entry point offers core-understanding, systematic-learning, and integrated-practice routes. The core route may stop at Essential and core spoken answers without starting a project. The systematic route recovers dependencies and self-test gaps. Practice then enters independent exercises or the showcase. Each route states what the reader should be able to do and where to return when stuck. “Read the files” or “ran the demo” is not mastery. Generating a project by default does not require studying it first.

## Whole-pack content review

Structural validation checks files and mappings only. Review content separately:

- **Selection and depth:** Check compound requirements, difficult core problems, and supporting technologies against the original JD. Ensure project implementation did not set curriculum depth; broad chapter links cannot replace specific treatment.
- **Independent learning:** Give Essential reviewers only the JD and body. KB reviewers may also receive its explicitly declared KB prerequisites, not the project, QA, or extra explanations. Ask for mechanisms, worked variations, alternative comparisons, and diagnosis with textual grounds. Record a reasoning break when evidence is missing rather than filling it from the reviewer's knowledge. Example and self-test conditions must agree with taught rules.
- **Cross-output consistency:** Route acceptance tests the claimed capability; key QA answers trace to teaching; concepts, assumptions, data, and capability boundaries remain consistent. Repair cases where a definition was taught but a different skill is assessed.
- **Project facts:** Check every feature, number, and test-scope claim in QA, coverage, and the entry point against code or actual checks. One generic verification link cannot prove a whole paragraph. Do not present KB ideal designs, exercise coverage, or generic test checklists as project facts.

Use an isolated independent review when available; otherwise self-review to the same standard and disclose the method. Record specific gaps, revise, and recheck. Summarize content review in existing progress separately from project/publication status, without creating a fixed scoring file. Word, term, or heading counts do not prove quality. Neither review acceptance nor passing project tests proves the reader has mastered the material.
