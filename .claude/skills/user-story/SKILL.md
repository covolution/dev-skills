---
name: user-story
description: Use when the user pastes a rough feature idea, ticket notes, or feature description and wants it structured; when refining or grooming backlog tickets; when creating acceptance criteria; or when the user mentions user stories, INVEST, or Given-When-Then.
---

# User Story Writer

Transform rough descriptions into well-structured user stories following Agile best practices and INVEST principles.

## Process

1. Read the user's input (pasted text, rough idea, or feature description)
2. Transform it into the structured format below, applying the INVEST checklist
3. Present in markdown for readability in the conversation
4. Invite the user to refine — ask if anything needs adjusting (scope, role, criteria, etc.)
5. Iterate until the user is satisfied
6. Only once the user confirms they're happy (or explicitly asks for Jira), offer to push to Jira

## INVEST Checklist

Apply each before presenting the story:

- **Independent** — the story can be delivered without depending on another unfinished story. Split if it can't.
- **Negotiable** — describes the need, not a locked technical solution.
- **Valuable** — the "so that" clause names a real user or business benefit.
- **Estimable** — scope is clear enough for a team to size it. Flag unknowns in Context.
- **Small** — deliverable within a single sprint. If not, propose splitting.
- **Testable** — every acceptance criterion can pass or fail objectively.

## Output Format (Conversation)

Present the story in markdown:

```
## <Title>

### Description
As a <specific user role>, I want <desired capability> so that <business value/benefit>.

**Context:**
<2-4 sentences of background, assumptions, constraints, or business rules>

### Acceptance Criteria
- **Given** <precondition>, **When** <action>, **Then** <outcome>
- **Given** <precondition>, **When** <action>, **Then** <outcome>
...
```

## Output Format (Jira)

When pushing to Jira, convert to wiki markup:

```
h2. <Title>

h3. Description
As a <specific user role>, I want <desired capability> so that <business value/benefit>.

*Context:*
<2-4 sentences of background, assumptions, constraints, or business rules>

h3. Acceptance Criteria
* *Given* <precondition>, *When* <action>, *Then* <outcome>
* *Given* <precondition>, *When* <action>, *Then* <outcome>
```

## Writing Guidelines

### Title
- Infer from the description if none provided
- Brief, action-oriented (e.g., "Enable user profile updates")
- Under 12 words
- Focus on the capability being delivered, not implementation details

### User Story Statement
- Use exactly: "As a <type of user>, I want <some goal> so that <some reason>"
- Be specific about the user role (e.g., "registered customer" not just "user")
- State the desired capability, not the technical solution
- Explain the business value clearly

### Context
- Relevant background information
- Assumptions or constraints
- Business rules or edge cases
- Keep concise: 2-4 sentences maximum

### Acceptance Criteria
- Use Given-When-Then pattern consistently
- Include 3-7 criteria covering:
  - Happy path scenarios
  - Key edge cases
  - Non-functional requirements (performance, security) if relevant
- Each criterion must be specific, measurable, and testable
- Criteria should be independent and non-overlapping
- Keep each criterion to a single When/Then — avoid compound criteria that chain multiple actions or outcomes
- Focus on "what" not "how"

## Important Principles

- Focus on what needs to be achieved, not how it will be implemented
- Use consistent terminology throughout
- Do not add preamble before the story; a brief refine/next-step prompt after it is expected
- If the input is vague, make reasonable inferences but flag assumptions in the Context section

## Common Mistakes

- **Vague role** — "As a user" instead of a specific role like "registered customer" or "account admin"
- **Solution disguised as a story** — describing the UI or implementation ("add a dropdown") instead of the need
- **Untestable criteria** — outcomes that can't objectively pass or fail ("the page is fast")
- **Only happy-path criteria** — no error, empty, or edge-case scenarios
- **Compound criteria** — one bullet chaining several When/Then steps
- **Missing business value** — a "so that" clause that just restates the action

## Example

**Input:** "users should be able to reset their password"

**Output:**

```
## Enable self-service password reset

### Description
As a registered customer, I want to reset my password from the login page so that I can regain access without contacting support.

**Context:**
Reset links must expire after 30 minutes and be single-use. Assumes email is the verified account identifier.

### Acceptance Criteria
- **Given** I am on the login page, **When** I select "Forgot password" and submit a registered email, **Then** a reset link is sent to that email
- **Given** I submit an email not on file, **When** I request a reset, **Then** I see the same confirmation message (no account disclosure)
- **Given** I open a reset link older than 30 minutes, **When** the page loads, **Then** I see an "expired link" message and an option to request a new one
- **Given** I set a new password meeting policy, **When** I submit, **Then** my password is updated and I am signed in
```

## Jira Integration

Only offer Jira integration when the user explicitly asks to push to Jira, or confirms they're happy with the story and you're wrapping up. Do not mention Jira unprompted after the first draft.

When the user is ready:
1. Confirm a Jira integration (skill or MCP tool) is available. If none is available, output the wiki markup for the user to paste manually and stop.
2. Convert the output to Jira wiki markup format (as shown above)
3. Ask for the Jira project key and issue type (Story, Task, etc.) if not already known
4. Create or update the ticket via the available Jira integration
