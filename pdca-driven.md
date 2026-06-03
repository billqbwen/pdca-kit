# PDCA-Driven Development

## Why PDCA?

Software development is never linear. Requirements change, understanding deepens, problems surface during implementation. Traditional waterfall tries to plan everything before coding. Agile embraces change but often lacks structured quality assurance.

**PDCA (Plan-Do-Check-Act)** is a classic continuous improvement cycle from the world of quality management. PDCA Kit applies this cycle to AI-assisted software development — not as a new concept, but as a return to the essence of development: **Plan, Execute, Check, Improve**.

## Mapping PDCA to Software Development

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    ▼                                              │
  PLAN                  DO                  CHECK
  ──────              ──────               ────────
  Define what to       Execute to plan     Verify quality
  build and how
                      · Task-by-task       · Cross-document
  · Constitution      · TDD approach         consistency
  · Specification     · Incremental        · Code review
  · Clarification       builds             · Testing
  · Technical plan                          · Quality checklists
  · Task breakdown                              │
    │                                           │
    │                                           ▼
    │                                         ACT
    │                                       ────────
    │                                       Deploy & Learn
    │                                       
    │                                       · Deploy to target
    │                                       · Release management
    │                                       · Gather feedback
    │                                           │
    └─────────────────── feedback drives next ───┘
