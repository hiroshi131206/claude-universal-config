# Lessons Command

Record what was learned from a correction or mistake into `tasks/lessons.md`.
Run this after every correction to build a self-improving ruleset.

## When to Run

- After the user corrects Claude's approach
- After a bug fix that revealed a pattern or assumption error
- After a PR review that exposed a recurring issue
- At the start of a session: review existing lessons for the current project

---

## Steps

### 1. Identify the Pattern Behind the Mistake

Do not just record what went wrong. Record the *pattern* that caused it:
- Wrong assumption about the codebase
- Misunderstood requirement
- Skipped a validation step
- Used the wrong tool or approach for the context

### 2. Write the Rule

Format each lesson as an actionable rule — not a description of the past error:

```
## [Category] — [Short title]

Rule: [What to do differently next time, specific and actionable]
Why: [What went wrong and why this matters]
Applies to: [When this rule kicks in — specific triggers or conditions]
```

### 3. Update tasks/lessons.md

Append to `tasks/lessons.md` (create it if it doesn't exist). Group by category:
- `Workflow` — process mistakes (skipped steps, wrong order)
- `Code` — code quality mistakes (wrong pattern, missing validation)
- `Communication` — misunderstood intent, wrong scope
- `Tools` — wrong tool choice, incorrect parameters

### 4. Prune Obsolete Lessons

If an existing rule no longer applies (code was refactored, policy changed), remove or update it. A stale ruleset is worse than none.

---

## Example

User correction: "You added a new API endpoint without checking if one already exists."

Resulting lesson:
```
## Workflow — Check before creating

Rule: Before creating any new function, endpoint, or component, search the codebase
      for existing implementations that already do the same thing.
Why: Added a duplicate endpoint; the existing one was not obvious from context.
Applies to: Any time a "create new X" request is received.
```

---

## Session Start Behavior

At the start of each session, if `tasks/lessons.md` exists for this project:
- Read it
- Internalize the rules before starting any task
- Do not ask the user to repeat context that is already captured there
