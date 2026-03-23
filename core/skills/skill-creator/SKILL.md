---
name: skill-creator
description: Interactive guide for creating new Claude skills from scratch. Walks through use case definition, SKILL.md authoring, frontmatter generation, reference file design, and quality validation. Use when asked to "create a skill", "build a skill", "make a new skill", "help me write a skill", "design a skill for", "turn this workflow into a skill", or "improve this skill".
license: MIT
metadata:
  author: claude-universal-config
  version: "1.0"
  category: meta
---

# Skill Creator

Interactive guide that helps you build a high-quality Claude skill in one sitting.
A skill is a folder with `SKILL.md` (required) + optional `references/`, `scripts/`, `assets/`.

Before starting, decide: are you **creating** a new skill, or **reviewing/improving** an existing one?

---

## Phase 1: Gather Requirements

Ask the user (or infer from context) the following. Confirm before proceeding.

**1. What problem does this skill solve?**
- What repeatable workflow will it automate?
- Who uses it — individual, team, or external users?

**2. Identify 2–3 concrete use cases**
For each use case, define:
```
Trigger: What does the user say / what situation triggers this?
Steps:   What multi-step process does Claude need to follow?
Result:  What does success look like?
```

**3. What tools are needed?**
- Claude built-in only (Read, Write, Bash, WebFetch, etc.)
- MCP server? If yes, which one and which tools?

**4. What domain knowledge should be embedded?**
- Rules, constraints, best practices the user knows but Claude doesn't
- Common errors to avoid
- Output quality standards

**5. Choose a pattern** (consult `references/patterns.md`):
- Sequential workflow → ordered steps with validation gates
- Multi-MCP coordination → phases across multiple services
- Iterative refinement → quality loop until threshold met
- Context-aware tool selection → decision tree based on input
- Domain-specific intelligence → embed compliance/expertise logic

---

## Phase 2: Design the Frontmatter

The frontmatter is the most critical part — it controls when Claude loads the skill.

**Required structure:**
```yaml
---
name: your-skill-name-in-kebab-case
description: [What it does]. Use when [specific trigger phrases users say].
---
```

**Rules (consult `references/frontmatter-guide.md` for full spec):**
- `name`: kebab-case, no spaces, no capitals, no "claude"/"anthropic" prefix
- `description`: MUST include WHAT + WHEN. Under 1024 chars. No XML tags (< >).
- Good description formula: `[Capability summary]. Use when user [verb phrases] or asks to [action phrases].`

**Draft the description with the user.** Show them:
```
Too vague:   "Helps with projects."
Too narrow:  "Creates Notion databases."  (no triggers)
Good:        "Sets up Notion project workspaces including pages, databases, and
              templates. Use when user says 'set up a project', 'create workspace',
              'initialize Notion project', or 'new project in Notion'."
```

**Optional fields to add if relevant:**
```yaml
license: MIT
metadata:
  author: Name
  version: "1.0"
  mcp-server: server-name   # if MCP-dependent
```

---

## Phase 3: Write the SKILL.md Body

After the frontmatter, write the actual instructions in Markdown.

**Standard structure:**

```markdown
# Skill Name

One-sentence summary of what this skill does.

## Instructions

### Step 1: [First action]
[Clear explanation. What Claude should do, check, or call.]

Expected output: [Describe what success looks like]

### Step 2: [Next action]
...

## Examples

### Example 1: [Common scenario]
User says: "..."
Actions:
1. ...
2. ...
Result: ...

## Common Issues

### [Error or edge case]
Cause: [Why it happens]
Solution: [How to fix it]
```

**Writing rules:**
- Be specific and actionable — no vague verbs like "validate properly"
- Put CRITICAL instructions near the top, use `## IMPORTANT` if needed
- For critical validations, bundle a script in `scripts/` rather than relying on language
- Keep SKILL.md under 5,000 words — move detailed docs to `references/`
- Reference bundled files explicitly: `Consult references/api-guide.md for rate limits`

---

## Phase 4: Design Reference Files (if needed)

Move detailed content to `references/` to minimize tokens loaded at startup.

Good candidates for `references/`:
- API patterns, rate limits, error codes
- Domain-specific rules (compliance, style guides)
- Large example libraries
- Step-by-step sub-workflows

Reference each file explicitly in SKILL.md:
```markdown
Before proceeding, consult `references/api-patterns.md` for:
- Authentication requirements
- Pagination handling
- Error codes and retry logic
```

---

## Phase 5: Validate and Output

Run the quality checklist from `references/quality-checklist.md` before outputting files.

Then output:

1. **The complete folder structure** as a tree
2. **SKILL.md** — full content, ready to save
3. **Each reference file** — if applicable
4. **Suggested test cases** — 3 should-trigger + 3 should-NOT-trigger queries
5. **Installation instructions**:
   - Place the folder in `.claude/skills/<skill-name>/`
   - Or run `python cli/generate.py claude-config.yaml .` if using claude-universal-config

---

## Phase 6: Improvement Mode

If the user provides an existing skill to improve:

1. Read the current SKILL.md carefully
2. Identify issues using `references/troubleshooting.md`
3. Check triggering: Is the description specific enough? Does it include trigger phrases?
4. Check instructions: Are they actionable? Is there error handling?
5. Check structure: Is content too large for SKILL.md? Should some move to references/?
6. Output the improved version with a diff summary of changes made

---

## References

- `references/frontmatter-guide.md` — Complete YAML field spec, security rules, examples
- `references/patterns.md` — 5 proven workflow patterns with examples
- `references/quality-checklist.md` — Pre/during/post-upload validation checklist
- `references/troubleshooting.md` — Common errors and fixes
