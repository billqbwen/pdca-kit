---
description: Finalize the release by generating release notes and confirming deployment readiness for production.
handoffs: 
  - label: Create New Spec
    agent: pdca.define
    prompt: Start a new feature specification
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

**Check for extension hooks (before release)**:
- Check if `.pdca/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_release` key
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

**Purpose**: Finalize the release by generating comprehensive release notes. This is the final step in the Act phase — the feature is now complete and delivered.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read from FEATURE_DIR:
   - **REQUIRED**: spec.md — feature requirements, user stories
   - **REQUIRED**: plan.md — technical approach, architecture
   - **REQUIRED**: tasks.md — completed implementation tasks
   - **REQUIRED**: deploy-log.md — deployment status
   - **IF EXISTS**: test-report.md — test results
   - **IF EXISTS**: review-report.md — review findings
   - **IF EXISTS**: Load `/memory/constitution.md` for governance constraints

3. **Verify release readiness**:
   - Confirm deploy-log.md shows successful deployment
   - Confirm test-report.md shows all tests passing (if exists)
   - Confirm review-report.md shows no blocking issues (if exists)
   - Verify all tasks in tasks.md are marked `[X]`
   - If any check fails, abort and report what needs to be resolved

4. **Determine version**: 
   - Extract version from plan.md or deploy-log.md
   - If version not specified, use semantic versioning based on changes:
     - **Major**: Breaking changes to existing functionality
     - **Minor**: New features, non-breaking
     - **Patch**: Bug fixes, minor improvements

5. **Generate release notes**: Create `FEATURE_DIR/release-note.md` with the following structure:

   ```markdown
   # Release Notes: [FEATURE NAME]

   **Version**: [version number]
   **Release Date**: [DATE]
   **Branch**: `[###-feature-name]`

   ## Overview

   [One-paragraph summary of what this release delivers, extracted from spec.md Summary and plan.md Summary]

   ## What's New

   ### New Features

   | Feature | Description | User Story |
   |---------|-------------|------------|
   | [Feature name] | [Brief description] | US1 (P1) |

   ### Improvements

   | Improvement | Description |
   |-------------|-------------|
   | [Improvement] | [Description] |

   ### Bug Fixes

   | Bug | Description | Reference |
   |-----|-------------|-----------|
   | [Bug] | [Description] | [Issue/PR reference] |

   ## Changes

   ### Functional Changes

   | Requirement | Change | Impact |
   |-------------|--------|--------|
   | FR-001 | [What changed] | [User impact] |

   ### Technical Changes

   | Component | Change | Rationale |
   |-----------|--------|-----------|
   | [Component] | [Change] | [Why] |

   ## Known Issues

   | Issue | Severity | Workaround |
   |-------|----------|------------|
   | [Issue] | Low/Medium/High | [Workaround if any] |

   ## Upgrade Notes

   ### Prerequisites

   - [Required dependencies or versions]
   - [Configuration changes needed]

   ### Migration Steps

   1. [Step 1]
   2. [Step 2]

   ### Breaking Changes

   | Change | Migration Path |
   |--------|---------------|
   | [Breaking change] | [How to migrate] |

   ## Release Checklist

   - [x] All tasks completed (tasks.md)
   - [x] All tests passing (test-report.md)
   - [x] Code review approved (review-report.md)
   - [x] Deployed to [environment] (deploy-log.md)
   - [x] Post-deployment verification passed
   - [x] Monitoring and alerts configured
   - [x] Documentation updated
   - [x] Release notes finalized

   ## Performance Metrics

   | Metric | Target | Actual | Status |
   |--------|--------|--------|--------|
   | [Metric from SC-XXX] | [target] | [actual] | ✅/❌ |

   ## Contributors

   [List of contributors if available]

   ## References

   - Spec: [link to spec.md]
   - Plan: [link to plan.md]
   - Tasks: [link to tasks.md]
   - Deploy Log: [link to deploy-log.md]
   ```

6. **Final validation**:
   - Verify all Release Checklist items are checked
   - Confirm version number is correct
   - Ensure no placeholder text remains

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.pdca/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_release`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_release` key.
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
- Path to `FEATURE_DIR/release-note.md`
- Version released
- Summary of what's included (features, fixes, improvements)
- Known issues (if any)
- Upgrade notes for users
- The PDCA cycle for this feature is now **complete**

## Done When

- [ ] Release readiness verified (deploy success, tests pass, review clean)
- [ ] Version determined and documented
- [ ] Release notes generated at FEATURE_DIR/release-note.md
- [ ] Release checklist fully validated
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user — feature is released and PDCA cycle complete
