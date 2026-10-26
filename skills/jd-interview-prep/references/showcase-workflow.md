# Showcase Technology Selection and Demo Modes

Read when implementing a project. See [Deliverables](deliverables.md) for structure and [GitHub workflow](github-workflow.md) for publication. Select technology to demonstrate core JD capabilities; do not add unnecessary frontend/backend components merely to use a preferred stack.

## Choose the capability to prove

Choose part of the whole pack's capability thread for deep implementation. Map it in the project README/design to concrete behavior, demo inputs, and verification evidence; cover other core capabilities through standalone KB exercises. A small scope is acceptable, but it must not shrink teaching or use broad capability labels to conceal a UI-only implementation.

For example, proving host-side tool execution needs actual handling of a proposed call, validation and dispatch, correlated results, return to the model, and continuation/termination. Deterministic model output and tool stand-ins can verify that program chain; stage animation cannot. Distinguish stand-in verification, real model decisions, external integration, and production effects. Missing live dependencies need not prevent a complete, verifiable program mechanism.

Check each feature, number, and test-scope claim in project documentation and QA against code or actual checks. KB designs, simulation scripts, and generic test lists are not current facts. Citing a verification document does not establish every scenario claimed in prose.

## Technology selection

- Select frameworks and languages from the JD and actual project needs by default. Current user instructions override adopted preferences; explicitly loaded preferences may select a different demonstration stack. Do not load personal settings from the installation directory. On continuation, preserve confirmed stack decisions unless current instructions change them.
- **Frontend:** Use the JD's required framework when it is relevant to the project by default. When supplied, `frontend_policy: prefer_jd` keeps an explicit JD requirement ahead of a configured frontend; `prefer_config` uses the configured frontend even when the JD names another stack. A current explicit user instruction takes precedence. For example, a user can select Vue with `prefer_config` even for a React JD; disclose that difference and fully teach/practice the JD's React requirements in KB and QA. A Vue showcase cannot be claimed as verified React implementation. Essential continues to select topics by role-level importance.
- **Backend:** Follow explicit JD requirements by default. When no backend is mandated, honor a supplied preference such as FastAPI or choose an appropriate implementation. A JD listing languages as alternatives leaves that choice open. A current instruction can explicitly change the demonstration stack; record any difference. Do not add a backend to a purely frontend project.
- Briefly record the selection rationale, differences from the JD, and complementary exercises. Use compatible versions checked during implementation and lock dependencies as appropriate; do not hardcode dependency versions as permanent skill defaults.

## One project, optional static and complete local modes

The default deliverable is a local project. When Pages is enabled and browser presentation is meaningful, provide a static demonstration and keep a reproducible full local flow for projects with a backend. Pages hosts static HTML/CSS/JavaScript; an application backend needs its own runtime process, so a successful Pages build is not backend deployment. Do not purchase services or create other cloud resources by default. [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), [FastAPI deployment example](https://fastapi.tiangolo.com/deployment/manually/).

| Part | Optional Pages static demo | Complete local flow |
| --- | --- | --- |
| UI, rendering, editing, interaction state | Same frontend | Same frontend |
| Input/output/event constraints and public samples | Shared contracts and fixtures | Shared contracts and fixtures |
| Transport adapter | In-browser simulation or fixture replay | HTTP/backend calls when needed |
| Business scope | Explicitly simulated scenarios and limitations | Actually implemented interfaces, business logic, and dependencies |

- Switch the transport adapter rather than maintaining two UIs or duplicating backend business algorithms for Pages. Prevent cross-language contract drift with shared schemas, type generation, or the same positive/negative samples validated by both sides. Use the smallest suitable approach.
- Label the Pages UI and README “static demo / simulated data.” Explain sample selection and which capabilities need local services. Arbitrary input must not appear to have been understood by a real model. The online demo needs no keys, login, or localhost service; never bundle secrets in the browser. The full local flow may also use mocks; state which real dependencies are integrated and actually checked.
- If generation streams, share event consumption, validation, result commit, and request-identity protection across adapters. Keep project-relevant progress, error, slow-response, cancellation, and retry interactions. Business needs determine event/protocol design; do not impose one project's fixed stages on every showcase.
- Static cancellation cleans timers, streams, and old request state. Separately test disconnection and background-task cleanup in the local flow. Browser cancellation or a passing simulation does not prove a real model call was canceled, provider billing stopped, or production integration was verified.

## Local acceptance

1. Verify shared contracts, valid/invalid samples, the business loop, and project-relevant errors, cancellation, concurrency, and stale responses. Frontend and backend should agree on the same public samples.
2. If a Pages mode is included, build and preview under the real repository subpath with the local API stopped. Check core interactions, resources, and applicable editing/export. No localhost requests, missing keys, or resource 404s may be required for the static loop. Test direct navigation and refresh when routing is used.
3. Start and check the complete local flow, including real interface/frontend integration. For streaming, commit only a valid terminal result; preserve recoverable state on failure/cancellation, and prevent stale requests from overwriting newer work.
4. Record commands, results, environment, and limitations separately for each implemented mode. A published simulation proves tested program behavior, not real model quality, production impact, or personal work experience.
