# Skill Quality Checklist

Run this checklist before delivering a skill. A skill that fails any item
in "During development" or "Before upload" should be fixed before output.

---

## Before You Start

- [ ] Identified 2–3 concrete use cases with triggers and expected results
- [ ] Tools identified (Claude built-in, MCP, or scripts)
- [ ] Chosen a pattern from `patterns.md`
- [ ] Planned folder structure

---

## During Development

### Structure
- [ ] Folder named in kebab-case (e.g. `my-skill`, not `My Skill`)
- [ ] File named exactly `SKILL.md` (case-sensitive — not SKILL.MD or skill.md)
- [ ] No `README.md` inside the skill folder
- [ ] References in `references/` subdirectory (not inline in SKILL.md)

### Frontmatter
- [ ] YAML frontmatter has `---` opening and closing delimiters
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `name` does NOT start with `claude` or `anthropic`
- [ ] `description` includes WHAT the skill does
- [ ] `description` includes WHEN to use it (trigger phrases)
- [ ] `description` is under 1024 characters
- [ ] No XML angle brackets (`<` or `>`) anywhere in frontmatter

### Instructions (SKILL.md body)
- [ ] Instructions are specific and actionable (no vague verbs)
- [ ] Critical instructions are near the top or under `## IMPORTANT`
- [ ] Error handling is included for common failure modes
- [ ] At least 1–2 concrete examples with input and expected output
- [ ] Reference files explicitly linked: `consult references/xxx.md`
- [ ] SKILL.md is under 5,000 words (move overflow to references/)

### Reference Files (if used)
- [ ] Each reference file is clearly named and focused on one topic
- [ ] No content duplicated between SKILL.md and references/
- [ ] References are linked from SKILL.md body

---

## Before Delivery (triggering tests)

Run mentally or by testing with Claude:

**Should trigger (3 positive cases):**
- [ ] Obvious phrasing: "Help me [core task]"
- [ ] Paraphrased: "[Synonym] for [goal]"
- [ ] Domain-specific: "[Technical term from the domain]"

**Should NOT trigger (3 negative cases):**
- [ ] Unrelated topic: irrelevant domain
- [ ] Adjacent but different task
- [ ] Task handled by a different skill

---

## Success Criteria Targets

| Metric | Target |
|---|---|
| Triggers on relevant queries | 9 / 10 tests |
| Completes without user correction | 3 / 5 runs |
| Consistent structure across sessions | Yes |
| User doesn't need to prompt next steps | Yes |

---

## After Delivery

- [ ] Test in real conversations with varied phrasing
- [ ] Monitor for under-triggering (never auto-loads)
- [ ] Monitor for over-triggering (loads for irrelevant tasks)
- [ ] Iterate: improve description based on triggering behavior
- [ ] Update `metadata.version` when making significant changes
