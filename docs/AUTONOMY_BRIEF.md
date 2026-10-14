# Autonomous portfolio task brief

## Assignment

Improve the entire career portfolio into a coherent, technically credible hiring resource with excellent graphics and search-friendly writing. Read [AGENTS.md](../AGENTS.md), then [WORK_QUEUE.md](WORK_QUEUE.md), before editing.

This is portfolio work. Employment safety and evidence-backed fit guide decisions; do not turn the run into an unrelated job-search project or wait for vacancies before improving existing material. Use current source records and all areas of Tucker's background.

Preserve the user's direct personal voice, occasional bigger words, and earned technical vocabulary. For every substantive case, recover the full decision and then derive a concise reading version. Keep deeper evidence reachable.

## Existing source map

- [Experience](../EXPERIENCE.md), [capabilities](../CAPABILITIES.md), and [work index](../WORK_INDEX.md).
- [Source review](SOURCE_REVIEW.md), [evidence map](EVIDENCE_MAP.md), and [owner inputs](OWNER_INPUTS.md).
- [Artifact index](../artifacts/README.md) and [figure guide](FIGURE_GUIDE.md).
- Project pages and their artifact records; inspect affected dependencies and generation scripts before edits.

Use public/retained facts directly. Read additional authorized records when accessible, but retain only appropriate public evidence in this public repo. Seek firsthand information only when it changes a claim or decision.

## Execution loop

1. Refresh repository head and open PRs. Reconcile any existing batch and read the queue.
2. Survey breadth, evidence strength, employer relevance, and remaining ready work. Choose a small coherent batch.
3. Complete the changes. Delegate independent scopes where supported; prevent shared-file collisions.
4. Review the complete diff. Check claims against sources and accepted limitations. Keep source records and generated assets consistent.
5. Run relevant checks and inspect changed exports. Repair concrete failures before calling the batch verified.
6. Update queue status, parked dependencies, and next action. Record validation SHA/run links on the PR or result; a previous passing SHA is not current evidence.
7. Continue ready work until the v1 criteria below are met. If one source or tool is blocked, use available independent paths. Stop for missing required authorization or a genuine whole-task blocker with a precise report.

Use one branch and one reviewable PR for the release unless the operator explicitly changes the release arrangement. Keep drafting, execution, rendering, publication, and outcome verification separate in reports.

## Candidate checks

The existing workflow is [.github/workflows/portfolio-artifacts.yml](../.github/workflows/portfolio-artifacts.yml). It verifies and renders on PRs, main pushes, and manual dispatch; it does not run an agent or deploy a site.

Its current commands are:

~~~bash
python3 -m pip install --disable-pip-version-check --no-input CairoSVG==2.7.1 matplotlib==3.9.2 pypdf==5.1.0
python3 artifacts/colorado-transit-award-service/build_crosswalk.py
python3 scripts/air_storage_model.py --check
python3 scripts/render-portfolio.py --check --output /tmp/portfolio-rendered
python3 scripts/verify-portfolio.py
~~~

For intentionally changed generated assets, use the regeneration sequence in [FIGURE_GUIDE.md](FIGURE_GUIDE.md), then rerun check mode. Do not change retained exports simply to suppress a failure.

These checks establish retained calculation/export/link consistency. They do not independently verify historical accounts, rerun private software, establish delivered service, or judge visual quality. Review full-size and 375-pixel previews yourself. Do not count a recalled recovery duration as a measured run.

If the local launcher fails, document it and use connector reads/writes and exact-revision CI where available. Do not repeatedly retry the same failed launcher or repair the workstation as a portfolio side task.

## v1 finish line

- A clear entry page with balanced paths into paid work, fabrication/repair, independent hardware, software direction, Linux, research, and education.
- All five employers and Mines remain discoverable; missing employer-specific facts are visibly scoped and parked.
- At least three useful decision/evidence accounts from distinct work areas, with contribution, constraints, check, result, and limitations clear.
- Recovery, synthetic execution, historical reconstruction, and measured results are distinguished at the quick-reading surfaces.
- At least two relevant technical figures from different areas have been inspected in actual full-size and phone-width exports, with print/PDF reviewed where applicable. Concrete reading/layout defects are resolved. If a required inspection cannot run, record it as unfinished; do not declare v1 complete.
- Supported titles/headings/captions/links make the content easier to discover and inspect. Website-only SEO is not reported implemented without a site.
- Candidate checks pass on the exact PR head. The result and queue identify any remaining nonblocking firsthand gaps.
- A reviewable PR is available. Merge/publication follows the operator's actual authorization.

Every V1-* row in WORK_QUEUE.md is required and must meet its acceptance condition before v1 completion. Parked firsthand dependencies are nonblocking when existing facts can be presented with their limitations. Stop after v1 rather than endlessly enlarging the corpus. Further studies belong in the next queue after use or new evidence justifies them.

## One instruction to launch

> Finish portfolio v1 using AGENTS.md, this brief, and WORK_QUEUE.md. Work autonomously across the whole repository, recover full decision context, preserve contribution and Tucker's voice, park missing firsthand details, verify the candidate and rendered exports, and deliver the result as a checked pull request. Continue ready work until the stated v1 finish line is met; report any required blocked check precisely.

A supported native Goal can use the same completion contract for continued turns. [Official Codex guidance](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) explains Goal completion criteria; [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md) explains project instructions. These files configure the work; an actual agent task must be started to execute it.