```

### PLAN: Turn Ideas Into Executable Plans

This is the foundation of the entire cycle. Vague ideas must be transformed into clear, verifiable specifications.

**Core principle: First clarify "what" and "why," then decide "how."**

Many developers start coding as soon as they have an idea. PDCA requires completing these steps in the Plan phase first:

1. **Constitution** — Define governing principles for the project. What makes good code? What are the testing standards? What architectural constraints exist? These principles are enforced and checked throughout all subsequent phases.

2. **Specification (Define)** — Describe functional requirements in natural language. Focus on **what users need** and **why they need it**. No tech stack, no implementation details. When something is unclear, mark it with `[NEEDS CLARIFICATION]` — don't guess.

3. **Clarification (Clarify)** — Before entering technical planning, eliminate ambiguities through structured Q&A. This is the quality gate of the Plan phase — entering development with an unclear spec is like crossing a desert without a map.

4. **Technical Plan** — Translate business requirements into a technical blueprint. Choose the tech stack, design data models, define API contracts. Every technical decision should trace back to a specific requirement.

5. **Task Breakdown (Tasks)** — Decompose the technical plan into an executable task list. Define dependencies, mark parallelizable tasks, and ensure every task has a clear deliverable.

Plan phase output: **A clarified feature specification, a justified technical plan, and an executable task list.**

### DO: Execute to Plan

The Do phase is not free-form exploration — it's disciplined execution of the task list produced in Plan.

**Core principle: One task at a time, every step verifiable.**

1. **Task-driven** — AI executes tasks one by one as defined in `tasks.md`. No skipping, no adding "nice-to-have" features on its own.

2. **TDD (Test-Driven Development)** — Write tests first, confirm they fail, then write implementation. This isn't dogma — it's ensuring every piece of code has corresponding verification logic.

3. **Incremental builds** — Each completed task is a verifiable increment. Don't wait until everything is done to check — verify as you go.

Do phase output: **Spec-compliant, tested, runnable code.**

### CHECK: Quality Is Built In, Not Bolted On

Check doesn't wait until everything is written — it runs throughout. The PDCA Check phase has multi-dimensional quality assurance:

**Core principle: Quality cannot be "added on" — it must be "built in."**

1. **Cross-document consistency (Analyze)** — Are the spec, plan, and tasks consistent? Are there requirements in the spec not covered by the plan? Are there technical decisions in the plan not reflected in the tasks?

2. **Code review (Review)** — Review implementation code against the spec and plan. Not a vague "looks good," but a line-by-line confirmation: Does this feature implement requirement #3 in the spec? Does this technical choice align with the architecture principles in the plan?

3. **Test verification (Test)** — Run tests to confirm correctness. Not just unit tests, but integration and end-to-end tests as well.

4. **Quality checklist (Checklist)** — Generate a project-specific quality checklist, validating requirements completeness and clarity like "unit tests for English."

Check phase output: **A quality report clearly stating what passes and what needs fixing.**

### ACT: Deploy, Release, and Return to PLAN

The Act phase pushes verified code to production and feeds experience back into the next cycle.

**Core principle: Every deployment is the starting point for the next improvement.**

1. **Deployment (Deploy)** — Deploy the feature to the target environment. Rollback mechanism available if deployment fails.

2. **Release (Release)** — Manage versioning, generate changelog, confirm release readiness.

3. **Feedback loop** — Production performance, user feedback, and discovered issues all become input for the next Plan phase. This isn't a linear process — it's a continuously spinning flywheel.

Act phase output: **A deployed feature + input for the next round of improvement.**

## Why PDCA Fits AI-Assisted Development

AI coding tools dramatically accelerate the "idea to code" pipeline, but speed amplifies problems:

- **No Plan**: Let AI code directly, and it will guess your intent. A wrong guess takes you further and further off course.
- **No Check**: AI-generated code may look correct but could miss edge cases, violate architectural principles, or lack tests entirely.
- **No Act**: Code written but never deployed to verify — you'll never know if it actually works in a real environment.

The PDCA cycle, through structured phase gates, gives AI clear inputs, outputs, and verification criteria at every stage. AI is not asked to "write a chat app" — it's guided through a traceable process:

```
You say → Spec → Clarify → Plan → Tasks → Implement → Analyze → Review → Test → Deploy → Feedback → You say (next round)
```

Every step produces concrete artifacts. Every step can be traced back.

## The 14 Commands in PDCA Kit

PDCA Kit provides 14 AI commands covering the full cycle:

| Phase | Command | What it does |
|-------|---------|-------------|
| **Plan** | `/pdca.constitution` | Establish project governance principles |
| **Plan** | `/pdca.define` | Turn ideas into structured specifications |
| **Plan** | `/pdca.clarify` | Eliminate ambiguity in specs |
| **Plan** | `/pdca.plan` | Create a technical implementation plan |
| **Plan** | `/pdca.tasks` | Break down into executable tasks |
| **Plan** | `/pdca.taskstoissues` | Convert tasks to GitHub Issues |
| **Do** | `/pdca.implement` | Execute tasks one by one |
| **Check** | `/pdca.analyze` | Cross-document consistency analysis |
| **Check** | `/pdca.checklist` | Generate quality validation checklists |
| **Check** | `/pdca.review` | Review code against spec and plan |
| **Check** | `/pdca.test` | Generate and execute tests |
| **Act** | `/pdca.deploy` | Deploy to target environment |
| **Act** | `/pdca.release` | Release management |
| **Act** | `/pdca.fallback` | Rollback on deployment failure |

Commands are chained via handoff relationships: `constitution` → `define` → `clarify` → `plan` → `tasks` → `implement` → `analyze/test` → `review` → `deploy` → `release` → back to `define`.

## Template-Driven Quality: Constraining AI Output With Structure

PDCA Kit's core is not just in the commands themselves, but in the templates behind each command. These templates are not simple fill-in-the-blank documents — they are structural constraints on AI behavior:

### Preventing Premature Implementation Details

The spec template explicitly separates "what" from "how":
- The spec phase **forbids** mentioning tech stacks, API design, or code structure
- Locks AI attention on user needs and business scenarios

### Forcing Explicit Uncertainty Markers

Templates require `[NEEDS CLARIFICATION]` markers for anything unclear — AI is prohibited from guessing. For example:

```
[NEEDS CLARIFICATION: Auth method not specified — email/password? SSO? OAuth?]
```

### Gate Mechanisms

The plan template includes "Phase -1 Gates" — checkpoints that must be passed before implementation begins:
- Project count ≤ 3? (prevent over-engineering)
- Using frameworks directly rather than over-wrapping?
- Contracts defined?

Passing these gates means AI must answer "why this design" before starting implementation.

### Checklist-Driven Self-Review

Every template includes built-in checklists for AI to self-review its output:
- Any unmarked ambiguities remaining?
- Is every requirement testable?
- Are success criteria measurable?

## Extensible: Fit Your Way of Working

PDCA Kit doesn't impose a single fixed process. Through the Extension and Preset systems, you can:

- **Extensions**: Add new commands or development phases. For example, add a security audit phase or a performance testing phase.
- **Presets**: Override template content to fit your team's terminology, organizational standards, or compliance requirements.

Priority mechanism: Project overrides > Presets > Extensions > Core defaults. Override a template in one project without affecting others; install a preset once and it applies everywhere.

## Summary

PDCA-Driven Development is not a new invention. The PDCA cycle has existed for decades, and software development has always operated in a Plan → Build → Test → Release cycle.

What PDCA Kit does is **make this cycle structured, executable, and AI-friendly**. It transforms AI programming from a gamble of "one prompt, one pile of code" into engineering practice with planning, execution, checking, and feedback.

**Plan your work. Do the work. Check the work. Act on what you learn. Repeat.**
