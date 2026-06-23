---
name: work-on-ticket
description: "Start work on a Jira ticket: fetches ticket details, creates an appropriately named git branch, and summarises what needs to be done. Trigger when the user says work on PROJ-123, start PROJ-123, pick up PROJ-123, or similar phrasing with a Jira issue key."
user-invocable: true
---

# Work on Ticket

Sets up the local environment to start work on a Jira ticket — fetches the ticket, creates a
branch, and gives you a clear summary of what to do.

## When to Use This Skill

- "work on PROJ-123"
- "start work on PROJ-123"
- "pick up PROJ-123" / "begin PROJ-123"
- Any phrase combining a work-start verb with a Jira issue key (`[A-Z]+-[0-9]+`)

---

## Workflow

### 1. Parse Ticket ID

Extract the issue key from the user's message. Format: `[A-Z]+-[0-9]+` (e.g. `PROJ-123`).

If no issue key is found, ask the user for one before proceeding.

---

### 2. Fetch Ticket Details

Use the **jira skill** to fetch the ticket. Load it first if not already in context.

**acli backend:**
```bash
acli jira workitem view KEY-123 --fields "key,summary,description,issuetype,status,assignee,priority"
```

**MCP backend:**
```
mcp__atlassian__getJiraIssue(issueKey: "KEY-123")
```

Extract: summary, description, issue type, status, assignee, acceptance criteria (if present).

If the ticket is not found, inform the user and **STOP** — do not proceed to branch creation.

---

### 3. Generate Branch Name

Format: `[TICKET-ID]-[kebab-case-summary]`

Rules:
- Lowercase
- Replace spaces and special characters with `-`
- Strip punctuation
- Max 60 characters total (including the ticket ID prefix)
- Prefer meaningful words — drop filler words if needed

Examples:
- `PROJ-123-migrate-mcp-server`
- `PROJ-456-fix-auth-token-expiry`
- `PROJ-789-add-user-settings-page`

---

### 4. Check Git State

```bash
git branch --show-current
git status --porcelain
```

**If there are uncommitted changes:**
- STOP and inform the user
- Ask: "You have uncommitted changes. Should I commit them, stash them, or continue anyway?"
- Wait for the user's decision before proceeding

**If not on `main`:**
- STOP and inform the user
- Ask: "You're currently on `[CURRENT_BRANCH]`. Should I switch to `main` first?"
- Wait for the user's decision before proceeding

---

### 5. Create Branch

Once it is safe to proceed:

```bash
git checkout main
git pull origin main
git checkout -b [BRANCH_NAME]
```

Confirm to the user: "Created and checked out branch: `[BRANCH_NAME]`"

**If the branch already exists:**
- Inform the user: "Branch `[BRANCH_NAME]` already exists."
- Ask: "Should I check it out, create a branch with a different name, or stop?"
- Wait for the user's decision

---

### 6. Summarise the Ticket

Present a concise, actionable summary:

- **Ticket:** `KEY-123` — [summary]
- **Type / Priority:** [issue type] / [priority]
- **Status:** [current status]
- **Description:** [condensed, plain-language description]
- **Acceptance criteria:** [bulleted list if extractable, otherwise omit]
- **Suggested first step:** [one concrete action based on the ticket content]

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Ticket not found | Inform user and STOP |
| Uncommitted changes | Pause and ask how to proceed |
| Not on `main` | Pause and ask whether to switch |
| Branch already exists | Pause and ask how to proceed |
| Git command fails | Show the error and STOP |

---

## Success Criteria

1. ✅ Ticket fetched and key details extracted
2. ✅ Git state verified (clean, or user approved)
3. ✅ Branch created and checked out from `main`
4. ✅ Clear ticket summary presented to the user
