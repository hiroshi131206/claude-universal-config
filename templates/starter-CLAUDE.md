# CLAUDE.md — Project Starter Template

Copy this file to your project root as `CLAUDE.md` and customize it.
Delete sections that don't apply. Add project-specific rules below.

---

## Workflow

### Plan Before Building
- For tasks with 3+ steps or architectural decisions, enter plan mode before writing any code.
- If the work goes sideways, stop immediately and re-plan. Do not push through.
- Use plan mode for verification steps, not just implementation.
- Write detailed specs to eliminate ambiguity before handing off work.

### Use Subagents for Parallel Work
- Keep the main context window clean by offloading research, exploration, and parallel analysis to subagents.
- One subagent per focused task.
- Append "use subagents" to any request where more compute would help.

### Self-Improvement Loop
- After every correction from the user, run `/lessons` to record the pattern in `tasks/lessons.md`.
- At the start of each session, review `tasks/lessons.md` for this project.
- Iterate on lessons until the same mistake stops recurring.

### Validate Before Marking Done
- A task is not complete until behavior is demonstrated, not just implemented.
- Run tests, check logs, prove it works.
- Ask: "Would a staff engineer approve this?"

### Pursue Elegance (with balance)
- After significant changes, pause and ask: "Is there a more elegant approach?"
- If a fix feels like a workaround, say so and propose the clean solution.
- For simple, obvious fixes: skip this step to avoid over-engineering.

### Autonomous Bug Fixing
- When given a bug report, fix it without waiting for step-by-step instructions.
- Identify failing logs, errors, and tests — then resolve them.
- If CI tests fail, fix them without being asked.

---

## Proactive Skill and Agent Selection

Before starting any task, evaluate whether an available skill or agent applies.
Do not wait for the user to specify — select and use the right tool automatically.

### Skill Routing

| Task type | Skill to use |
|---|---|
| SwiftUI / iOS code review or writing | `swiftui-pro` |
| Web component, page, or UI code | `frontend-design` |
| Image generation, sprites, transparent assets | `nano-banana` |
| Find code by intent ("where is auth handled?") | `grepai` |
| Autonomous iterative loop (modify → verify → repeat) | `autoresearch` |
| User explicitly says "use Codex" or "ask Codex" | `codex` |
| Creating or improving a Claude skill | `skill-creator` |

### Agent Routing

Invoke agents proactively using the Task tool when the task matches.
Do not wait for the user to name the agent.

| Task type | Agent to invoke |
|---|---|
| Security audit — one-shot vulnerability report | `black-hacker` → then `white-hacker` |
| Security audit — iterative loop until clean | `/autoresearch:security` |
| Design or plan a new feature's architecture | `code-architect` |
| Explore an unfamiliar codebase | `code-explorer` |
| Review a PR for test coverage and correctness | `pr-test-analyzer` |
| Review PR comments or discussion | `comment-analyzer` |
| Find and remove unnecessary complexity | `code-simplifier` |
| Review error handling for silent failures | `silent-failure-hunter` |
| Review type definitions and data model design | `type-design-analyzer` |

### Decision Flow

When a task arrives:
1. Check: does it match a skill trigger above? → load that skill
2. Check: does it match an agent trigger above? → invoke that agent via Task tool
3. If multiple apply: use the most specific match (e.g. `swiftui-pro` beats `code-simplifier` for Swift code)
4. If none apply: proceed with standard Claude Code behavior

Do not announce this routing to the user unless asked. Just do it.

---

## Task Management

1. **Plan first**: Write the plan as a checklist in `tasks/todo.md` before coding.
2. **Confirm the plan**: Verify approach before starting implementation.
3. **Track progress**: Check off completed items as you go.
4. **Summarize changes**: After each step, provide a high-level summary of what was done.
5. **Record outcomes**: Add a review section to `tasks/todo.md` when done.
6. **Extract lessons**: After any correction, update `tasks/lessons.md`.

---

## Core Principles

- **Simplicity**: Keep every change as small as possible. Minimize blast radius.
- **Root causes**: Find the actual cause. No band-aid fixes.
- **Minimal impact**: Only change what is necessary. Don't introduce new bugs while fixing old ones.

---

## Project-Specific Rules

<!-- Add your project rules below. Examples: -->
<!-- - Always run `npm run typecheck` before marking a task done -->
<!-- - API responses must always include a `requestId` field -->
<!-- - Do not modify the `legacy/` directory without explicit permission -->
