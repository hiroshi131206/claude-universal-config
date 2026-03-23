# YAML Frontmatter Reference

The frontmatter is how Claude decides whether to load your skill. It is always
loaded into the system prompt — this is level 1 of progressive disclosure.

## Minimal Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

## All Fields

```yaml
---
name: skill-name-in-kebab-case          # REQUIRED
description: Full description here.     # REQUIRED (see below)
license: MIT                            # Optional: MIT, Apache-2.0, etc.
allowed-tools: "Bash(python:*) WebFetch" # Optional: restrict tool access
metadata:                               # Optional: custom key-value pairs
  author: Your Name
  version: "1.0"
  mcp-server: server-name
  category: productivity
  tags: [automation, workflow]
  documentation: https://example.com/docs
  support: support@example.com
---
```

## Field Rules

### name (required)
- kebab-case only: `my-cool-skill`
- No spaces: ~~`My Cool Skill`~~
- No underscores: ~~`my_cool_skill`~~
- No capitals: ~~`MyCoolSkill`~~
- Must match folder name
- Forbidden prefixes: `claude-`, `anthropic-` (reserved)

### description (required)
- MUST include BOTH: what the skill does + when to use it (triggers)
- Under 1024 characters
- No XML angle brackets (< or >)
- Formula: `[Capability]. Use when user [phrases] or asks to [actions].`

**Good examples:**
```yaml
# Specific + actionable + has triggers
description: Analyzes Figma design files and generates developer handoff docs.
  Use when user uploads .fig files, asks for "design specs", "component docs",
  or "design-to-code handoff".

# MCP workflow + clear triggers
description: Manages Linear sprint planning including task creation and status
  tracking. Use when user mentions "sprint", "Linear tasks", "project planning",
  or asks to "create tickets".

# Domain-specific + outcome-focused
description: End-to-end customer onboarding for PayFlow. Handles account
  creation, payment setup, and subscription. Use when user says "onboard new
  customer", "set up subscription", or "create PayFlow account".
```

**Bad examples:**
```yaml
# Too vague — no triggers
description: Helps with projects.

# Missing triggers — Claude won't know when to load it
description: Creates sophisticated multi-page documentation systems.

# Too technical — no user-facing phrases
description: Implements the Project entity model with hierarchical relationships.
```

### license (optional)
Common values: `MIT`, `Apache-2.0`, `GPL-3.0`

### allowed-tools (optional)
Restrict which tools the skill can use. Space-separated.
Examples:
```yaml
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"
allowed-tools: "Read Write Edit"
```

### metadata (optional)
Any custom key-value pairs. Suggested fields:
- `author`: Skill author name
- `version`: Semantic version string (quote it: `"1.0"`)
- `mcp-server`: MCP server this skill depends on
- `category`: Descriptive category for organization

## Security Rules

**Forbidden in frontmatter:**
- XML angle brackets (`<` or `>`) — security restriction
- Names starting with `claude` or `anthropic` — reserved by Anthropic
- Code execution expressions — YAML is parsed safely

**Why:** Frontmatter appears verbatim in Claude's system prompt.
Malicious content could inject unauthorized instructions.

## Triggering Behavior

The description field is the sole signal Claude uses to decide whether
to load your skill for a given conversation. Tuning tips:

| Problem | Symptom | Fix |
|---|---|---|
| Under-triggering | Skill never auto-loads | Add more trigger phrases, technical terms |
| Over-triggering | Loads for unrelated queries | Add "Do NOT use for X" or narrow scope |
| Wrong context | Loads but doesn't help | Clarify scope in description |

**Debug technique:** Ask Claude "When would you use the [skill name] skill?"
It will quote the description back, revealing gaps.
