# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `__PDCA_COMMAND_PLAN__` command. All design artifacts (research, data model, contracts, quickstart) are included as sections within this single file.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── spec.md              # Feature specification (__PDCA_COMMAND_SPECIFY__ command output)
├── plan.md              # This file — implementation plan with all design artifacts inline
├── tasks.md             # Task list (__PDCA_COMMAND_TASKS__ command output)
├── checklist.md         # Quality checklists (__PDCA_COMMAND_CHECKLIST__ command output)
├── test-report.md       # Test execution report (__PDCA_COMMAND_TEST__ command output)
├── review-report.md     # Code review report (__PDCA_COMMAND_REVIEW__ command output)
├── deploy-log.md        # Deployment log (__PDCA_COMMAND_DEPLOY__ / __PDCA_COMMAND_FALLBACK__ command output)
└── release-note.md      # Release notes (__PDCA_COMMAND_RELEASE__ command output)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Phase 0: Research

> This section replaces the former `research.md` file. All research decisions are documented inline.

[For each NEEDS CLARIFICATION in Technical Context, document the research outcome:]

### Decision: [Topic]

- **Decision**: [what was chosen]
- **Rationale**: [why chosen]
- **Alternatives considered**: [what else evaluated]

[Repeat for each research decision]

## Phase 1: Design

> This section replaces the former `data-model.md`, `contracts/`, and `quickstart.md` files.

### Data Model

[Extract entities from feature spec:]

#### Entity: [Entity Name]

- **Fields**: [field name]: [type] — [description]
- **Relationships**: [to other entities]
- **Validation Rules**: [from requirements]
- **State Transitions**: [if applicable]

[Repeat for each entity]

### API Contracts

[Define interface contracts if the project has external interfaces. Skip if purely internal.]

#### Contract: [Interface Name]

- **Type**: [e.g., REST endpoint, CLI command, public function, UI component]
- **Signature/Route**: [the contract definition]
- **Input**: [parameters and their types]
- **Output**: [return value and error modes]
- **Behavior**: [expected behavior, side effects]

[Repeat for each contract]

### Quickstart

> Runnable validation scenarios that prove the feature works end-to-end. Includes prerequisites, setup commands, test/run commands, and expected outcomes. References data model and contracts instead of duplicating details. Implementation details belong in `tasks.md`.

#### Scenario: [Scenario Name]

- **Prerequisites**: [what must be set up first]
- **Steps**:
  1. [Command or action]
  2. [Expected outcome]
- **Validation**: [how to confirm it works]

[Repeat for each validation scenario]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
