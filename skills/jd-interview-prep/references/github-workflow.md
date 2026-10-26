# Showcase Implementation and GitHub Publication

Read when a project is needed. Technology selection and demo modes follow [Showcase workflow](showcase-workflow.md); complete output requirements are in [Deliverables](deliverables.md), and the main flow is in [SKILL.md](../SKILL.md).

## Defaults and authorization scope

- Implement a complete, locally runnable small project in `artifacts/showcase/` by default. “Project directory” below means that path. **Local generation is the default; a complete preparation request alone does not enable publication.** Publish source only when current instructions or explicitly adopted preferences select public/private publication. Deploy suitable Pages only when enabled and applicable. Derive the repository's ASCII theme slug from the core capability without unnecessarily exposing the target employer.
- Owner and fallback author identity come from explicit current input or loaded workspace preferences/fact sources, never a hardcoded person. Current input wins. When publishing without an owner setting, use the current authenticated personal account; do not infer it from an email. Verify any specified owner.
- Explicitly configured publication is part of the requested workflow, so do not ask for the same permission again. Planning, skill maintenance, isolated evaluation without a real task, local-only, no-project, and publication-disabled requests create no remote showcase resources or deployments. Changing a one-off instruction does not save a new personal preference unless requested. Preserve confirmed publication settings on continuation unless current instructions change them.
- Use a fallback email only when supplied by confirmed user information and a valid author email is missing. It is not evidence of authenticated identity. Keep existing valid author settings; any required change is repository-local, never global.
- Publish only the project directory and upload only its static build to Pages. Keep JD input, resumes, learning material, QA, coverage, and progress local. Extract appropriate public project explanations instead of copying the whole preparation pack.

## 1. Local implementation and verification

1. Select core requirements suitable for deep implementation in a small project. Define inputs, outputs, the business loop, visible results, and tradeoffs. An empty scaffold or design document is not a completed project.
2. Implement a local flow and, when enabled, a suitable static mode using [Showcase workflow](showcase-workflow.md). Do not purchase or deploy other cloud services by default. Configure actual external dependencies through environment variables and provide usable examples. Label simulated data and mocks in both README and demo. Record untested real integrations as gaps, not completed integration.
3. Complete code, meaningful tests, run instructions, design tradeoffs, verification records, and a demo script using [Deliverables](deliverables.md). Actually run the project and key checks, recording commands, outcomes, environment, and limitations. Performance and accuracy numbers must come from measurement.
4. Before any enabled publication, inspect the exact files to commit. Exclude credentials, tokens, real `.env` values, personal information, JD text, private data, dependency caches, and build products. Configure an appropriate `.gitignore`; use placeholders or clearly simulated public examples. Do not print sensitive contents into logs.

A public push also exposes commit history. Before the first publication of a reused repository, inspect all reachable history of the branch to be published, including deleted files; on later pushes inspect added commits. The current tree/index alone is insufficient. If the history cannot be confirmed within the public scope, preserve local work and report a publication blocker without deleting or rewriting history.

For a local-only project, stop before remote configuration and report source publication/Pages as omitted under the adopted settings. The independent local repository and verification can still be completed.

## 2. Confirm an independent Git repository

The preparation pack may be inside another Git repository. Resolve the project's actual absolute path and check the Git top level; successful `git status` alone does not prove independence.

Commands below are stepwise examples. Obtain paths and names from confirmed state instead of interpolating JD/user text directly into shell commands.

```sh
showcase_dir='/absolute/path/to/preparations/company-role-date/artifacts/showcase'
git -C "$showcase_dir" rev-parse --show-toplevel
```

Normalize and compare the returned path to `showcase_dir`. If equal, inspect and reuse it. If the command fails or returns a parent repository, initialize inside the project directory. Do not operate on the parent's configuration or index.

```sh
git -C "$showcase_dir" init -b main
git -C "$showcase_dir" config --get user.name
git -C "$showcase_dir" config --get user.email
```

Preserve an existing repository's branch and history. Use valid author settings when present. If missing, determine the name from confirmed user identity or GitHub account data, using an available confirmed fallback email where needed. Restrict any change to this repository, for example:

```sh
git -C "$showcase_dir" config --local user.email "$project_email"
```

Obtain and safely pass `project_email` from confirmed information; do not run the example with an unknown value. Inspect the working tree and stage reviewed paths only. The filenames below are examples, not a fixed list. Do not use `git add ..` or expand into the pack or parent repository. When reusing a repository, ensure the index contains no unrelated existing user changes.

```sh
git -C "$showcase_dir" status --short --untracked-files=all
git -C "$showcase_dir" add -- README.md .gitignore pyproject.toml src tests
git -C "$showcase_dir" diff --cached --stat
git -C "$showcase_dir" diff --cached --name-only
```

Review staged content and actual verification before committing. Describe the real implementation, not unrun tests as passed. This commit covers only the showcase.

## 3. Verify GitHub identity and target when publication is enabled

Prefer an available platform connector that can read identity/repositories, create a repository, publish content, and verify the remote commit. Otherwise use `gh` and `git`. The same identity, scope, and outcome rules apply to either; no specific connector is mandatory.

With `gh`, first read:

```sh
gh auth status
gh api user --jq '.login'
```

