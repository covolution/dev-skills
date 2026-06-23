# Commands Reference

Complete reference for the official Atlassian CLI (`acli`).
Install: `brew tap atlassian/homebrew-acli && brew install acli`
Docs: https://developer.atlassian.com/cloud/acli/reference/commands/

---

## Authentication

```bash
# OAuth login (recommended — opens browser)
acli jira auth login --web

# API token login
echo <token> | acli jira auth login \
  --site "yoursite.atlassian.net" \
  --email "you@example.com" \
  --token

# Read token from file
acli jira auth login \
  --site "yoursite.atlassian.net" \
  --email "you@example.com" \
  --token < token.txt

# Check current auth status
acli jira auth status

# Logout
acli jira auth logout

# Switch between accounts
acli jira auth switch
```

Generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens

---

## Viewing Issues

```bash
# View a work item (default fields: key, issuetype, summary, status, assignee, description)
acli jira workitem view KEY-123

# View specific fields
acli jira workitem view KEY-123 --fields "key,summary,status,assignee,description,comment"

# View all fields
acli jira workitem view KEY-123 --fields "*all"

# View as JSON
acli jira workitem view KEY-123 --json

# Open in browser
acli jira workitem view KEY-123 --web
```

---

## Searching Issues

```bash
# Search with JQL (default fields: issuetype, key, assignee, priority, status, summary)
acli jira workitem search --jql "project = PROJ"

# Specify output fields
acli jira workitem search \
  --jql "assignee = currentUser() AND status != Done" \
  --fields "key,summary,status,assignee,priority"

# Limit results
acli jira workitem search --jql "project = PROJ" --limit 20

# Paginate through all results
acli jira workitem search --jql "project = PROJ" --paginate

# Count only
acli jira workitem search --jql "project = PROJ" --count

# CSV output
acli jira workitem search --jql "project = PROJ" --csv

# JSON output
acli jira workitem search --jql "project = PROJ" --json

# Search using a saved filter ID
acli jira workitem search --filter 10001

# Open results in browser
acli jira workitem search --jql "project = PROJ" --web
```

### Common JQL patterns

```jql
# My open issues
assignee = currentUser() AND status NOT IN (Done, Closed)

# My in-progress issues
assignee = currentUser() AND status = "In Progress"

# Bugs this week, by priority
issuetype = Bug AND created >= startOfWeek() ORDER BY priority DESC

# Current sprint
sprint in openSprints() AND project = PROJ

# Unassigned high-priority bugs
issuetype = Bug AND assignee IS EMPTY AND priority >= High ORDER BY created DESC

# Recently updated by me
updatedBy = currentUser() AND updated >= -7d ORDER BY updated DESC

# Issues I'm watching
watcher = currentUser()
```

See `references/mcp.md` for the full JQL field/operator reference — JQL syntax is identical for both backends.

---

## Creating Issues

```bash
# Minimal creation
acli jira workitem create \
  --summary "Fix login button on Safari" \
  --project "PROJ" \
  --type "Bug"

# With assignee and labels
acli jira workitem create \
  --summary "Add export feature" \
  --project "PROJ" \
  --type "Story" \
  --assignee "user@example.com" \
  --label "backend,api"

# Self-assign
acli jira workitem create \
  --summary "Investigate auth issue" \
  --project "PROJ" \
  --type "Task" \
  --assignee "@me"

# With inline description
acli jira workitem create \
  --summary "Fix null pointer in payment service" \
  --project "PROJ" \
  --type "Bug" \
  --description "NPE thrown when cart is empty at checkout"

# Multi-line description — write to a file first
cat > /tmp/jira_desc.txt <<'EOF'
## Problem
Users see a blank screen after login on Safari 16+.

## Steps to reproduce
1. Open Safari 16
2. Log in with any valid account
3. Observe blank screen

## Expected
Dashboard should load.
EOF

acli jira workitem create \
  --summary "Blank screen after login on Safari" \
  --project "PROJ" \
  --type "Bug" \
  --description-file /tmp/jira_desc.txt

# Create subtask (requires parent)
acli jira workitem create \
  --summary "Write unit tests for auth" \
  --project "PROJ" \
  --type "Subtask" \
  --parent "PROJ-123"

# Create from a JSON file
acli jira workitem create --from-json workitem.json

# Generate a template JSON file to fill in
acli jira workitem create --generate-json

# Open text editor for summary and description
acli jira workitem create --editor
```

---

## Editing Issues

```bash
# Update summary
acli jira workitem edit --key "PROJ-123" --summary "Updated summary"

# Update assignee
acli jira workitem edit --key "PROJ-123" --assignee "user@example.com"

# Self-assign
acli jira workitem edit --key "PROJ-123" --assignee "@me"

# Remove assignee
acli jira workitem edit --key "PROJ-123" --remove-assignee

# Update description inline
acli jira workitem edit --key "PROJ-123" --description "New description text"

# Update description from file (use for multi-line)
acli jira workitem edit --key "PROJ-123" --description-file /tmp/new_desc.txt

# Update labels
acli jira workitem edit --key "PROJ-123" --labels "backend,urgent"

# Remove labels
acli jira workitem edit --key "PROJ-123" --remove-labels "urgent"

# Edit multiple issues (confirm with --yes to skip prompts)
acli jira workitem edit --key "PROJ-123,PROJ-124" --assignee "user@example.com" --yes

# Edit issues matching a JQL query
acli jira workitem edit --jql "project = PROJ AND status = 'To Do'" \
  --assignee "user@example.com" --yes
```

