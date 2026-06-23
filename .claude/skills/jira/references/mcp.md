# MCP Reference

Complete reference for Atlassian Jira operations via MCP tools.

---

## MCP Tool Reference

### Search Operations

#### `mcp__atlassian__searchJiraIssuesUsingJql`

Search Jira using JQL (Jira Query Language).

**Parameters:**
- `jql` (required): JQL query string
- `maxResults`: Maximum results (default: 50)
- `startAt`: Pagination offset
- `fields`: Comma-separated fields to return

**Example:**
```
mcp__atlassian__searchJiraIssuesUsingJql(
  jql: "project = PROJ AND status = 'In Progress'"
)
```

---

### Issue Operations

#### `mcp__atlassian__getJiraIssue`

Retrieve full issue details by key.

**Parameters:**
- `issueKey` (required): Issue key (e.g., "PROJ-123")
- `expand`: Additional data (changelog, transitions, renderedFields)

#### `mcp__atlassian__createJiraIssue`

Create a new issue.

**Parameters:**
- `projectKey` (required): Target project
- `issueType` (required): Issue type (Story, Bug, Task, Epic, etc.)
- `summary` (required): Issue title
- `description`: Detailed description
- `assignee`: Account ID — use `lookupJiraAccountId` first
- `priority`: Priority name (Highest, High, Medium, Low, Lowest)
- `labels`: Array of labels
- `components`: Array of component names

**Example:**
```
mcp__atlassian__createJiraIssue(
  projectKey: "PROJ",
  issueType: "Story",
  summary: "Implement user authentication",
  description: "Add OAuth2 authentication flow...",
  labels: ["backend", "security"]
)
```

#### `mcp__atlassian__editJiraIssue`

Update an existing issue.

**Parameters:**
- `issueKey` (required): Issue to update
- Any field to update (summary, description, assignee, etc.)

---

### Transition Operations

#### `mcp__atlassian__getTransitionsForJiraIssue`

Get available status transitions for an issue. Always call this before transitioning — workflow state names vary per project.

**Parameters:**
- `issueKey` (required): Issue key

**Returns:** List of available transitions with IDs and names.

#### `mcp__atlassian__transitionJiraIssue`

Change issue status.

**Parameters:**
- `issueKey` (required): Issue key
- `transitionId` (required): Transition ID from `getTransitionsForJiraIssue`
- `comment`: Optional comment for the transition

**Workflow:**
```
1. Get transitions:
   mcp__atlassian__getTransitionsForJiraIssue(issueKey: "PROJ-123")

2. Find the desired transition ID from results

3. Execute:
   mcp__atlassian__transitionJiraIssue(
     issueKey: "PROJ-123",
     transitionId: "31"
   )
```

---

### Comment Operations

#### `mcp__atlassian__addCommentToJiraIssue`

Add a comment to an issue.

**Parameters:**
- `issueKey` (required): Issue key
- `body` (required): Comment text (supports Jira markdown)

---

### User Operations

#### `mcp__atlassian__lookupJiraAccountId`

Find user account ID for assignments. Always use this before setting assignee — display names do not work for assignment.

**Parameters:**
- `query` (required): Search by display name, email, or username

**Example:**
```
mcp__atlassian__lookupJiraAccountId(query: "user@example.com")
```

---

### Project Operations

#### `mcp__atlassian__getVisibleJiraProjects`

List available Jira projects.

#### `mcp__atlassian__getJiraProjectIssueTypesMetadata`

Get issue types and required fields for a project. Call before creating issues to understand required fields.

**Parameters:**
- `projectKey` (required): Project key

#### `mcp__atlassian__getJiraIssueTypeMetaWithFields`

Get detailed field metadata for an issue type.

**Parameters:**
- `projectKey` (required): Project key
- `issueTypeId` (required): Issue type ID

---

## JQL (Jira Query Language) Reference

### Basic Syntax

```
field operator value [AND|OR field operator value]
```

### Common Fields

| Field | Description | Example |
|-------|-------------|---------|
| `project` | Project key | `project = "PROJ"` |
| `issuetype` | Issue type | `issuetype = Bug` |
| `status` | Issue status | `status = "In Progress"` |
| `assignee` | Assigned user | `assignee = currentUser()` |
| `reporter` | Issue creator | `reporter = "jsmith"` |
| `priority` | Priority level | `priority = High` |
| `labels` | Issue labels | `labels = "backend"` |
| `component` | Components | `component = "API"` |
| `created` | Creation date | `created >= -30d` |
| `updated` | Last update | `updated >= -7d` |
| `resolved` | Resolution date | `resolved >= startOfMonth()` |
| `sprint` | Sprint name/ID | `sprint in openSprints()` |
| `text` | Full-text search | `text ~ "authentication"` |
| `summary` | Title search | `summary ~ "login"` |
| `description` | Description search | `description ~ "OAuth"` |

### Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Exact match | `status = Done` |
| `!=` | Not equal | `status != Closed` |
| `~` | Contains (text) | `summary ~ "auth*"` |
| `!~` | Does not contain | `summary !~ "test"` |
| `>` `>=` `<` `<=` | Comparisons | `priority >= High` |
| `IN` | Multiple values | `status IN (Open, "In Progress")` |
| `NOT IN` | Exclude values | `status NOT IN (Done, Closed)` |
| `IS` | Null check | `assignee IS EMPTY` |
| `IS NOT` | Not null | `assignee IS NOT EMPTY` |
| `WAS` | Historical value | `status WAS "In Progress"` |
| `CHANGED` | Field changed | `status CHANGED` |

### Functions

| Function | Description | Example |
|----------|-------------|---------|
| `currentUser()` | Logged-in user | `assignee = currentUser()` |
| `now()` | Current timestamp | `created <= now()` |
| `startOfDay()` | Midnight today | `updated >= startOfDay()` |
| `startOfWeek()` | Start of week | `created >= startOfWeek()` |
| `startOfMonth()` | Start of month | `created >= startOfMonth()` |
| `openSprints()` | Active sprints | `sprint in openSprints()` |
| `closedSprints()` | Completed sprints | `sprint in closedSprints()` |

### Relative Dates

```jql
created >= -7d    # Last 7 days
updated >= -30d   # Last 30 days
created >= -2w    # Last 2 weeks
created >= -1M    # Last month
created >= "2024-01-01"  # Specific date
```

### Common Query Patterns

```jql
# My open issues, high priority
assignee = currentUser() AND status NOT IN (Done, Closed) AND priority >= High

# Bugs created this week
issuetype = Bug AND created >= startOfWeek() ORDER BY priority DESC

# Active sprint backlog
sprint in openSprints() AND status = "To Do" ORDER BY rank ASC

# Issues I'm watching
watcher = currentUser()

# Unassigned high-priority bugs
issuetype = Bug AND assignee IS EMPTY AND priority >= High

# Issues updated by me recently
updatedBy = currentUser() AND updated >= -7d ORDER BY updated DESC

# Recently resolved
resolved >= -7d AND project = PROJ ORDER BY resolved DESC

# Everything in a specific epic
"Epic Link" = PROJ-100 AND status != Done
```

---

## Issue Linking

The Atlassian MCP does not currently support creating issue links directly. Use the Jira REST API as a workaround:

```bash
# Requires environment variables:
# JIRA_BASE_URL  — e.g. https://yourcompany.atlassian.net
# JIRA_USER      — your email address
# JIRA_API_TOKEN — from Atlassian account settings

curl -s -u "$JIRA_USER:$JIRA_API_TOKEN" \
  -X POST "$JIRA_BASE_URL/rest/api/3/issueLink" \
  -H "Content-Type: application/json" \
  -d '{
    "type": {"name": "Blocks"},
    "inwardIssue": {"key": "PROJ-100"},
    "outwardIssue": {"key": "PROJ-200"}
  }'
```

**Available link type names** (check your instance):
```bash
curl -s -u "$JIRA_USER:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issueLinkType" | jq '.issueLinkTypes[].name'
```

---

## Description Formatting

### Jira Wiki Markup (older instances)

```
h1. Heading 1
*bold* _italic_ -strikethrough-

{code:java}
// code here
{code}

* Bullet list
# Numbered list
||Header 1||Header 2||
|Cell 1|Cell 2|
```

### Atlassian Document Format (ADF, newer instances)

For `createJiraIssue`, descriptions may use ADF:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Description text"}]
    }
  ]
}
```

---

## Common Workflows

### Move Ticket to Done

```
1. Get available transitions:
   mcp__atlassian__getTransitionsForJiraIssue(issueKey: "PROJ-123")

2. Find "Done" (or equivalent) transition ID

3. Execute transition:
   mcp__atlassian__transitionJiraIssue(
     issueKey: "PROJ-123",
     transitionId: "<id>"
   )

4. Optionally add a comment:
   mcp__atlassian__addCommentToJiraIssue(
     issueKey: "PROJ-123",
     body: "Completed and deployed"
   )
```

### Create and Assign Issue

```
1. Look up user account ID:
   mcp__atlassian__lookupJiraAccountId(query: "john@example.com")

2. Create issue with assignment:
   mcp__atlassian__createJiraIssue(
     projectKey: "PROJ",
     issueType: "Task",
     summary: "Implement feature X",
     description: "Details here...",
     assignee: "<account_id_from_step_1>"
   )
```

---

## Error Handling

| HTTP Code | Error | Cause | Resolution |
|-----------|-------|-------|------------|
| 400 | Bad Request | Invalid field values | Check required fields for issue type |
| 401 | Unauthorized | Invalid credentials | Reconnect Atlassian MCP (`/mcp`) |
| 403 | Forbidden | Insufficient permissions | Check project permissions |
| 404 | Not Found | Issue/project doesn't exist | Verify key is correct |
| 422 | Unprocessable | Validation failed | Check field constraints |

**Authentication issues:** Run `/mcp` to check connection status and reconnect the Atlassian MCP service if disconnected. Verify API token permissions in Atlassian account settings.

**Field validation:** Before creating issues, call `getJiraProjectIssueTypesMetadata` to discover required fields and valid values for the target project.