Check valid authentication, the selected owner, and target write permission without reading/printing tokens. Email is not authentication evidence. If a configured owner differs from the authenticated identity, first inspect explicit authorization for that account; without grounds ask which identity to use rather than switching accounts or creating resources. Continue feasible local work if authentication is unavailable, recording pending publication.

Read the chosen remote target before creating it. A default slug can be `jd-<project-theme>`; use `-2`, `-3`, etc. for naming conflicts. Reuse an existing same-name repository only when progress, configured remote, history, or explicit user instructions establish that it belongs to this project. Ownership by the same account alone does not authorize overwriting it. Distinguish absence from permission/read failures before creating anything.

```sh
repo_slug='jd-example-project'
gh repo view "$repo_owner/$repo_slug" --json nameWithOwner,url,isPrivate,defaultBranchRef
git -C "$showcase_dir" remote -v
```

Both `repo_owner` and `repo_slug` must be verified identifiers. Inspect the exact target of an existing `origin`; do not replace a different remote. Confirm repository identity, file scope, a valid local commit, and adopted publication settings before remote writes.

## 4. Create, push, and verify

Treat repository creation and pushing as separate states. This example applies only when **public publication is enabled**, the target is confirmed absent, and no `origin` exists. Use `--private` instead when private publication is selected; local mode does not run either command.

```sh
gh repo create "$repo_owner/$repo_slug" --public --source="$showcase_dir" --remote=origin
git -C "$showcase_dir" remote get-url origin
git -C "$showcase_dir" branch --show-current
```

Use the actual branch name after confirming the remote. Do not assume a reused repository uses `main`, and do not force-push.

```sh
project_branch='main'
git -C "$showcase_dir" push -u origin "$project_branch"
git -C "$showcase_dir" rev-parse HEAD
git -C "$showcase_dir" ls-remote origin "refs/heads/$project_branch"
gh repo view "$repo_owner/$repo_slug" --json nameWithOwner,url,isPrivate,defaultBranchRef
```

Mark **source publication complete** only after the remote branch SHA matches the expected local commit and URL, owner, visibility, and default branch are verified. A new repository's default branch should be the demonstration branch; inspect before changing mismatches. Connector publication also requires remote commit verification. Repository creation, command success, or receiving a URL does not prove code publication or an online demo.

## 5. Optional GitHub Pages deployment and online acceptance

1. Proceed only when Pages is enabled, publication allows it, and a meaningful browser demo exists. Inspect settings and permissions, then configure Actions as the publishing source only if needed. Verify existing configuration belongs to this project and preserve user settings. If private publication/Pages eligibility or permissions prevent deployment, record it pending without silently making private source public. Continue local/source delivery. For backend-only or unsuitable projects, record inapplicability instead of adding a frontend or another cloud backend for hosting.
2. Provide a Pages workflow for actual-branch pushes and manual dispatch. Run appropriate checks, install locked dependencies, and build the static demo using official `configure-pages`, `upload-pages-artifact`, and `deploy-pages` actions. Verify current official versions during implementation and pin verified versions/commits. Deployment needs `contents: read`, `pages: write`, `id-token: write`, the `github-pages` environment, and successful build dependencies. Upload only static output with `index.html` at its root, not the repository or local backend. [Official Actions workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
3. For Vite project sites, set `base` from the actual URL to `/<repo>/`; use `/` only for account-root sites or confirmed custom domains. Asset and fixture paths follow the same prefix. Do not add routing unnecessarily; where needed, default to hash routing and check direct navigation/refresh. Preview the build at the same subpath without a localhost API before pushing. [Vite Pages deployment](https://vite.dev/guide/static-deploy.html#github-pages).
4. After pushing, inspect the workflow run for the target commit, `head_sha`, build/deployment conclusions, and actual Pages URL. Reconcile any difference between deployed and verified source commits instead of accepting an old deployment as current. Read the URL from Pages/deployment state rather than guessing. [Pages status API](https://docs.github.com/en/rest/pages/pages#get-a-github-pages-site).
5. Open the actual online URL in a browser and check resources, clear simulation labeling, and the business loop. Test applicable streaming, cancellation, regeneration, editing, and export. Mark **online demonstration accepted** only when the page belongs to the intended build and works without local services. Workflow success, HTTP 200, or a URL cannot replace interaction checks; unavailable browser verification means pending online acceptance.

## 6. Failures, continuation, and status

- If creation times out or the outcome is unknown, read the target repository, remote, and branch first, reconciling completed actions before retrying. Do not create duplicate repositories because the previous result is uncertain.
- Stop repeating an operation after the same failure occurs twice. Record the error category, completed steps, and information required to proceed while continuing independent work. Do not delete repositories, rewrite history, or force-push to hide failures.
- Track local implementation, project verification, source publication, and online deployment/acceptance independently in `meta/progress.md`. Record actual commands/results, repository URL/branch/SHA, and applicable Pages URL/workflow run/deployed commit/browser checks. Mark unknown fields unverified; preserve failures and next steps without inventing success or mixing stage states.
- Add verified source and online links separately to the pack and project README. Any resulting new public commit requires final source/deployment verification again. The pack's own state records are never uploaded with the showcase. A Pages failure does not erase local or source-verification facts; report each separately and preserve usable work for continuation.
