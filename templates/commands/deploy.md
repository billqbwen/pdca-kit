---
description: Deploy the reviewed and tested feature to the target environment.
handoffs: 
  - label: Rollback Deployment
    agent: pdca.fallback
    prompt: Execute fallback for the failed deployment
  - label: Release Feature
    agent: pdca.release
    prompt: Release the deployed feature
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

**Check for extension hooks (before deploy)**:
- Check if `.pdca/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_deploy` key
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

**Purpose**: Deploy the feature to the target environment. Creates a deployment log documenting all steps and outcomes.

1. **Setup**: Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read from FEATURE_DIR:
   - **REQUIRED**: plan.md — deployment target, infrastructure, configuration (from Technical Context and Quickstart)
   - **REQUIRED**: tasks.md — implementation status
   - **IF EXISTS**: test-report.md — verify all tests passed
   - **IF EXISTS**: review-report.md — verify no blocking issues
   - **IF EXISTS**: Load `/memory/constitution.md` for governance constraints

3. **Pre-deployment checks**:
   - Verify test-report.md exists and all tests pass
   - Verify review-report.md exists and no blocking issues remain
   - Confirm target environment from plan.md Technical Context (Target Platform)
   - Check deployment dependencies and prerequisites
   - If any prerequisite fails, abort and report missing prerequisites

4. **Execute deployment**: Perform deployment steps appropriate for the project type:

   a. **Build & Package**:
      - Build the project according to plan.md tech stack
      - Verify build artifacts

   b. **Configuration**:
      - Apply environment-specific configuration
      - Set up environment variables, secrets, feature flags

   c. **Deploy**:
      - Deploy to target environment
      - Verify deployment health (health checks, smoke tests)

   d. **Post-deployment verification**:
      - Run quickstart validation scenarios from plan.md `### Quickstart`
      - Verify critical paths are functional
      - Check monitoring/alerting is active

5. **Generate deploy log**: Create or update `FEATURE_DIR/deploy-log.md` with the following structure:

   ```markdown
   # Deploy Log: [FEATURE NAME]

   **Branch**: `[###-feature-name]` | **Date**: [DATE]
   **Environment**: [target environment]
   **Version**: [version/tag/commit hash]

   ## Pre-Deployment Checks

   | Check | Status | Notes |
   |-------|--------|-------|
   | All tests passing | ✅/❌ | [from test-report.md] |
   | No blocking review issues | ✅/❌ | [from review-report.md] |
   | Target environment ready | ✅/❌ | [notes] |
   | Dependencies verified | ✅/❌ | [notes] |

   ## Deployment Steps

   ### Step 1: Build & Package

   | Action | Status | Duration | Details |
   |--------|--------|----------|---------|
   | [Build step] | ✅/❌ | [time] | [details] |

   ### Step 2: Configuration

   | Config Item | Value | Status |
   |-------------|-------|--------|
   | [Config key] | [value] | ✅ Applied |

   ### Step 3: Deploy

   | Action | Status | Duration | Details |
   |--------|--------|----------|---------|
   | [Deploy step] | ✅/❌ | [time] | [details] |

   ### Step 4: Post-Deployment Verification

   | Check | Status | Details |
   |-------|--------|---------|
   | Health check | ✅/❌ | [details] |
   | Quickstart scenario 1 | ✅/❌ | [details] |
   | Quickstart scenario 2 | ✅/❌ | [details] |
   | Monitoring active | ✅/❌ | [details] |

   ## Deployment Summary

   | Metric | Value |
   |--------|-------|
   | Total Steps | [N] |
   | Successful | [N] |
   | Failed | [N] |
   | Total Duration | [time] |

   ## Issues & Notes

   [Any issues encountered, workarounds, or observations]

   ## Rollback Instructions (if needed)

   [Steps to rollback this deployment — see `__PDCA_COMMAND_FALLBACK__`]
   ```

6. **Gate check**: If deployment fails at any step:
   - Document the failure in deploy-log.md
   - Report: "Deployment failed at [step]. See deploy-log.md for details."
   - Suggest running `__PDCA_COMMAND_FALLBACK__` to rollback

## Mandatory Post-Execution Hooks

**You MUST complete this section before reporting completion to the user.**

Check if `.pdca/extensions.yml` exists in the project root.
- If it does not exist, or no hooks are registered under `hooks.after_deploy`, skip to the Completion Report.
- If it exists, read it and look for entries under the `hooks.after_deploy` key.
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
- Path to `FEATURE_DIR/deploy-log.md`
- Deployment status (success/failure)
- Environment deployed to
- Version deployed
- Duration
- Suggested next command: `__PDCA_COMMAND_RELEASE__` (if successful) or `__PDCA_COMMAND_FALLBACK__` (if failed)

## Done When

- [ ] Pre-deployment checks completed and verified
- [ ] All deployment steps executed and logged
- [ ] Post-deployment verification passed
- [ ] Deploy log written to FEATURE_DIR/deploy-log.md
- [ ] Extension hooks dispatched or skipped according to the rules in Mandatory Post-Execution Hooks above
- [ ] Completion reported to user with deployment summary
