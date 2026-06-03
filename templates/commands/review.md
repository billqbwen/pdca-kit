---
description: Perform code review against the specification and technical plan to ensure implementation quality and consistency.
handoffs: 
  - label: Deploy Feature
    agent: pdca.deploy
    prompt: Deploy the reviewed feature to the target environment
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before review)**:
- Check if `.pdca/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_review` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    
    Wait for the result of the hook command before proceeding to the Outline.
    ```
- If no hooks are registered or `.pdca/extensions.yml` does not exist, skip silently

## Outline

**Purpose**: Perform a thorough code review of the implementation against the specification and technical plan. This is a **mandatory** Check-phase command.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read from FEATURE_DIR:
   - **REQUIRED**: spec.md — feature requirements, user stories, success criteria
   - **REQUIRED**: plan.md — tech stack, architecture, data model, contracts (all inline)
   - **REQUIRED**: tasks.md — task list with completion status
   - **IF EXISTS**: test-report.md — test results from previous phase
   - **IF EXISTS**: Load `/memory/constitution.md` for project principles

3. **Review dimensions**: Conduct review across the following dimensions:

   a. **Specification Conformance**:
      - Compare implemented code against spec.md functional requirements (FR-XXX)
      - Verify each user story is fully implemented
      - Check that all acceptance scenarios are satisfied
      - Identify any missing or incomplete features

   b. **Plan Conformance**:
      - Compare implementation against plan.md architecture and structure
      - Verify tech stack choices are followed
      - Check data model implementation matches plan.md `### Data Model`
      - Verify contracts are implemented as defined in plan.md `### API Contracts`
      - Check project structure matches plan.md `## Project Structure`

   c. **Constitution Compliance**:
      - Verify implementation follows project principles from constitution.md
      - Check for any governance violations
      - Document any justified deviations

   d. **Code Quality**:
      - Review for common code issues (duplication, complexity, readability)
      - Check error handling patterns
      - Verify logging and observability
      - Review naming conventions and consistency
      - Check for security best practices

   e. **Test Coverage** (if test-report.md exists):
      - Review test coverage against spec requirements
      - Identify gaps in test coverage
      - Verify test quality and relevance

4. **Generate review report**: Create `FEATURE_DIR/review-report.md` with the following structure:

   ```markdown
   # Review Report: [FEATURE NAME]

   **Branch**: `[###-feature-name]` | **Date**: [DATE]
   **Reviewer**: AI Code Review | **Input**: spec.md, plan.md, tasks.md, test-report.md

   ## Overall Assessment

   | Dimension | Status | Score (1-5) |
   |-----------|--------|-------------|
   | Specification Conformance | ✅/❌ | [1-5] |
   | Plan Conformance | ✅/❌ | [1-5] |
   | Constitution Compliance | ✅/❌ | [1-5] |
   | Code Quality | ✅/❌ | [1-5] |
   | Test Coverage | ✅/❌ | [1-5] |

   **Overall Verdict**: ✅ APPROVED / ❌ CHANGES REQUESTED

   ## Specification Conformance

   ### User Story Coverage

   | User Story | Status | Notes |
   |------------|--------|-------|
   | US1 (P1): [title] | ✅ Complete / ⚠️ Partial / ❌ Missing | [notes] |
   | US2 (P2): [title] | ✅ Complete / ⚠️ Partial / ❌ Missing | [notes] |

   ### Requirement Checklist

   | Requirement | Implemented | Notes |
   |-------------|-------------|-------|
   | FR-001: [description] | ✅/❌ | [notes] |
   | FR-002: [description] | ✅/❌ | [notes] |

   ## Plan Conformance

   ### Architecture Check

   | Aspect | Plan | Actual | Status |
   |--------|------|--------|--------|
   | [Aspect] | [expected] | [actual] | ✅/❌ |

   ### Data Model Check

   | Entity | Plan | Actual | Status |
   |--------|------|--------|--------|
   | [Entity] | [expected fields] | [actual fields] | ✅/❌ |

   ## Code Quality

   ### Issues Found

   | Severity | File | Line | Issue | Recommendation |
   |----------|------|------|-------|----------------|
   | Critical | [file] | [line] | [issue] | [fix] |
   | Major | [file] | [line] | [issue] | [fix] |
   | Minor | [file] | [line] | [issue] | [fix] |

   ### Positive Findings

   - [Well-implemented aspects]

   ## Action Items

   ### Must Fix (Blocking)

   - [ ] [Critical issue requiring resolution before deploy]

   ### Should Fix (Non-blocking)

   - [ ] [Important but non-blocking improvements]

   ### Nice to Have

   - [ ] [Optional enhancements]

   ## Reviewer Notes

   [Additional context, observations, and recommendations]
   ```

5. **Gate check**: If any "Must Fix (Blocking)" items exist:
   - **STOP** and report: "Review found [N] blocking issues. See review-report.md for details. Resolve blocking issues before proceeding."
   - Do NOT proceed to Mandatory Post-Execution Hooks

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.pdca/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_review`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_review` key.
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue to the Completion Report.
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Mandatory hook** (`optional: false`) — **You MUST emit `EXECUTE_COMMAND:` for each mandatory hook**:
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```

## Completion Report

Report completion to the user with:
- Path to `FEATURE_DIR/review-report.md`
- Overall verdict (APPROVED or CHANGES REQUESTED)
- Summary of issues by severity
- Spec conformance score and coverage
- Suggested next command: `__PDCA_COMMAND_DEPLOY__`

## Done When

- [ ] All review dimensions evaluated (spec conformance, plan conformance, constitution, code quality, test coverage)
- [ ] Review report generated at FEATURE_DIR/review-report.md
- [ ] No blocking issues remain (gate enforced)
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with review summary
