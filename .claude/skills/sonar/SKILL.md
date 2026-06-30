---
name: sonar
description: Use this skill for anything involving SonarQube or code quality on the self-hosted DVLA server (https://sonarqube.tooling.dvla.gov.uk/). Trigger on mentions of sonar, sonarqube, code quality, quality gate, coverage, code smells, vulnerabilities, hotspots, technical debt, or a SonarQube project key like VENG:vehicle-tax-rate-service. Covers discovering projects, searching issues, checking quality gates, and building branch quality reports.
---

# SonarQube

Query the self-hosted SonarQube server using the official SonarQube CLI (`sonar`).

**Server:** `https://sonarqube.tooling.dvla.gov.uk/`

## Setup Check

Before any operation, verify both — on failure, load **[references/setup.md](references/setup.md)**:

- `which sonar` — installed? If not, guide the user to install.
- `sonar auth status` — authenticated to the DVLA server? If not, ask the user to
  authenticate (agents can't — `sonar auth login` must be run by the user).

--

## Quick Reference

| Intent | Command |
|--------|---------|
| Auth status | `sonar auth status` |
| List all projects | `sonar list projects` |
| Search projects | `sonar list projects -q vehicle-tax` |
| Issues in a project | `sonar list issues -p VENG:vehicle-tax-rate-service` |
| Issues, LLM format | `sonar list issues -p <key> --format toon` |
| Filter by severity | `sonar list issues -p <key> --severities HIGH,BLOCKER` |
| Filter by status | `sonar list issues -p <key> --statuses OPEN,CONFIRMED` |
| Issues on a branch | `sonar list issues -p <key> --branch feature/VPASW-9781-...` |
| Issues on a PR | `sonar list issues -p <key> --pull-request 151` |
| Raw API call (read) | `sonar api get "/api/qualitygates/project_status?projectKey=<key>"` |
| System diagnostics | `sonar system status --json` |

`sonar list issues` filters: `--statuses`, `--severities`, `--branch`,
`--pull-request`, `--format`, `--page`, `--page-size` (1–500).

---

## Severity & Status Values

Severities (MQR mode): `INFO`, `LOW`, `MEDIUM`, `HIGH`, `BLOCKER`.
Issue statuses: `OPEN`, `CONFIRMED`, `FALSE_POSITIVE`, `ACCEPTED`, `FIXED`.

---

## Output Format Convention

- Default to `--format toon` optimised for LLM input.
- Default (no `--format`) is JSON — when you need to parse specific fields (e.g. building a report) or pipe into other commands, eg. (`jq`).

---

## Workflow — Search Issues

1. Resolve the project key if you don't already have it.
2. Apply filters from the request — severity, status, branch, PR.
3. Run, e.g.:
   ```
   sonar list issues -p VENG:vehicle-tax-rate-service \
     --severities HIGH,BLOCKER --statuses OPEN
   ```
4. Summarise: group by severity or file, and surface the rule key + message.

For **new-code-period** filtering, quality gates, or branch reports, the typed
`list issues` command is not enough — use `sonar api`. See
[references/api.md](references/api.md).

---

## Workflow — Branch Quality Report

This is the canonical report (quality gate + new violations on a branch). It
requires two `sonar api` calls. Full endpoint details, the exact queries, and the
report format are in **[references/api.md](references/api.md)** — load it whenever
the user asks for a quality gate, branch report, or "new violations".

High level:
1. `GET /api/qualitygates/project_status?projectKey=<key>&branch=<branch>`
2. `GET /api/issues/search?componentKeys=<key>&branch=<branch>&resolved=false&inNewCodePeriod=true&ps=<n>`
3. Render the gate conditions table and the new-violations table.

---

## Safety Rules

This skill is **read-only**. Stick to querying.

- **Never run `sonar auth login` yourself** — only the user can authenticate.
- **Only use `sonar api get`** for queries. Do not issue `sonar api post/put/delete`
  (which can transition issues or mutate state) unless the user explicitly asks and
  confirms.
- **Do not run `sonar integrate`, `sonar analyze`, `sonar remediate`, or
  `sonar system reset`** as part of this skill — they change local config, trigger
  scans, or alter server state.
- **Never print or store the auth token.** `sonar api` uses the keychain; you don't
  need the raw token.
- **Confirm the exact project key** before reporting — a wrong key returns empty
  results that look like "no issues".

---

## When to Load Reference Files

| Task | Load? |
|------|-------|
| List projects / simple issue search | No — Quick Reference is enough |
| Quality gate status | **Yes** — [references/api.md](references/api.md) |
| Branch quality report / new violations | **Yes** — [references/api.md](references/api.md) |
| Coverage, duplications, measures | **Yes** — [references/api.md](references/api.md) |
| Security hotspots | **Yes** — [references/api.md](references/api.md) |
| CLI install / authentication | **Yes** — [references/setup.md](references/setup.md) |
