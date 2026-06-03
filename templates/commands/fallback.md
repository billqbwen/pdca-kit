---
description: Execute rollback or fallback procedures when a deployment has failed or caused issues.
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

**Check for extension hooks (before fallback)**:
- Check if `.pdca/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_fallback` key
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

**Purpose**: Execute rollback or fallback procedures when a deployment has failed. Appends the rollback record to the existing deploy log.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read from FEATURE_DIR:
   - **REQUIRED**: deploy-log.md — understand what was deployed and what failed
   - **REQUIRED**: plan.md — deployment configuration and infrastructure
   - **IF EXISTS**: Load `/memory/constitution.md` for governance constraints

3. **Assess the situation**:
   - Review deploy-log.md to identify the failure point and scope
   - Determine the appropriate fallback strategy:
     - **Rollback**: Revert to previous version/state
     - **Degrade**: Disable the failing feature while keeping the system running
     - **Hotfix**: Apply an immediate fix if the issue is minor
   - If user input `$ARGUMENTS` specifies a strategy, use it

4. **Execute fallback**:
   a. **Pre-fallback checks**:
      - Confirm rollback target version/state
      - Verify rollback path is available
      - Notify relevant stakeholders (if applicable)

   b. **Execute rollback/fallback actions**:
      - Revert deployment artifacts
      - Restore previous configuration
      - Restore previous database state (if applicable)
      - Disable feature flags for the failing feature

   c. **Post-fallback verification**:
      - Verify system health after rollback
      - Run critical path smoke tests
      - Confirm monitoring returns to normal

5. **Append fallback record to deploy log**: Append the following section to `FEATURE_DIR/deploy-log.md`:

   ```markdown
   ## Rollback Record

   **Date**: [DATE]
   **Trigger**: [What caused the rollback — reference specific deployment failure]
   **Strategy**: Rollback / Degrade / Hotfix

   ### Rollback Steps

   | Step | Action | Status | Duration | Details |
   |------|--------|--------|----------|---------|
   | R1 | [Action] | ✅/❌ | [time] | [details] |
   | R2 | [Action] | ✅/❌ | [time] | [details] |

   ### Verification

   | Check | Status | Details |
   |-------|--------|---------|
   | System health | ✅/❌ | [details] |
   | Critical paths | ✅/❌ | [details] |
   | Monitoring | ✅/❌ | [details] |

   ### Root Cause Analysis

   **What failed**: [Description of the deployment failure]

   **Why it failed**: [Root cause analysis]

   **Prevention**: [What will prevent this from happening again]

   ### Impact Assessment

   | Dimension | Details |
   |-----------|---------|
   | Users affected | [scope] |
   | Duration of impact | [time] |
   | Data loss | [yes/no, details] |
   | Services degraded | [list] |

   ### Lessons Learned

   - [Lesson 1]
   - [Lesson 2]
   ```

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.pdca/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_fallback`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_fallback` key.
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
- Path to updated `FEATURE_DIR/deploy-log.md`
- Fallback strategy used
- Rollback status (success/failure)
- Root cause summary
- Impact assessment
- Suggested next steps (fix the issue and re-deploy)

## Done When

- [ ] Fallback strategy determined and executed
- [ ] System verified healthy after fallback
- [ ] Fallback record appended to FEATURE_DIR/deploy-log.md
- [ ] Root cause analysis documented
- [ ] Lessons learned captured
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with fallback summary
