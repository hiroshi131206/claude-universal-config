# Workflow Patterns

Five patterns that cover most skill use cases. Choose the one that fits,
then adapt the structure for your specific workflow.

## Choosing an Approach

**Problem-first:** User describes an outcome → skill orchestrates the tools.
Example: "Set up a project workspace" → skill calls Notion MCP in sequence.

**Tool-first:** User has tool access → skill teaches the optimal workflow.
Example: "I have Linear MCP" → skill embeds sprint planning best practices.

---

## Pattern 1: Sequential Workflow Orchestration

**Use when:** Multi-step process that must happen in a specific order.

```markdown
## Workflow: [Task Name]

### Step 1: [Action]
Call: `mcp_tool_name` with params: field1, field2
Verify: [what success looks like]

### Step 2: [Action — depends on Step 1]
Use result from Step 1: customer_id
Call: `next_tool` with params: ...
Verify: ...

### Step 3: [Finalize]
...

### On failure at any step:
1. Log the error with context
2. [Rollback instructions if applicable]
3. Ask user how to proceed
```

**Key techniques:**
- Explicit step ordering with numbered list
- State what output each step produces (for next step)
- Validation gate before advancing
- Rollback instructions for failures

---

## Pattern 2: Multi-MCP Coordination

**Use when:** Workflow spans multiple services.

```markdown
## Workflow: [Handoff Name]

### Phase 1: [Source Service] (Figma MCP)
1. Export X from source
2. Generate specification
3. Save to: [location]

### Phase 2: [Storage Service] (Drive MCP)
1. Create folder structure
2. Upload Phase 1 outputs
3. Generate shareable links

### Phase 3: [Task Service] (Linear MCP)
1. Create tasks from Phase 1 spec
2. Attach Phase 2 links
3. Assign to team

### Phase 4: [Notification] (Slack MCP)
1. Post summary to channel
2. Include links from all phases
```

**Key techniques:**
- Clear phase separation with service label
- Explicit data handoff between phases (what passes forward)
- Validate before moving to next phase
- Centralized error handling section

---

## Pattern 3: Iterative Refinement

**Use when:** Output quality improves through repeated review-and-fix cycles.

```markdown
## Workflow: [Output Type] Generation

### Step 1: Initial Draft
1. Fetch/gather input data
2. Generate first draft
3. Save draft to temporary location

### Step 2: Quality Check
Run: `scripts/validate.py --input draft.md`
Check for:
- Missing required sections
- Formatting inconsistencies
- Data validation errors

### Step 3: Refinement Loop
For each issue found:
1. Address the specific issue
2. Regenerate affected section only
3. Re-validate

Repeat until: all checks pass OR 3 iterations reached

### Step 4: Finalize
1. Apply final formatting
2. Generate summary of changes
3. Save to output location
```

**Key techniques:**
- Explicit quality criteria (not vague "make it better")
- Validation scripts in `scripts/` for deterministic checks
- Loop exit condition (max iterations or quality threshold)
- Incremental changes, not full regeneration

---

## Pattern 4: Context-Aware Tool Selection

**Use when:** Same outcome, but the right tool depends on the input.

```markdown
## Workflow: [Outcome]

### Step 1: Analyze Input
Check: file type, size, context
Determine:
- Condition A → use Tool X
- Condition B → use Tool Y
- Condition C → use Tool Z
- Default → use Tool X

### Step 2: Execute
Based on decision from Step 1:

**If Tool X:**
Call: `tool_x` with params: ...

**If Tool Y:**
Call: `tool_y` with params: ...

### Step 3: Confirm with User
Explain: which tool was chosen and why
```

**Key techniques:**
- Explicit decision criteria (not "choose the best one")
- Fallback/default option always defined
- Transparency — tell user what was chosen and why
- Test each branch separately

---

## Pattern 5: Domain-Specific Intelligence

**Use when:** The skill adds specialized knowledge Claude doesn't have natively —
compliance rules, internal standards, proprietary logic.

```markdown
## Workflow: [Domain Task]

### CRITICAL: Pre-flight Checks
Before any action, verify:
- [ ] Condition 1 (required by [rule/policy])
- [ ] Condition 2
- [ ] Condition 3

If any check fails: STOP. Document reason. Ask user.

### Step 1: [Main Action]
[Only proceed if all pre-flight checks passed]
...

### Step 2: Audit Trail
Record:
- What was done
- Which checks passed
- Who authorized (if applicable)
- Timestamp

### On Exception:
1. Do NOT proceed
2. Flag with reason: [specific format]
3. Escalate to: [person/queue]
```

**Key techniques:**
- Domain rules embedded directly, not referenced externally
- Pre-flight checks BEFORE any tool calls
- Audit trail built into every action
- Explicit exception handling with escalation path

---

## Combining Patterns

Patterns compose well:
- Sequential + Iterative: Run ordered steps, then refine the output
- Multi-MCP + Domain: Coordinate services while enforcing compliance rules
- Context-Aware + Sequential: Choose path first, then execute that path's sequence
