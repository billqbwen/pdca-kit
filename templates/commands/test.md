---
description: Generate and execute tests to validate the implementation against the specification and technical plan.
handoffs: 
  - label: Review Implementation
    agent: pdca.review
    prompt: Review the implementation against spec and plan
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

**Check for extension hooks (before testing)**:
- Check if `.pdca/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_test` key
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

**Purpose**: Validate the implementation by generating and executing tests against the spec and plan. This is a **mandatory** Check-phase command.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read from FEATURE_DIR:
   - **REQUIRED**: spec.md — feature requirements and user stories
   - **REQUIRED**: plan.md — tech stack, architecture, data model, contracts, research (all inline)
   - **REQUIRED**: tasks.md — task list with completion status
   - **IF EXISTS**: Load `/memory/constitution.md` for project principles

3. **Analyze test coverage needs**:
   - Extract acceptance scenarios from spec.md (User Stories → Acceptance Scenarios)
   - Extract success criteria from spec.md (Success Criteria → Measurable Outcomes)
   - Extract interface contracts from plan.md (`### API Contracts` section)
   - Extract entities from plan.md (`### Data Model` section)
   - Review completed tasks in tasks.md for areas that need testing
   - Identify the testing framework from plan.md (Technical Context → Testing)

4. **Generate test cases**: Based on the analysis above, generate tests in the following categories:

   a. **Contract Tests** (if contracts defined):
      - For each interface contract, verify inputs, outputs, and error modes
      - Map to testing framework appropriate for the project type

   b. **Integration Tests**:
      - For each user story, verify end-to-end flow
      - Include setup/teardown as needed

   c. **Unit Tests**:
      - For each entity and service, verify core logic
      - Include edge cases from spec.md

   d. **Acceptance Tests**:
      - Map each acceptance scenario (Given/When/Then) to executable tests
      - Verify success criteria are measurable and met

5. **Execute tests**:
   - Run the generated tests using the project's testing framework
   - Capture results: pass/fail per test, execution time, coverage data
   - For each failure, document the root cause

6. **Generate test report**: Create `FEATURE_DIR/test-report.md` with the following structure:

   ```markdown
   # Test Report: [FEATURE NAME]

   **Branch**: `[###-feature-name]` | **Date**: [DATE]
   **Input**: spec.md, plan.md, tasks.md from `FEATURE_DIR`

   ## Summary

   | Metric | Value |
   |--------|-------|
   | Total Tests | [N] |
   | Passed | [N] |
   | Failed | [N] |
   | Skipped | [N] |
   | Coverage % | [N%] |
   | Execution Time | [N seconds] |

   ## Test Results by Category

   ### Contract Tests

   | # | Test Name | Status | Duration | Notes |
   |---|-----------|--------|----------|-------|
   | T001 | [test name] | ✅/❌ | [time] | [notes] |

   ### Integration Tests

   | # | Test Name | Status | Duration | Notes |
   |---|-----------|--------|----------|-------|
   | T010 | [test name] | ✅/❌ | [time] | [notes] |

   ### Unit Tests

   | # | Test Name | Status | Duration | Notes |
   |---|-----------|--------|----------|-------|
   | T020 | [test name] | ✅/❌ | [time] | [notes] |

   ### Acceptance Tests

   | # | Spec Reference | Status | Notes |
   |---|----------------|--------|-------|
   | A001 | [Spec §X.Y / US-N] | ✅/❌ | [notes] |

   ## Spec Coverage Mapping

   | User Story | Acceptance Scenarios Tested | Status |
   |------------|---------------------------|--------|
   | US1 (P1) | N of M scenarios | ✅/❌ |
   | US2 (P2) | N of M scenarios | ✅/❌ |

   ## Success Criteria Validation

   | Criterion | Target | Actual | Status |
   |-----------|--------|--------|--------|
   | SC-001: [description] | [target] | [actual] | ✅/❌ |

   ## Failures & Issues

   [Detailed failure analysis for each failing test]

   ## Recommendations

   - [Action items for failing tests]
   - [Coverage gaps identified]
   - [Performance concerns]
   ```

7. **Gate check**: If any tests fail:
   - Document all failures in the report
   - **STOP** and report: "Test execution complete with [N] failures. See test-report.md for details. Fix failures before proceeding to review."
   - Do NOT proceed to Mandatory Post-Execution Hooks

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.pdca/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_test`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_test` key.
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
- Path to `FEATURE_DIR/test-report.md`
- Total test count, pass/fail/skip breakdown
- Coverage percentage
- Spec coverage mapping summary
- Any failures requiring attention
- Suggested next command: `__PDCA_COMMAND_REVIEW__`

## Done When

- [ ] Tests generated for all acceptance scenarios, contracts, entities, and services
- [ ] Tests executed and results captured in test-report.md
- [ ] All tests pass (gate enforced — do not proceed with failures)
- [ ] Spec coverage mapping complete
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with test summary
