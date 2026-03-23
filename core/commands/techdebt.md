# Tech Debt Command

Scan the codebase for tech debt at the end of a session and eliminate it.

## Steps

### 1. Scan for Duplicated Code
Search for:
- Functions or logic that appear more than once
- Copy-pasted blocks (same variable names, similar structure)
- Multiple implementations of the same utility (e.g., date formatting, error handling)

### 2. Scan for Dead Code
Search for:
- Unused imports, variables, functions, and components
- Commented-out code blocks
- Feature flags that are always `true` or always `false`
- Unreachable branches

### 3. Scan for Shortcuts and Workarounds
Look for:
- `// TODO`, `// FIXME`, `// HACK`, `// XXX` comments
- `any` types in TypeScript without justification
- Hardcoded values that should be constants or config
- `try/catch` blocks that silently swallow errors

### 4. Prioritize and Fix
For each item found:
- **High**: Duplicated logic that causes bugs when one copy is updated → refactor now
- **Medium**: Dead code, unused imports → delete now
- **Low**: TODOs without urgency → log in `tasks/todo.md`, skip for now

Fix high and medium items immediately. Do not leave the session with duplicated logic.

### 5. Output a Summary

```
## Tech Debt Report

### Fixed
- [What was fixed and why]

### Remaining (logged to tasks/todo.md)
- [What was deferred and its priority]

### Refactoring Opportunities (future)
- [Optional: larger structural improvements noticed]
```

## When to Run

- At the end of any session that added new features or fixed multiple bugs
- Before opening a PR
- After a rapid-prototyping phase before hardening

## Notes

- Do not refactor code that wasn't touched in this session unless the duplication is critical
- If a refactor would take more than 30 minutes, log it and defer
