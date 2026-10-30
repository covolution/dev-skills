# SonarQube API Reference (`sonar api`)

Load this when the typed `sonar list` commands can't express the query — quality
gates, new-code-period filtering, coverage/duplication measures, and hotspots.

## How `sonar api` works

```
sonar api <method> "<endpoint>"
sonar api get "/api/system/status"
sonar api get "/api/issues/search?componentKeys=VENG:foo&ps=10"
sonar api post "/api/issues/do_transition" --data '{"issue":"AY..","transition":"accept"}'
```

- Authenticated automatically from the keychain (`sonar auth login`). **Never pass a
  token.**
- For this skill, use **`get` only** (read-only). `post`/`put`/`delete` mutate state
  and require explicit user confirmation — out of scope for normal reporting.
- Add `--verbose` (`-v`) to debug the request/response.
- Returns the raw JSON from the SonarQube Web API.
---
## Useful Read Endpoints

| Need | Endpoint |
|------|----------|
| Quality gate for a branch | `/api/qualitygates/project_status?projectKey=<key>&branch=<branch>` |
| Quality gate for a PR | `/api/qualitygates/project_status?projectKey=<key>&pullRequest=<id>` |
| Issue search | `/api/issues/search?componentKeys=<key>&resolved=false&...` |
| New issues only | add `&inNewCodePeriod=true` to issue search |
| Filter issue search | `&severities=`, `&statuses=`, `&types=`, `&rules=`, `&branch=`, `&pullRequest=` |
| Measures (coverage, etc.) | `/api/measures/component?component=<key>&metricKeys=coverage,duplicated_lines_density,bugs,vulnerabilities,code_smells,ncloc&branch=<branch>` |
| New-code measures | use `new_coverage`, `new_violations`, `new_duplicated_lines_density` metric keys |
| List branches | `/api/project_branches/list?project=<key>` |
| List PRs | `/api/project_pull_requests/list?project=<key>` |
| Security hotspots | `/api/hotspots/search?projectKey=<key>&branch=<branch>` |
| Project list | `/api/projects/search?q=<text>` |
| Rule detail | `/api/rules/show?key=java:S1192` |

Common metric keys for `/api/measures/component`: `coverage`, `new_coverage`,
`duplicated_lines_density`, `new_duplicated_lines_density`, `bugs`,
`vulnerabilities`, `code_smells`, `security_hotspots`, `ncloc`,
`sqale_index` (technical debt), `reliability_rating`, `security_rating`.

---
## Pagination

Issue/project search returns `paging: { pageIndex, pageSize, total }`. If
`total > pageSize`, increase `ps` (max 500) or iterate `p=1,2,...`. The Web API
caps total results at 10,000 — narrow with filters rather than deep paging.

---

## Branch Quality Report

The canonical report: quality gate result + the new violations introduced on a
branch.

### Step 1 — Quality gate status

```
sonar api get "/api/qualitygates/project_status?projectKey=VENG:vehicle-tax-rate-service&branch=feature/VPASW-9781-reduce-cognitive-complexity"

Map `metricKey` → friendly name, `comparator`+`errorThreshold` → threshold
(`LT`→`≥`, `GT`→`≤`), and `status` → ✅ OK / ❌ ERROR.
```
### Step 2 — New violations on the branch

```
sonar api get "/api/issues/search?componentKeys=VENG:vehicle-tax-rate-service&branch=feature/VPASW-9781-reduce-cognitive-complexity&resolved=false&inNewCodePeriod=true&ps=10"
```

Key parameters:

| Param | Meaning |
|-------|---------|
| `componentKeys` | Project key |
| `branch` | Branch name (URL-encode if it contains special chars) |
| `resolved=false` | Only unresolved issues |
| `inNewCodePeriod=true` | Restrict to the new code period (new violations only) |
| `ps` | Page size (max 500) |
| `p` | Page number |

Each `issues[]` entry contains: `severity`, `rule` (e.g. `java:S1192`), `component`
(`project:path/File.java`), `line`, and `message`. Use these for the violations
table.

If all new violations trace back to a merged PR rather than the branch's own
changes, add an explanatory note (compare against the base branch / `main` issues to
confirm).

---

## Tips

- URL-encode branch names with `/` only if the shell or CLI mishandles them; `sonar
  api` generally accepts them as-is inside the quoted endpoint.
- Use `--verbose` to inspect the exact URL and status code when a query returns
  unexpectedly empty results (often a wrong `projectKey` or `branch`).
- A 404 / empty `conditions` usually means the branch hasn't been analysed yet, or
  the branch name doesn't match what SonarQube recorded — check
  `/api/project_branches/list`.
