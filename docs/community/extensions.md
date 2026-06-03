# Community Extensions

> [!NOTE]
> Community extensions are independently created and maintained by their respective authors. Maintainers only verify that catalog entries are complete and correctly formatted — they do **not review, audit, endorse, or support the extension code itself**. The Community Extensions website is also a third-party resource. Review extension source code before installation and use at your own discretion.

🔍 **Browse and search community extensions on the [Community Extensions website](https://pdca-community.github.io/extensions/).**

The following community-contributed extensions are available in [`catalog.community.json`](https://github.com/github/pdca-kit/blob/main/extensions/catalog.community.json):

**Categories:**

- `docs` — reads, validates, or generates spec artifacts
- `code` — reviews, validates, or modifies source code
- `process` — orchestrates workflow across phases
- `integration` — syncs with external platforms
- `visibility` — reports on project health or progress

**Effect:**

- `Read-only` — produces reports without modifying files
- `Read+Write` — modifies files, creates artifacts, or updates specs

| Extension | Purpose | Category | Effect | URL |
|-----------|---------|----------|--------|-----|
| Agent Assign | Assign specialized Claude Code agents to pdca-kit tasks for targeted execution | `process` | Read+Write | [pdca-kit-agent-assign](https://github.com/xymelon/pdca-kit-agent-assign) |
| Agent Governance | Generate agent-platform repository governance files from PDCA Kit metadata | `process` | Read+Write | [pdca-kit-agent-governance](https://github.com/bigsmartben/pdca-kit-agent-governance) |
| AI-Driven Engineering (AIDE) | A structured 7-step workflow for building new projects from scratch with AI assistants — from vision through implementation | `process` | Read+Write | [aide](https://github.com/mnriem/pdca-kit-extensions/tree/main/aide) |
| API Evolve | Managed API contract evolution — breaking-change detection, semver enforcement, deprecation orchestration, and lifecycle gates across REST, GraphQL, and gRPC | `process` | Read+Write | [pdca-kit-api-evolve](https://github.com/Quratulain-bilal/pdca-kit-api-evolve) |
| Architect Impact Previewer | Predicts architectural impact, complexity, and risks of proposed changes before implementation. | `visibility` | Read-only | [pdca-kit-architect-preview](https://github.com/UmmeHabiba1312/pdca-kit-architect-preview) |
| Architecture Guard | Framework-agnostic architecture review extension for validating implementation against governance and architecture constitutions, detecting architectural drift, and generating non-blocking refactor tasks | `process` | Read+Write | [pdca-kit-architecture-guard](https://github.com/DyanGalih/pdca-kit-architecture-guard) |
| Architecture Workflow | Generate or reverse project-level 4+1 architecture view artifacts and synthesis | `docs` | Read+Write | [pdca-kit-arch](https://github.com/bigsmartben/pdca-kit-arch) |
| Archive Extension | Archive merged features into main project memory. | `docs` | Read+Write | [pdca-kit-archive](https://github.com/stn1slv/pdca-kit-archive) |
| Azure DevOps Integration | Sync user stories and tasks to Azure DevOps work items using OAuth authentication | `integration` | Read+Write | [pdca-kit-azure-devops](https://github.com/pragya247/pdca-kit-azure-devops) |
| Blueprint | Stay code-literate in AI-driven development: review a complete code blueprint for every task from spec artifacts before /pdca.implement runs | `docs` | Read+Write | [pdca-kit-blueprint](https://github.com/chordpli/pdca-kit-blueprint) |
| Branch Convention | Configurable branch and folder naming conventions for /specify with presets and custom patterns | `process` | Read+Write | [pdca-kit-branch-convention](https://github.com/Quratulain-bilal/pdca-kit-branch-convention) |
| Brownfield Bootstrap | Bootstrap pdca-kit for existing codebases — auto-discover architecture and adopt SDD incrementally | `process` | Read+Write | [pdca-kit-brownfield](https://github.com/Quratulain-bilal/pdca-kit-brownfield) |
| BrownKit | Evidence-driven capability discovery, security and QA risk assessment for existing codebases | `process` | Read+Write | [BrownKit](https://github.com/MaksimShevtsov/BrownKit) |
| Bugfix Workflow | Structured bugfix workflow — capture bugs, trace to spec artifacts, and patch specs surgically | `process` | Read+Write | [pdca-kit-bugfix](https://github.com/Quratulain-bilal/pdca-kit-bugfix) |
| Canon | Adds canon-driven (baseline-driven) workflows: spec-first, code-first, spec-drift. Requires Canon Core preset installation. | `process` | Read+Write | [pdca-kit-canon](https://github.com/maximiliamus/pdca-kit-canon/tree/master/extension) |
| Catalog CI | Automated validation for pdca-kit community catalog entries — structure, URLs, diffs, and linting | `process` | Read-only | [pdca-kit-catalog-ci](https://github.com/Quratulain-bilal/pdca-kit-catalog-ci) |
| CI Guard | Spec compliance gates for CI/CD — verify specs exist, check drift, and block merges on gaps | `process` | Read-only | [pdca-kit-ci-guard](https://github.com/Quratulain-bilal/pdca-kit-ci-guard) |
| Checkpoint Extension | Commit the changes made during the middle of the implementation, so you don't end up with just one very large commit at the end | `code` | Read+Write | [pdca-kit-checkpoint](https://github.com/aaronrsun/pdca-kit-checkpoint) |
| Cleanup Extension | Post-implementation quality gate that reviews changes, fixes small issues (scout rule), creates tasks for medium issues, and generates analysis for large issues | `code` | Read+Write | [pdca-kit-cleanup](https://github.com/dsrednicki/pdca-kit-cleanup) |
| Conduct Extension | Orchestrates pdca-kit phases via sub-agent delegation to reduce context pollution. | `process` | Read+Write | [pdca-kit-conduct-ext](https://github.com/twbrandon7/pdca-kit-conduct-ext) |
| Confluence Extension | Create a doc in Confluence summarizing the specifications and planning files | `integration` | Read+Write | [pdca-kit-confluence](https://github.com/aaronrsun/pdca-kit-confluence) |
| Cost Tracker | Track real LLM dollar cost across SDD workflows — per-feature budgets, per-integration comparison, and finance-ready exports | `visibility` | Read+Write | [pdca-kit-cost](https://github.com/Quratulain-bilal/pdca-kit-cost) |
| DocGuard — CDD Enforcement | Canonical-Driven Development enforcement. Validates, scores, and traces project documentation with automated checks, AI-driven workflows, and pdca-kit hooks. Zero NPM runtime dependencies. | `docs` | Read+Write | [pdca-kit-docguard](https://github.com/raccioly/docguard) |
| Extensify | Create and validate extensions and extension catalogs | `process` | Read+Write | [extensify](https://github.com/mnriem/pdca-kit-extensions/tree/main/extensify) |
| Fix Findings | Automated analyze-fix-reanalyze loop that resolves spec findings until clean | `code` | Read+Write | [pdca-kit-fix-findings](https://github.com/Quratulain-bilal/pdca-kit-fix-findings) |
| FixIt Extension | Spec-aware bug fixing — maps bugs to spec artifacts, proposes a plan, applies minimal changes | `code` | Read+Write | [pdca-kit-fixit](https://github.com/pdca-community/pdca-kit-fixit) |
| Fleet Orchestrator | Orchestrate a full feature lifecycle with human-in-the-loop gates across all SpecKit phases | `process` | Read+Write | [pdca-kit-fleet](https://github.com/sharathsatish/pdca-kit-fleet) |
| GitHub Issues Integration 1 | Generate spec artifacts from GitHub Issues - import issues, sync updates, and maintain bidirectional traceability | `integration` | Read+Write | [pdca-kit-github-issues](https://github.com/Fatima367/pdca-kit-github-issues) |
| GitHub Issues Integration 2 | Creates and syncs local specs from an existing GitHub issue | `integration` | Read+Write | [pdca-kit-issue](https://github.com/aaronrsun/pdca-kit-issue) |
| Interactive HTML Preview | Generate self-contained interactive HTML prototypes from PDCA Kit artifacts | `docs` | Read+Write | [pdca-kit-preview](https://github.com/bigsmartben/pdca-kit-preview) |
| Intelligent Agent Orchestrator | Cross-catalog agent discovery and intelligent prompt-to-command routing | `process` | Read+Write | [pdca-kit-orchestrator](https://github.com/pragya247/pdca-kit-orchestrator) |
| Iterate | Iterate on spec documents with a two-phase define-and-apply workflow — refine specs mid-implementation and go straight back to building | `docs` | Read+Write | [pdca-kit-iterate](https://github.com/imviancagrace/pdca-kit-iterate) |
| Jira Integration | Create Jira Epics, Stories, and Issues from pdca-kit specifications and task breakdowns with configurable hierarchy and custom field support | `integration` | Read+Write | [pdca-kit-jira](https://github.com/mbachorik/pdca-kit-jira) |
| Learning Extension | Generate educational guides from implementations and enhance clarifications with mentoring context | `docs` | Read+Write | [pdca-kit-learn](https://github.com/imviancagrace/pdca-kit-learn) |
| Linear Integration | Mirror pdca-kit feature directories into Linear (filesystem → Linear, reconcile-based, unidirectional). | `integration` | Read+Write | [pdca-kit-linear](https://github.com/ashbrener/pdca-kit-linear) |
| MAQA — Multi-Agent & Quality Assurance | Coordinator → feature → QA agent workflow with parallel worktree-based implementation. Language-agnostic. Auto-detects installed board plugins. Optional CI gate. | `process` | Read+Write | [pdca-kit-maqa-ext](https://github.com/GenieRobot/pdca-kit-maqa-ext) |
| MAQA Azure DevOps Integration | Azure DevOps Boards integration for MAQA — syncs User Stories and Task children as features progress | `integration` | Read+Write | [pdca-kit-maqa-azure-devops](https://github.com/GenieRobot/pdca-kit-maqa-azure-devops) |
| MAQA CI/CD Gate | Auto-detects GitHub Actions, CircleCI, GitLab CI, and Bitbucket Pipelines. Blocks QA handoff until pipeline is green. | `process` | Read+Write | [pdca-kit-maqa-ci](https://github.com/GenieRobot/pdca-kit-maqa-ci) |
| MAQA GitHub Projects Integration | GitHub Projects v2 integration for MAQA — syncs draft issues and Status columns as features progress | `integration` | Read+Write | [pdca-kit-maqa-github-projects](https://github.com/GenieRobot/pdca-kit-maqa-github-projects) |
| MAQA Jira Integration | Jira integration for MAQA — syncs Stories and Subtasks as features progress through the board | `integration` | Read+Write | [pdca-kit-maqa-jira](https://github.com/GenieRobot/pdca-kit-maqa-jira) |
| MAQA Linear Integration | Linear integration for MAQA — syncs issues and sub-issues across workflow states as features progress | `integration` | Read+Write | [pdca-kit-maqa-linear](https://github.com/GenieRobot/pdca-kit-maqa-linear) |
| MAQA Trello Integration | Trello board integration for MAQA — populates board from specs, moves cards, real-time checklist ticking | `integration` | Read+Write | [pdca-kit-maqa-trello](https://github.com/GenieRobot/pdca-kit-maqa-trello) |
| MarkItDown Document Converter | Convert documents (PDF, Word, PowerPoint, Excel, and more) to Markdown for use as spec reference material | `docs` | Read+Write | [pdca-kit-markitdown](https://github.com/BenBtg/pdca-kit-markitdown) |
| MDE | Minimal model-driven engineering workflow with setup, next, and status commands | `process` | Read+Write | [pdca-kit-mde](https://github.com/AI-MDE/pdca-kit-mde) |
| Memory Loader | Loads .pdca/memory/ files before lifecycle commands so LLM agents have project governance context | `docs` | Read-only | [pdca-kit-memory-loader](https://github.com/KevinBrown5280/pdca-kit-memory-loader) |
| Memory MD | PDCA Kit extension for repository-native Markdown memory that captures durable decisions, bugs, and project context | `docs` | Read+Write | [pdca-kit-memory-hub](https://github.com/DyanGalih/pdca-kit-memory-hub) |
| MemoryLint | Agent memory governance tool: Automatically audits and fixes boundary conflicts between AGENTS.md and the constitution. | `process` | Read+Write | [memorylint](https://github.com/RbBtSn0w/pdca-kit-extensions/tree/main/memorylint) |
| Microsoft 365 Integration | Fetch Teams messages, meeting transcripts, and SharePoint/OneDrive files as local Markdown for spec generation | `integration` | Read+Write | [pdca-kit-m365](https://github.com/BenBtg/pdca-kit-m365) |
| Multi-Model Review | Cross-model PDCA Kit handoffs for spec authoring, implementation routing, and review. | `process` | Read+Write | [multi-model-review](https://github.com/formin/multi-model-review) |
| Multi-Sites PDCA Kit | Multi-site aware specify command with per-site spec folders, auto-increment, and Drupal support | `process` | Read+Write | [pdca-kit-multi-sites](https://github.com/teeyo/pdca-kit-multi-sites) |
| .NET Framework to Modern .NET Migration | Orchestrate end-to-end .NET Framework to modern .NET migration across 7 phases, with SDD lifecycle integration | `process` | Read+Write | [pdca-kit-fx-to-net](https://github.com/RogerBestMsft/pdca-kit-FxToNet) |
| Onboard | Contextual onboarding and progressive growth for developers new to pdca-kit projects. Explains specs, maps dependencies, validates understanding, and guides the next step | `process` | Read+Write | [pdca-kit-onboard](https://github.com/dmux/pdca-kit-onboard) |
| Optimize | Audit and optimize AI governance for context efficiency — token budgets, rule health, interpretability, compression, coherence, and echo detection | `process` | Read+Write | [pdca-kit-optimize](https://github.com/sakitA/pdca-kit-optimize) |
| OWASP LLM Threat Model | OWASP Top 10 for LLM Applications 2025 threat analysis on agent artifacts | `code` | Read-only | [pdca-kit-threatmodel](https://github.com/NaviaSamal/pdca-kit-threatmodel) |
| Plan Review Gate | Require spec.md and plan.md to be merged via MR/PR before allowing task generation | `process` | Read-only | [pdca-kit-plan-review-gate](https://github.com/luno/pdca-kit-plan-review-gate) |
| PR Bridge | Auto-generate pull request descriptions, checklists, and summaries from spec artifacts | `process` | Read-only | [pdca-kit-pr-bridge-](https://github.com/Quratulain-bilal/pdca-kit-pr-bridge-) |
| Presetify | Create and validate presets and preset catalogs | `process` | Read+Write | [presetify](https://github.com/mnriem/pdca-kit-extensions/tree/main/presetify) |
| Product Forge | Full product lifecycle from research to release — express/lite/standard/v-model tracks, living spec + traceability, structured journeys → E2E, monorepo, and selectable doc-structure strategies | `process` | Read+Write | [pdca-product-forge](https://github.com/VaiYav/pdca-product-forge) |
| Product Spec Extension | Generates PRFAQ, Lean PRD, stakeholder summaries, and technical designs from engineering specs | `docs` | Read+Write | [pdca-kit-product](https://github.com/d0whc3r/pdca-kit-product) |
| Project Health Check | Diagnose a PDCA Kit project and report health issues across structure, agents, features, scripts, extensions, and git | `visibility` | Read-only | [pdca-kit-doctor](https://github.com/KhawarHabibKhan/pdca-kit-doctor) |
| Project Status | Show current SDD workflow progress — active feature, artifact status, task completion, workflow phase, and extensions summary | `visibility` | Read-only | [pdca-kit-status](https://github.com/KhawarHabibKhan/pdca-kit-status) |
| QA Testing Extension | Systematic QA testing with browser-driven or CLI-based validation of acceptance criteria from spec | `code` | Read-only | [pdca-kit-qa](https://github.com/arunt14/pdca-kit-qa) |
| RAG Azure Builder | PDCA Kit extension for onboarding and operating an Azure RAG stack with guided workflows. | `process` | Read+Write | [pdca-kit-extension-rag-azure-builder](https://github.com/Sertxito/pdca-kit-extension-rag-azure-builder) |
| Ralph Loop | Autonomous implementation loop using AI agent CLI | `code` | Read+Write | [pdca-kit-ralph](https://github.com/Rubiss-Projects/pdca-kit-ralph) |
| Reconcile Extension | Reconcile implementation drift by surgically updating feature artifacts. | `docs` | Read+Write | [pdca-kit-reconcile](https://github.com/stn1slv/pdca-kit-reconcile) |
| Red Team | Adversarial review of specs before /pdca.plan — parallel lens agents surface risks that clarify/analyze structurally can't (prompt injection, integrity gaps, cross-spec drift, silent failures). Produces a structured findings report; no auto-edits to specs. | `docs` | Read+Write | [pdca-kit-red-team](https://github.com/ashbrener/pdca-kit-red-team) |
| Repository Index | Generate index for existing repo for overview, architecture and module level. | `docs` | Read-only | [pdca-kit-repoindex](https://github.com/liuyiyu/pdca-kit-repoindex) |
| Reqnroll BDD | Adds Reqnroll BDD planning, Gherkin generation, traceability, safe task injection, handoff, and verification to PDCA Kit | `process` | Read+Write | [pdca-kit-reqnroll-bdd](https://github.com/LoogacyStudio/pdca-kit-reqnroll-bdd) |
| Retro Extension | Sprint retrospective analysis with metrics, spec accuracy assessment, and improvement suggestions | `process` | Read+Write | [pdca-kit-retro](https://github.com/arunt14/pdca-kit-retro) |
| Retrospective Extension | Post-implementation retrospective with spec adherence scoring, drift analysis, and human-gated spec updates | `docs` | Read+Write | [pdca-kit-retrospective](https://github.com/emi-dm/pdca-kit-retrospective) |
| Review Extension | Post-implementation comprehensive code review with specialized agents for code quality, comments, tests, error handling, type design, and simplification | `code` | Read-only | [pdca-kit-review](https://github.com/ismaelJimenez/pdca-kit-review) |
| Ripple | Detect side effects that tests can't catch after implementation — delta-anchored analysis across 9 domain-agnostic categories | `code` | Read+Write | [pdca-kit-ripple](https://github.com/chordpli/pdca-kit-ripple) |
| SDD Utilities | Resume interrupted workflows, validate project health, and verify spec-to-task traceability | `process` | Read+Write | [pdca-utils](https://github.com/mvanhorn/pdca-utils) |
| Security Review | Full-project secure-by-design security audits plus staged, branch/PR, plan, task, follow-up, and apply reviews | `code` | Read+Write | [pdca-kit-security-review](https://github.com/DyanGalih/pdca-kit-security-review) |
| SFPDCA | Enterprise Salesforce SDLC with 18 commands for the full SDD lifecycle. | `process` | Read+Write | [pdca-kit-sf](https://github.com/ysumanth06/pdca-kit-sf) |
| Ship Release Extension | Automates release pipeline: pre-flight checks, branch sync, changelog generation, CI verification, and PR creation | `process` | Read+Write | [pdca-kit-ship](https://github.com/arunt14/pdca-kit-ship) |
| Spec Changelog | Auto-generate changelogs and release notes from spec git history and requirement diffs | `docs` | Read-only | [pdca-kit-changelog](https://github.com/Quratulain-bilal/pdca-kit-changelog) |
| Spec Critique Extension | Dual-lens critical review of spec and plan from product strategy and engineering risk perspectives | `docs` | Read-only | [pdca-kit-critique](https://github.com/arunt14/pdca-kit-critique) |
| Spec Diagram | Auto-generate Mermaid diagrams of SDD workflow state, feature progress, and task dependencies | `visibility` | Read-only | [pdca-kit-diagram-](https://github.com/Quratulain-bilal/pdca-kit-diagram-) |
| PDCA Kit Schedule | Optimal multi-agent task scheduling via CP-SAT — DAG precedence, hallucination-aware caps, file-conflict avoidance, stochastic durations, replanning, and interactive HTML output | `process` | Read+Write | [pdca-kit-schedule](https://github.com/jfranc38/pdca-kit-schedule) |
| Spec Orchestrator | Cross-feature orchestration — track state, select tasks, and detect conflicts across parallel specs | `process` | Read-only | [pdca-kit-orchestrator](https://github.com/Quratulain-bilal/pdca-kit-orchestrator) |
| Spec Reference Loader | Reads the ## References section from the feature spec and loads only the listed docs into context | `docs` | Read-only | [pdca-kit-spec-reference-loader](https://github.com/KevinBrown5280/pdca-kit-spec-reference-loader) |
| Spec Refine | Update specs in-place, propagate changes to plan and tasks, and diff impact across artifacts | `process` | Read+Write | [pdca-kit-refine](https://github.com/Quratulain-bilal/pdca-kit-refine) |
| Spec Scope | Effort estimation and scope tracking — estimate work, detect creep, and budget time per phase | `process` | Read-only | [pdca-kit-scope-](https://github.com/Quratulain-bilal/pdca-kit-scope-) |
| Spec Sync | Detect and resolve drift between specs and implementation. AI-assisted resolution with human approval | `docs` | Read+Write | [pdca-kit-sync](https://github.com/bgervin/pdca-kit-sync) |
| Spec Validate | Comprehension validation, review gating, and approval state for pdca-kit artifacts — staged quizzes, peer review SLA, and a hard gate before /pdca.implement | `process` | Read+Write | [pdca-kit-spec-validate](https://github.com/aeltayeb/pdca-kit-spec-validate) |
| Spec2Cloud | Spec-driven workflow tuned for shipping to Azure | `process` | Read+Write | [spec2cloud](https://github.com/Azure-Samples/Spec2Cloud) |
| SpecTest | Auto-generate test scaffolds from spec criteria, map coverage, and find untested requirements | `code` | Read+Write | [pdca-kit-spectest](https://github.com/Quratulain-bilal/pdca-kit-spectest) |
| Squad Bridge | Bootstrap and synchronize a Squad agent team from your PDCA spec and tasks. | `process` | Read+Write | [pdca-kit-squad](https://github.com/jwill824/pdca-kit-squad) |
| Staff Review Extension | Staff-engineer-level code review that validates implementation against spec, checks security, performance, and test coverage | `code` | Read-only | [pdca-kit-staff-review](https://github.com/arunt14/pdca-kit-staff-review) |
| Status Report | Project status, feature progress, and next-action recommendations for spec-driven workflows | `visibility` | Read-only | [Open-Agent-Tools/pdca-kit-status](https://github.com/Open-Agent-Tools/pdca-kit-status) |
| Superpowers Bridge | Orchestrates obra/superpowers skills within the pdca-kit SDD workflow across the full lifecycle (clarification, TDD, review, verification, critique, debugging, branch completion) | `process` | Read+Write | [superpowers-bridge](https://github.com/RbBtSn0w/pdca-kit-extensions/tree/main/superpowers-bridge) |
| Superpowers Implementation Bridge | Thin orchestrator between PDCA Kit (design) and Superpowers (implementation). Cross-agent. | `process` | Read+Write | [pdca-superpowers-bridge](https://github.com/lihan3238/pdca-superpowers-bridge) |
| Superspec | Bridges pdca-kit with obra/superpowers (brainstorming, TDD, subagent, code-review) into a unified, resumable workflow with graceful degradation and session progress tracking | `process` | Read+Write | [superspec](https://github.com/WangX0111/superspec) |
| Team Assign | Assign tasks.md items to human engineers, split into subtasks, and generate a per-engineer workboard | `process` | Read+Write | [pdca-kit-team-assign](https://github.com/tarunkumarbhati/pdca-kit-team-assign) |
| Time Machine | Retroactively apply the full SDD workflow to existing codebases — analyse, spec, and ship feature-by-feature | `process` | Read+Write | [pdca-kit-time-machine](https://github.com/teeyo/pdca-kit-time-machine) |
| TinySpec | Lightweight single-file workflow for small tasks — skip the heavy multi-step SDD process | `process` | Read+Write | [pdca-kit-tinyspec](https://github.com/Quratulain-bilal/pdca-kit-tinyspec) |
| Token Budget | Reduces LLM token consumption in PDCA Kit workflows: compact artifacts in-place, scope per-phase reading, suppress prose padding, and report token usage | `process` | Read+Write | [pdca-kit-token-budget](https://github.com/tinesoft/pdca-kit-token-budget) |
| Token Consumption Analyzer | Captures, analyzes, and compares token consumption across SDD workflows | `visibility` | Read-only | [pdca-kit-token-analyzer](https://github.com/coderandhiker/pdca-kit-token-analyzer) |
| V-Model Extension Pack | Enforces V-Model paired generation of development specs and test specs with full traceability | `docs` | Read+Write | [pdca-kit-v-model](https://github.com/leocamello/pdca-kit-v-model) |
| Verify Extension | Post-implementation quality gate that validates implemented code against specification artifacts | `code` | Read-only | [pdca-kit-verify](https://github.com/ismaelJimenez/pdca-kit-verify) |
| Verify Tasks Extension | Detect phantom completions: tasks marked [X] in tasks.md with no real implementation | `code` | Read-only | [pdca-kit-verify-tasks](https://github.com/datastone-inc/pdca-kit-verify-tasks) |
| Version Guard | Verify tech stack versions against live npm registries before planning and implementation | `process` | Read-only | [pdca-kit-version-guard](https://github.com/KevinBrown5280/pdca-kit-version-guard) |
| What-if Analysis | Preview the downstream impact (complexity, effort, tasks, risks) of requirement changes before committing to them | `visibility` | Read-only | [pdca-kit-whatif](https://github.com/DevAbdullah90/pdca-kit-whatif) |
| Wireframe Visual Feedback Loop | SVG wireframe generation, review, and sign-off for spec-driven development. Approved wireframes become spec constraints honored by /pdca.plan, /pdca.tasks, and /pdca.implement | `visibility` | Read+Write | [pdca-kit-extension-wireframe](https://github.com/TortoiseWolfe/pdca-kit-extension-wireframe) |
| Work IQ | Integrate Microsoft 365 organizational knowledge into spec-driven development workflows | `integration` | Read-only | [pdca-kit-workiq](https://github.com/sakitA/pdca-kit-workiq) |
| Worktree Isolation | Spawn isolated git worktrees for parallel feature development without checkout switching | `process` | Read+Write | [pdca-kit-worktree](https://github.com/Quratulain-bilal/pdca-kit-worktree) |
| Worktrees | Default-on worktree isolation for parallel agents — sibling or nested layout | `process` | Read+Write | [pdca-kit-worktree-parallel](https://github.com/dango85/pdca-kit-worktree-parallel) |

To submit your own extension, see the [Extension Publishing Guide](https://github.com/github/pdca-kit/blob/main/extensions/EXTENSION-PUBLISHING-GUIDE.md).
