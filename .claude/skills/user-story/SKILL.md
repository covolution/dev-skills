---
name: user-story
description: Transform rough ideas, feature descriptions, or ticket notes into well-structured Agile user stories with Given-When-Then acceptance criteria. Use this skill whenever the user mentions writing user stories, refining tickets, creating acceptance criteria, turning ideas into stories, backlog grooming, or asks to format something "as a user story." Also trigger when the user pastes a rough feature description and asks you to structure it, or mentions INVEST principles, Given-When-Then, or acceptance criteria in the context of writing stories.
---

# User Story Writer

Transform rough descriptions into well-structured user stories following Agile best practices and INVEST principles (Independent, Negotiable, Valuable, Estimable, Small, Testable).

## When to Use

- User pastes a rough idea or feature description and wants it structured
- User asks to "write a user story" or "create acceptance criteria"
- User wants to refine or improve an existing story
- User mentions backlog grooming, story writing, or ticket refinement

## Process

1. Read the user's input (pasted text, rough idea, or feature description)
2. Transform it into the structured format below
3. Present in markdown for readability in the conversation
4. Invite the user to refine — ask if anything needs adjusting (scope, role, criteria, etc.)
5. Iterate until the user is satisfied
6. Only once the user confirms they're happy (or explicitly asks for Jira), offer to push to Jira

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
- Focus on "what" not "how"

## Important Principles

- Focus on what needs to be achieved, not how it will be implemented
- Use consistent terminology throughout
- Make the story independent and deliverable within a single sprint where possible
- Do not include pleasantries or explanations outside the formatted output
- If the input is vague, make reasonable inferences but flag assumptions in the Context section
- After presenting the story, ask what the user would like to refine — don't rush to Jira or treat the first draft as final

## Jira Integration

Only offer Jira integration when the user explicitly asks to push to Jira, or confirms they're happy with the story and you're wrapping up. Do not mention Jira unprompted after the first draft.

When the user is ready:
1. Convert the output to Jira wiki markup format (as shown above)
2. Ask for the Jira project key and issue type (Story, Task, etc.) if not already known
3. Use the Jira skill to create or update the ticket
