<div align="center">
    <h1> PDCA Kit</h1>
    <h3><em>Plan → Do → Check → Act. AI-driven development, made systematic.</em></h3>
</div>

<p align="center">
    <strong>An open source toolkit that applies the PDCA (Plan-Do-Check-Act) continuous improvement methodology to AI-powered software development.</strong>
</p>

<p align="center">
    <a href="https://github.com/billqbwen/pdca-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/billqbwen/pdca-kit" alt="License"/></a>
</p>

---

> [!WARNING]
> **PDCA Kit is currently in early development.** The project is actively being built and is not yet ready for production use. APIs, commands, and workflows may change. We welcome early feedback and contributions.

---

## 🤔 What is PDCA Kit?

PDCA Kit brings the proven **Plan-Do-Check-Act** (PDCA) methodology to AI coding agents. Instead of ad-hoc "vibe coding," you get a structured, repeatable process for building software with AI — from requirements to deployment, with quality built into every cycle.

### The PDCA Cycle

```
PLAN ──→ DO ──→ CHECK ──→ ACT ──→ (repeat)
```

| Phase | What it means for development |
|-------|------------------------------|
| **Plan** | Define what to build (specs), how to build it (architecture), and break it into tasks |
| **Do** | Execute tasks — the AI coding agent builds the feature step by step |
| **Check** | Validate quality — cross-artifact analysis, code review, testing |
| **Act** | Deploy, release, and feed learnings back into the next Plan cycle |

---

## 🚀 What PDCA Kit Does

### Core Capabilities

- **Project Bootstrapping** — `pdca init` scaffolds your project with templates, scripts, and agent integration in seconds
- **14 AI Agent Commands** — structured slash commands (`/pdca.*`) that guide AI coding agents through the full PDCA lifecycle
- **33 Coding Agent Integrations** — works with Claude, Copilot, Cursor, Windsurf, Gemini CLI, Codex, Qwen, and more
- **Extension System** — add new commands and capabilities beyond the core workflow
- **Preset System** — customize templates and terminology to fit your organization's standards
- **Workflow Engine** — compose multi-step workflows with conditionals, loops, parallel execution, and user prompts

### The Agent Command Workflow

PDCA Kit provides your AI coding agent with these slash commands, chained through a handoff system:

| Command | Phase | What it does |
|---------|-------|-------------|
| `/pdca.constitution` | Plan | Define project governing principles |
| `/pdca.define` | Plan | Create feature specifications from natural language |
| `/pdca.clarify` | Plan | Structured Q&A to resolve ambiguous requirements |
| `/pdca.plan` | Plan | Generate technical implementation plans |
| `/pdca.tasks` | Plan | Break plans into dependency-ordered task lists |
| `/pdca.taskstoissues` | Plan | Convert tasks into GitHub issues |
| `/pdca.implement` | Do | Execute all tasks and build the feature |
| `/pdca.analyze` | Check | Cross-artifact consistency analysis |
| `/pdca.checklist` | Check | Generate quality validation checklists |
| `/pdca.review` | Check | Code review against spec and plan |
| `/pdca.test` | Check | Generate and execute tests |
| `/pdca.deploy` | Act | Deploy to target environment |
| `/pdca.release` | Act | Release management and changelog |
| `/pdca.fallback` | Act | Rollback when deployment fails |

### CLI Management Commands

Manage your PDCA Kit setup from the terminal:

| Command | What it does |
|---------|-------------|
| `pdca init` | Scaffold a new PDCA project |
| `pdca check` | Verify required tools are installed |
| `pdca extension *` | Install, remove, search extensions |
| `pdca preset *` | Install, remove, search presets |
| `pdca integration *` | Manage coding agent integrations |
| `pdca workflow *` | Run and manage multi-step workflows |

---

## 🏗️ Key Design Principles

### Extensible by Design

PDCA Kit is built around a layered override system. Everything — from command prompts to templates — can be customized:

```
Project overrides (.pdca/templates/overrides/)
        ↑
Presets (.pdca/presets/templates/)
        ↑
Extensions (.pdca/extensions/templates/)
        ↑
Core defaults (.pdca/templates/)
```

- **Extensions** add new capabilities (new commands, new workflow phases)
- **Presets** customize how existing commands work (templates, terminology, standards)
- **Project overrides** let you tweak a single project without building a full preset

### Offline-First

All templates, scripts, and commands are bundled into the package. No network calls needed after installation.

### Agent-Agnostic

The same commands work across Claude, Copilot, Cursor, Gemini, and 29+ other coding agents. Choose the agent, keep the methodology.

---

## 📁 What Gets Created

After `pdca init`, your project looks like:

```
my-project/
├── .pdca/
│   ├── memory/
│   │   └── constitution.md          # Project principles
│   ├── templates/
│   │   ├── spec-template.md         # Feature specification template
│   │   ├── plan-template.md         # Implementation plan template
│   │   └── tasks-template.md        # Task breakdown template
│   ├── scripts/                     # Automation scripts (bash/powershell)
│   └── workflows/                   # Built-in PDCA workflow definitions
├── specs/                           # Feature specifications go here
│   └── 001-feature-name/
│       ├── spec.md                  # Feature requirements & user stories
│       ├── plan.md                  # Technical implementation plan
│       ├── tasks.md                 # Executable task list
│       └── ...                      # contracts, data-models, research, etc.
└── .claude/                         # Agent-specific command files
    └── commands/
        ├── pdca.constitution.md
        ├── pdca.define.md
        └── ...
```

---

## 💬 Feedback & Contributing

PDCA Kit is in early development. We welcome:

- **Bug reports and feature requests** via [GitHub Issues](https://github.com/billqbwen/pdca-kit/issues/new)
- **Ideas and discussion** about the PDCA methodology applied to AI-driven development
- **Code contributions** — check the codebase for areas that interest you

---

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.