---

## Transitioning Issues

```bash
# Transition by status name (acli handles the transition ID lookup automatically)
acli jira workitem transition --key "PROJ-123" --status "In Progress"
acli jira workitem transition --key "PROJ-123" --status "Done"
acli jira workitem transition --key "PROJ-123" --status "To Do"

# Skip confirmation prompt
acli jira workitem transition --key "PROJ-123" --status "Done" --yes

# Transition multiple issues
acli jira workitem transition --key "PROJ-123,PROJ-124" --status "Done" --yes

# Transition issues matching a JQL query
acli jira workitem transition \
  --jql "project = PROJ AND assignee = currentUser() AND status = 'In Progress'" \
  --status "In Review" --yes
```

> **Note:** Status names vary per project. If a transition fails, check the available states with `acli jira workitem view KEY-123` or ask the user what their workflow states are called.

---

## Assigning Issues

```bash
# Assign to a user by email
acli jira workitem assign --key "PROJ-123" --assignee "user@example.com"

# Self-assign
acli jira workitem assign --key "PROJ-123" --assignee "@me"

# Assign to project default assignee
acli jira workitem assign --key "PROJ-123" --assignee "default"

# Remove assignee
acli jira workitem assign --key "PROJ-123" --remove-assignee

# Assign via JQL
acli jira workitem assign \
  --jql "project = PROJ AND status = 'To Do' AND assignee IS EMPTY" \
  --assignee "@me" --yes
```

---

## Comments

```bash
# Add a comment
acli jira workitem comment create --key "PROJ-123" --body "This is my comment"

# Multi-line comment — write to a file first
cat > /tmp/jira_comment.txt <<'EOF'
Investigated today. Root cause is in the auth middleware.

Next steps:
- Fix the token validation logic
- Add a regression test
EOF

acli jira workitem comment create --key "PROJ-123" --body-file /tmp/jira_comment.txt

# Comment on issues matching a JQL query
acli jira workitem comment create \
  --jql "project = PROJ AND status = Done AND updated <= -7d" \
  --body "Closing as stale"

# Open editor to write the comment
acli jira workitem comment create --key "PROJ-123" --editor

# Edit the last comment you wrote on an issue
acli jira workitem comment create --key "PROJ-123" --body "Updated comment" --edit-last

# List comments on an issue
acli jira workitem comment list --key "PROJ-123"
```

---

## Linking Issues

```bash
# Link two issues (KEY-123 blocks KEY-456)
acli jira workitem link create --out "PROJ-123" --in "PROJ-456" --type "Blocks"

# General relationship
acli jira workitem link create --out "PROJ-123" --in "PROJ-456" --type "Relates"

# Skip confirmation
acli jira workitem link create --out "PROJ-123" --in "PROJ-456" --type "Blocks" --yes

# Get available link types for your instance
acli jira workitem link type

# List existing links on an issue
acli jira workitem link list --key "PROJ-123"

# Create multiple links from a JSON file
acli jira workitem link create --from-json links.json

# Generate a template JSON file for bulk linking
acli jira workitem link create --generate-json
```

> **Note:** Link type names (`Blocks`, `Relates`, `Duplicates`, etc.) vary per Jira instance.
> Run `acli jira workitem link type` to see what's available on your site.

---

## Sprints

```bash
# List work items in a sprint (requires both --sprint and --board IDs)
acli jira sprint list-workitems --sprint 1 --board 6

# With JQL filter
acli jira sprint list-workitems --sprint 1 --board 6 \
  --jql "assignee = currentUser()"

# Custom fields output
acli jira sprint list-workitems --sprint 1 --board 6 \
  --fields "key,summary,status,assignee,priority"

# Paginate through all results
acli jira sprint list-workitems --sprint 1 --board 6 --paginate
```

> **Tip:** If you don't know the sprint or board IDs, search for in-progress work using JQL instead:
> `acli jira workitem search --jql "sprint in openSprints() AND project = PROJ"`
> 
> **Kanban boards:** Don't use `sprint in openSprints()` — use status/statusCategory filters instead:
> `acli jira workitem search --jql "project = PROJ AND statusCategory != Done ORDER BY updated DESC"`

---

## Projects

```bash
# List projects
acli jira project list

# View a project
acli jira project view PROJ
```

---

## Other Useful Commands

```bash
# Clone a work item
acli jira workitem clone --key "PROJ-123"

# Archive a work item
acli jira workitem archive --key "PROJ-123"

# Delete a work item
acli jira workitem delete --key "PROJ-123"

# List attachments
acli jira workitem attachment-list --key "PROJ-123"

# Check acli version
acli --version
```
