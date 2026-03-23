# Troubleshooting Guide

Common problems when building and deploying skills, with root causes and fixes.

---

## Skill Won't Load / Upload Errors

### "Invalid YAML frontmatter"
**Cause:** Malformed YAML syntax in the `---` block.
**Fix:**
- Check for unquoted colons: `description: Handles: retry logic` → `description: "Handles: retry logic"`
- Check for missing closing `---` delimiter
- Remove XML angle brackets (`<` or `>`) — these are forbidden in frontmatter
- Validate with: paste your frontmatter into a YAML linter (e.g., yamllint.com)

### "Name already taken" / naming conflict
**Cause:** Another skill has the same `name` value.
**Fix:** Choose a more specific name. Use the domain + action pattern:
- `project-setup` → `notion-project-setup`
- `review` → `swift-code-review`

### Skill folder is ignored
**Cause:** File is not named exactly `SKILL.md` (case-sensitive).
**Fix:** Rename to exactly `SKILL.md` — not `skill.md`, `SKILL.MD`, or `Skill.md`.

---

## Skill Doesn't Trigger

### Skill never auto-loads
**Symptom:** You invoke the relevant workflow but Claude doesn't use the skill.
**Root cause:** Description is too vague or missing trigger phrases.

**Diagnosis:** Ask Claude directly:
> "When would you use the [skill-name] skill?"

Claude will quote the description back — you'll see exactly what's missing.

**Fix:** Add explicit trigger phrases to the description:
```yaml
# Before (too vague):
description: Helps with code review tasks.

# After (specific triggers):
description: Performs structured code review for Python and TypeScript projects.
  Use when user asks to "review this code", "check my PR", "code review",
  "look over this function", or pastes code and asks for feedback.
```

**Checklist for under-triggering:**
- [ ] Description includes 3–5 literal phrases users actually say
- [ ] Description includes domain-specific terms (e.g., "Linear", "Figma", "sprint")
- [ ] Description mentions the outcome, not just the mechanism

### Skill triggers on wrong queries
**Symptom:** Skill loads for unrelated requests.
**Fix:** Narrow the description scope:
```yaml
# Add negative scoping:
description: Manages Linear sprint planning. Use when user mentions "sprint",
  "Linear tasks", or "create tickets". Do NOT use for general task management
  or other project management tools.
```

---

## Instructions Not Followed

### Claude skips steps
**Cause:** Instructions are too far down in SKILL.md or buried in prose.
**Fix:**
- Move critical instructions to the top of SKILL.md
- Use `## IMPORTANT` heading for mandatory steps
- Use numbered lists instead of paragraphs for sequences

```markdown
## IMPORTANT

Before any other action:
1. Confirm the user's environment (staging vs. production)
2. Verify required MCP server is connected
3. Read current state before writing

Only proceed after all 3 checks pass.
```

### Claude interprets instructions loosely
**Cause:** Vague language like "validate properly", "ensure quality", "handle errors".
**Fix:** Replace every vague instruction with a concrete one:

| Vague | Specific |
|---|---|
| "Validate the input" | "Check that `user_id` is a non-empty string matching `/^[a-z0-9-]+$/`" |
| "Handle errors gracefully" | "On HTTP 429: wait 5s, retry once. On HTTP 5xx: log and ask user to retry." |
| "Format the output nicely" | "Output as a Markdown table with columns: Name, Status, Updated" |

### MCP tool called with wrong parameters
**Cause:** Skill doesn't specify exact parameter names.
**Fix:** Include explicit parameter mapping in instructions:
```markdown
Call: `mcp_linear_create_issue` with:
- title: [use the user's task description verbatim]
- teamId: [from Step 1 output]
- priority: 2 (medium, unless user specifies)
- description: [include acceptance criteria from the spec]
```

---

## MCP Connection Issues

### "MCP server not available"
**Cause:** The MCP server the skill depends on isn't running or configured.
**Fix in SKILL.md:** Add a pre-flight check at the top:
```markdown
## Pre-flight Check

Before starting, verify the required MCP server is available:
- If Linear MCP is unavailable: inform the user and stop
- If unavailable: suggest running `npx @linear/mcp-server` or checking MCP config
```

### MCP tools return unexpected data
**Cause:** API schema changed or wrong tool version.
**Fix:** Add explicit output validation in the skill:
```markdown
### Step 2: Validate MCP Response
After calling `mcp_tool_name`, verify the response contains:
- `id` field (string)
- `status` field (one of: "active", "archived", "draft")

If validation fails: log the raw response and ask the user to check their MCP version.
```

---

## Large Context / Performance Issues

### Skill exceeds token limits
**Symptom:** Skill causes context overflow; Claude truncates instructions.
**Fix:**
- Move anything over 500 words to `references/` files
- Link explicitly: `Consult references/api-patterns.md for rate limit details`
- Never inline large example libraries or API docs directly in SKILL.md

**Target sizes:**
- SKILL.md body: under 2,000 words for common cases, max 5,000
- Each reference file: focused on one topic, under 1,000 words ideally

### Reference files not being read
**Cause:** Skill says "see references/" but doesn't give Claude a clear signal to fetch them.
**Fix:** Use imperative language with the exact filename:
```markdown
# Weak (Claude may skip):
"See references/ for more details."

# Strong (Claude will fetch):
"Before proceeding to Step 3, read references/api-patterns.md.
Pay special attention to the rate limit and pagination sections."
```

---

## Output Quality Issues

### Skill produces inconsistent results
**Cause:** No output format specified.
**Fix:** Add an explicit output template to SKILL.md:
```markdown
## Output Format

Always produce output in this exact structure:
---
## Summary
[1–2 sentence outcome]

## Changes Made
- [Action 1]: [result]
- [Action 2]: [result]

## Next Steps
1. [Immediate next action for the user]
---
```

### Skill works once but not on repeat use
**Cause:** Skill depends on session state that doesn't persist.
**Fix:**
- Don't reference "what we did last time" in instructions
- Make each invocation self-contained
- If state matters, require the user to provide it as input

---

## Quick Diagnosis Checklist

When a skill isn't working as expected, run through this in order:

1. **Won't load?** → Check YAML syntax, file name, forbidden characters
2. **Doesn't trigger?** → Ask Claude "when would you use [skill]?" — add missing triggers
3. **Triggers wrong?** → Add "Do NOT use for X" negative scoping
4. **Steps skipped?** → Move critical instructions up, use numbered lists
5. **Wrong tool params?** → Add explicit parameter mapping per tool call
6. **MCP errors?** → Add pre-flight availability check
7. **Context overflow?** → Move content to references/, check file sizes
8. **Bad output format?** → Add explicit output template
