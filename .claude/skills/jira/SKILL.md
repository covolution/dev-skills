---
name: jira
description: Use this skill for anything involving Jira - viewing tickets, searching issues, checking sprint status, creating/updating issues, transitioning statuses, adding comments, or linking tickets. Trigger on any mention of jira, ticket, issue, sprint, backlog, story, epic, or bug. If the user mentions Jira in passing or drops an issue key like PROJ-123, use this skill.
---

# Jira

Natural language Jira interaction using the official Atlassian CLI (`acli`) or Atlassian MCP tools.

## Backend Detection

Run this check first before any Jira operation:

```
1. Check if Atlassian CLI is available:
   → Run: which acli
   → If found: USE ACLI BACKEND

2. If no acli, check for Atlassian MCP:
   → Look for mcp__atlassian__* tools
   → If available: USE MCP BACKEND

3. If neither available:
   → GUIDE USER TO SETUP (see bottom of this file)
```

| Backend | When to use | Reference |
|---------|-------------|-----------|
| **acli** | `acli` command found | `references/commands.md` |
| **MCP** | `mcp__atlassian__*` tools available | `references/mcp.md` |
| **None** | Neither found | Guide to install acli |

---

## Quick Reference — acli

> Skip if using MCP backend.

| Intent | Command |
|--------|---------|
| View issue | `acli jira workitem view KEY-123` |
| Search by JQL | `acli jira workitem search --jql "assignee = currentUser()"` |
| Search with output fields | `acli jira workitem search --jql "..." --fields "key,summary,status,assignee"` |
| Create issue | `acli jira workitem create --summary "..." --project "PROJ" --type "Task"` |
| Edit issue | `acli jira workitem edit --key "KEY-123" --summary "..."` |
| Transition issue | `acli jira workitem transition --key "KEY-123" --status "Done"` |
| Assign to me | `acli jira workitem assign --key "KEY-123" --assignee "@me"` |
| Add comment | `acli jira workitem comment create --key "KEY-123" --body "..."` |
| List comments | `acli jira workitem comment list --key "KEY-123"` |
| Open in browser | `acli jira workitem view KEY-123 --web` |
| Board issues (Kanban) | `acli jira workitem search --jql "project = PROJ AND statusCategory != Done ORDER BY updated DESC"` |
| In progress (Kanban) | `acli jira workitem search --jql "project = PROJ AND statusCategory = 'In Progress' ORDER BY updated DESC"` |
| Sprint issues (Scrum only) | `acli jira sprint list-workitems --sprint <id> --board <id>` |
| List projects | `acli jira project list` |
| Auth status | `acli jira auth status` |

---

## Quick Reference — MCP

> Skip if using acli backend.

| Intent | MCP Tool |
|--------|----------|
| Search issues (JQL) | `mcp__atlassian__searchJiraIssuesUsingJql` |
| View issue | `mcp__atlassian__getJiraIssue` |
| Create issue | `mcp__atlassian__createJiraIssue` |
| Update issue | `mcp__atlassian__editJiraIssue` |
| Get transitions | `mcp__atlassian__getTransitionsForJiraIssue` |
| Transition | `mcp__atlassian__transitionJiraIssue` |
| Add comment | `mcp__atlassian__addCommentToJiraIssue` |
| User lookup | `mcp__atlassian__lookupJiraAccountId` |
| List projects | `mcp__atlassian__getVisibleJiraProjects` |

See `references/mcp.md` for full MCP patterns and JQL reference.

---

## Issue Key Detection

Issue keys match `[A-Z]+-[0-9]+` (e.g., PROJ-123, ABC-42).

When the user mentions an issue key, immediately fetch it:
- **acli:** `acli jira workitem view KEY-123`
- **MCP:** `mcp__atlassian__getJiraIssue(issueKey: "KEY-123")`

---

## Workflow — Viewing & Searching

For simple fetches and searches the Quick Reference above is sufficient — no need to load the reference files.

**View a specific ticket:** Fetch it, then present the key fields clearly — summary, status, assignee, description, and recent comments.

**Search / list tickets:**
1. Identify filters from the user's request (project, status, assignee, text)
2. **Kanban boards:** Do NOT use `sprint in openSprints()` — use `project` + `status`/`statusCategory` filters instead
   - Active work: `project = PROJ AND statusCategory != Done ORDER BY updated DESC`
   - By column: `project = PROJ AND status = "In Progress" ORDER BY updated DESC`
3. **Scrum boards:** Sprint filters are valid — `sprint in openSprints() AND project = PROJ`
4. Build the JQL query (see `references/mcp.md` for JQL patterns — the JQL syntax is the same for both backends)
5. Run: `acli jira workitem search --jql "<query>" --fields "key,summary,status,assignee,priority"`
6. Present results in a readable summary

---

## Workflow — Adding Comments

1. If the issue key isn't already known, ask for it or search for the ticket
2. Show the user a draft of the comment before posting
3. Get confirmation, then add the comment:
   - **acli:** `acli jira workitem comment create --key "KEY-123" --body "..."`
   - For long multi-line comments, write to a file and use `--body-file`
4. Confirm it was added successfully

---

## Workflow — Creating Tickets

1. Gather: project key, issue type, summary, description, assignee (if any), labels
2. Draft the ticket — show it to the user for review
3. Create:
   - **acli:** `acli jira workitem create --summary "..." --project "PROJ" --type "Bug"`
   - For multi-line descriptions, write to a file and use `--description-file`
4. Return the new issue key

---

## Workflow — Updating & Transitioning

1. Fetch current state first — never assume status, assignee, or description
2. Show current → proposed changes and get approval
3. For transitions, `acli` takes the status name directly (no transition ID needed):
   - `acli jira workitem transition --key "KEY-123" --status "In Progress"`
4. Verify after applying

---

## Safety Rules

These exist because Jira has limited undo and changes notify watchers.

- **Always fetch before editing** — never assume the current state
- **Always show before posting** — preview comments, transitions, and edits, then confirm
- **Always use `--yes` only when the user has already confirmed** — the CLI prompts by default, which is the right behavior
- **Never create an issue without explicit user confirmation** — always show the full draft (summary, type, project, description) and wait for approval before running `create`
- **Never bulk-modify without explicit approval** — each change notifies watchers
- **Never edit description without showing original** — Jira has no undo
- **Transition names vary per project** — if a transition fails, ask the user what state names their project uses

---

## When to Load Reference Files

| Task | Load? |
|------|-------|
| View / list issues | No — Quick Reference is sufficient |
| Add a comment | No — Quick Reference is sufficient |
| Creating with multi-line description | **Yes** — `references/commands.md` (file-based pattern) |
| Complex JQL queries | **Yes** — `references/mcp.md` JQL section (JQL is the same for both backends) |
| Linking issues | **Yes** — `references/commands.md` |
| Auth setup or troubleshooting | **Yes** — `references/commands.md` auth section |

---

## No Backend Available

If neither `acli` nor MCP is available:

```
To use Jira, install the official Atlassian CLI:

  brew tap atlassian/homebrew-acli
  brew install acli

Then authenticate:

  acli jira auth login --web        # OAuth (recommended)
  # or
  echo <token> | acli jira auth login --site "yoursite.atlassian.net" \
    --email "you@example.com" --token

Generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens

Alternatively, configure the Atlassian MCP server in your MCP settings.
```
