# PDCA Kit — User Guide

> **Plan → Do → Check → Act. AI-driven development, made systematic.**

This guide covers everything you need to install, configure, and run PDCA Kit on your machine, including how to set up your AI coding agent (the "model" side of the equation).

---

## Table of Contents

1. [What is PDCA Kit?](#1-what-is-pdca-kit)
2. [Prerequisites](#2-prerequisites)
3. [Installation](#3-installation)
   - [Persistent Install (Recommended)](#persistent-install-recommended)
   - [One-time Usage](#one-time-usage)
   - [Alternative: pipx](#alternative-pipx)
   - [Enterprise / Air-Gapped Install](#enterprise--air-gapped-install)
4. [Initializing a Project](#4-initializing-a-project)
5. [Configuring Your AI Model (Coding Agent)](#5-configuring-your-ai-model-coding-agent)
   - [How PDCA Kit Interacts with AI Models](#how-pdca-kit-interacts-with-ai-models)
   - [Agent-specific Setup](#agent-specific-setup)
   - [Switching or Adding Agents](#switching-or-adding-agents)
6. [Running the PDCA Workflow](#6-running-the-pdca-workflow)
7. [Verification & Diagnostics](#7-verification--diagnostics)
8. [Upgrading](#8-upgrading)
9. [Uninstallation](#9-uninstallation)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. What is PDCA Kit?

PDCA Kit is an **open-source CLI toolkit** that applies the **Plan-Do-Check-Act (PDCA)** continuous-improvement methodology to AI-assisted software development. It does **not** replace your AI coding agent — instead, it gives your agent a structured, repeatable workflow through slash commands.

| Phase | What it means |
|-------|---------------|
| **Plan** | Define what to build (specs), how to build it (architecture), and break it into tasks |
| **Do** | Execute tasks — the AI coding agent builds the feature step by step |
| **Check** | Validate quality — cross-artifact analysis, code review, testing |
| **Act** | Deploy, release, and feed learnings back into the next Plan cycle |

PDCA Kit provides **14 slash commands** (`/pdca.constitution`, `/pdca.define`, `/pdca.plan`, etc.) and supports **30+ AI coding agents** including Claude Code, GitHub Copilot, Cursor, Gemini CLI, Codex, Windsurf, and more.

---

## 2. Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| **Python** | 3.11+ | |
| **Git** | Any recent version | |
| **uv** (recommended) | Latest | [Install guide](https://docs.astral.sh/uv/) |
| **An AI coding agent** | Varies | At least one of the [30 supported agents](#5-configuring-your-ai-model-coding-agent) |

**Operating Systems:** Linux, macOS, and Windows (PowerShell scripts supported without WSL).

> **Tip:** You can use `pip` directly instead of `uv`, but `uv` is faster and the officially recommended method.

---

## 3. Installation

PDCA Kit is installed from the official GitHub repository. It is **not yet published on PyPI** — any package named `pdca-cli` on PyPI is unrelated and unsupported.

### Persistent Install (Recommended)

Install once and use the `pdca` command anywhere:

```bash
# Install uv first if you don't have it:
# curl -LsSf https://astral.sh/uv/install.sh | sh

# Install PDCA Kit (replace vX.Y.Z with a release tag)
uv tool install pdca-cli --from git+https://github.com/billqbwen/pdca-kit.git@vX.Y.Z

# For the latest development version (use with caution):
uv tool install pdca-cli --from git+https://github.com/billqbwen/pdca-kit.git
```

Verify the installation:

```bash
pdca version
pdca --help
```

### One-time Usage

Run directly without installing (great for trying it out):

```bash
uvx --from git+https://github.com/billqbwen/pdca-kit.git pdca --help
uvx --from git+https://github.com/billqbwen/pdca-kit.git pdca init my-project --integration copilot
```

### Alternative: pipx

```bash
pipx install git+https://github.com/billqbwen/pdca-kit.git
# Then use directly:
pdca init my-project --integration claude
```

### Enterprise / Air-Gapped Install

If your environment blocks PyPI or GitHub, build a wheel locally and transfer it:

```bash
# On a machine with internet access:
git clone https://github.com/billqbwen/pdca-kit.git
cd pdca-kit
uv build          # produces dist/pdca_cli-*.whl

# Transfer the .whl file to the target machine, then:
uv tool install /path/to/pdca_cli-*.whl
```

All templates, scripts, and commands are bundled into the package — no network calls are needed after installation.

---

## 4. Initializing a Project

After installing the CLI, scaffold a new project:

```bash
# Create a new project directory
pdca init my-project --integration copilot
cd my-project

# Or initialize in the current directory
pdca init . --integration claude
```

### Key `pdca init` Options

| Option | Description |
|--------|-------------|
| `--integration <key>` | Choose your AI coding agent (e.g., `claude`, `copilot`, `gemini`, `codebuddy`) |
| `--script sh\|ps` | Force shell (`sh`) or PowerShell (`ps`) scripts |
| `--preset <name>` | Apply a preset during initialization |
| `--no-git` | Skip git repository initialization |
| `--ignore-agent-tools` | Skip checking whether the agent CLI is installed |
| `--force` | Overwrite existing files without prompting (for upgrades) |

### What Gets Created

```
my-project/
├── .pdca/
│   ├── memory/constitution.md      # Project principles
│   ├── templates/                  # Spec, plan, tasks templates
│   ├── scripts/                    # Automation scripts (bash/ps1)
│   └── workflows/                  # Built-in PDCA workflow definitions
├── specs/                          # Feature specifications go here
│   └── 001-feature-name/
│       ├── spec.md                 # Feature requirements & user stories
│       ├── plan.md                 # Technical implementation plan
│       └── tasks.md                # Executable task list
└── .claude/ (or agent-specific)    # Slash command files
    └── commands/
        ├── pdca.constitution.md
        ├── pdca.define.md
        └── ...
```

---

## 5. Configuring Your AI Model (Coding Agent)

### How PDCA Kit Interacts with AI Models

PDCA Kit is **agent-agnostic** — it does not contain or configure AI models directly. Instead, it installs structured **slash commands** (markdown/TOML/YAML files) into your AI coding agent's commands directory. When you invoke `/pdca.define` or `/pdca.plan` in your agent's chat interface, the agent reads the command file and executes the workflow.

**The AI model is whatever model your chosen coding agent is configured to use.** PDCA Kit simply provides the methodology layer on top.

### Agent-specific Setup

Below are setup instructions for the most common agents. For all 30+ supported agents, run `pdca integration list`.

#### Claude Code (Anthropic)

```bash
# 1. Install Claude Code if you haven't:
#    https://docs.anthropic.com/en/docs/claude-code/overview

# 2. Initialize PDCA Kit with Claude integration:
pdca init my-project --integration claude
cd my-project

# 3. Claude Code will read commands from .claude/skills/
#    Open the project in Claude Code and use /pdca.constitution to start
```

**AI Model Configuration for Claude Code:**
- Claude Code uses your Anthropic API key. Set it via:
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-..."
  ```
- Model selection is managed by Claude Code itself (defaults to the latest Claude model). You can change models with `claude --model` or `/model` within Claude Code.

#### GitHub Copilot

```bash
# 1. Install GitHub Copilot extension in VS Code

# 2. Initialize PDCA Kit:
pdca init my-project --integration copilot
cd my-project

# 3. Open the project in VS Code — commands are in .github/prompts/
#    Use @pdca.define in Copilot Chat to start
```

**AI Model Configuration for Copilot:**
- Copilot model selection is managed through your GitHub account settings or VS Code Copilot settings.
- Available models: GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash, etc.
- Change model: Click the Copilot icon in VS Code status bar → select model.

#### Gemini CLI (Google)

```bash
# 1. Install Gemini CLI:
#    https://github.com/google-gemini/gemini-cli

# 2. Initialize:
pdca init my-project --integration gemini
cd my-project

# 3. Commands are installed in .gemini/commands/
```

**AI Model Configuration for Gemini CLI:**
- Set your Google API key:
  ```bash
  export GEMINI_API_KEY="your-api-key"
  ```
- Gemini CLI defaults to the latest Gemini model. Check Gemini CLI docs for model switching options.

#### CodeBuddy CLI

```bash
# 1. Install CodeBuddy CLI:
#    https://www.codebuddy.ai/cli

# 2. Initialize:
pdca init my-project --integration codebuddy
cd my-project

# 3. Commands are in .codebuddy/commands/
```

**AI Model Configuration for CodeBuddy:**
- CodeBuddy model configuration is handled by the CodeBuddy CLI itself. Refer to [CodeBuddy documentation](https://www.codebuddy.ai/docs) for model selection.

#### Cursor

```bash
# Cursor is IDE-based — no CLI needed
pdca init my-project --integration cursor-agent
# Open the project in Cursor IDE
```

**AI Model Configuration for Cursor:**
- In Cursor: Settings → Models → select your preferred model (GPT-4o, Claude 3.5 Sonnet, etc.).
- API keys are configured in Cursor Settings.

#### Codex CLI (OpenAI)

```bash
# 1. Install Codex CLI:
#    https://github.com/openai/codex

# 2. Initialize with skills mode:
pdca init my-project --integration codex
cd my-project

# 3. Skills are in .agents/skills/
```

**AI Model Configuration for Codex:**
- Set your OpenAI API key:
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```
- Codex uses OpenAI models by default. Check Codex docs for model configuration.

#### Windsurf

```bash
# Windsurf is IDE-based
pdca init my-project --integration windsurf
# Open the project in Windsurf IDE
```

#### Generic / Custom Agent

If your agent isn't listed in the 30+ supported integrations:

```bash
pdca init my-project --integration generic \
  --integration-options="--commands-dir .myagent/cmds"
```

### Switching or Adding Agents

You can switch agents or use multiple agents in the same project:

```bash
# List all available integrations
pdca integration list

# Switch to a different agent
pdca integration switch claude

# Install an additional agent alongside the current one
pdca integration install gemini

# Set the default agent
pdca integration use copilot
```

> **Note:** Some agent combinations require `--force` if they share command directories. Multi-install safe agents (like Claude, CodeBuddy, Gemini, Cursor) can coexist without issues.

---

## 6. Running the PDCA Workflow

Once your project is initialized and your agent is configured, open the project in your AI coding agent and follow the PDCA cycle:

### Full Quality-Gate Workflow

```
/pdca.constitution → /pdca.define → /pdca.clarify → /pdca.checklist
→ /pdca.plan → /pdca.tasks → /pdca.analyze → /pdca.implement
```

### Quick Experiment Path (Lean)

```
/pdca.define → /pdca.plan → /pdca.tasks → /pdca.implement
```

### All Available Slash Commands

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

### Example Session

```
# In your AI coding agent's chat:

/pdca.constitution This project follows TDD. Use functional patterns. Prefer simplicity.

/pdca.define Build a REST API for a task management app. Users can create,
update, delete tasks. Tasks have status (todo, in-progress, done) and
assignee. No authentication needed for v1.

/pdca.clarify Focus on error handling and edge cases for task status transitions.

/pdca.plan Use Python with FastAPI. SQLite for storage. Pydantic for validation.
No ORM — raw SQL. Structure as a single module for simplicity.

/pdca.tasks

/pdca.analyze

/pdca.implement
```

---

## 7. Verification & Diagnostics

```bash
# Check that PDCA Kit is working and all required tools are installed
pdca check

# Show current version
pdca version

# Check if a newer version is available
pdca self check

# List installed integrations
pdca integration list

# List available presets
pdca preset list

# List available extensions
pdca extension list
```

---

## 8. Upgrading

### Upgrade the CLI Tool

```bash
# If installed with uv:
uv tool install pdca-cli --force --from git+https://github.com/billqbwen/pdca-kit.git@vX.Y.Z

# If installed with pipx:
pipx install --force git+https://github.com/billqbwen/pdca-kit.git@vX.Y.Z
```

### Update Project Files

Inside your project directory:

```bash
# Update slash commands, templates, and scripts
pdca init --here --force --integration <your-agent>

# ⚠️  This will overwrite .pdca/memory/constitution.md — back it up first:
cp .pdca/memory/constitution.md .pdca/memory/constitution-backup.md
pdca init --here --force --integration copilot
mv .pdca/memory/constitution-backup.md .pdca/memory/constitution.md
```

> **Safe:** Your `specs/` directory (specifications, plans, tasks) and source code are **never touched** during upgrades.

---

## 9. Uninstallation

This section covers how to completely remove PDCA Kit from your machine and from individual projects.

### Uninstall from a Project (Remove PDCA Kit Integration)

To remove PDCA Kit's agent integration from a specific project without deleting your code or specs:

```bash
cd my-project

# 1. Uninstall the current coding agent integration
pdca integration uninstall

# If you have multiple integrations installed, specify the key:
pdca integration uninstall claude
pdca integration uninstall copilot
```

| Option | Description |
|--------|-------------|
| `--force` | Remove all integration files, even if you've modified them locally |

**What gets removed:**
- Agent-specific command files (e.g., `.claude/skills/`, `.github/prompts/`)
- Agent context file sections (e.g., managed PDCA Kit section in `CLAUDE.md`)
- Integration state tracking in `.pdca/integration.json`

**What stays untouched:**
- Your `.pdca/` directory (templates, scripts, memory, workflows)
- Your `specs/` directory (all feature specifications, plans, and tasks)
- Your source code
- Your git history

> **Tip:** PDCA Kit tracks every file it creates with SHA-256 hashes. Modified files are preserved automatically during uninstall — only unmodified files are removed. Use `--force` to remove everything.

### Remove PDCA Kit Infrastructure Entirely from a Project

To completely strip PDCA Kit from a project (including templates, scripts, and memory):

```bash
cd my-project

# 1. Uninstall agent integrations first
pdca integration uninstall --force

# 2. Remove the PDCA Kit infrastructure directory
rm -rf .pdca/

# 3. Remove the specs directory if you no longer need it
rm -rf specs/

# 4. Remove agent context file sections manually if needed.
#    The managed section is delimited by:
#    <!-- PDCA START --> ... <!-- PDCA END -->
#    You can safely delete these markers and everything between them
#    from files like CLAUDE.md, GEMINI.md, CODEBUDDY.md, etc.
```

### Uninstall the PDCA CLI Tool from Your Machine

#### If installed with `uv tool install` (recommended method):

```bash
# Uninstall the pdca command
uv tool uninstall pdca-cli

# Verify it's gone
which pdca   # Should return "pdca not found"
```

#### If installed with `pipx`:

```bash
pipx uninstall pdca-cli
```

#### If installed with `pip` (editable install):

```bash
pip uninstall pdca-cli
```

#### Clean up leftover data (optional):

```bash
# Remove uv tool cache (if using uv)
uv cache clean pdca-cli

# Remove any pip/pipx caches
pip cache purge
```

### Uninstall a Specific Agent's CLI Tool

PDCA Kit does not manage the installation of your AI coding agent tools. To uninstall the agent itself, refer to the agent's own documentation:

| Agent | Uninstall Command |
|-------|------------------|
| Claude Code | `npm uninstall -g @anthropic-ai/claude-code` |
| Gemini CLI | `npm uninstall -g @google/gemini-cli` |
| Codex CLI | `npm uninstall -g @openai/codex` |
| CodeBuddy CLI | Follow [CodeBuddy docs](https://www.codebuddy.ai/docs) |
| GitHub Copilot | Uninstall the VS Code extension |
| Cursor / Windsurf | Uninstall the IDE application |

---

## 10. Troubleshooting

### `pdca: command not found`

```bash
# Check if pdca-cli is installed
uv tool list

# If not installed:
uv tool install pdca-cli --from git+https://github.com/billqbwen/pdca-kit.git

# Verify PATH
which pdca
# Should point to ~/.local/bin/pdca or similar
```

### Slash commands not showing up in the agent

1. **Restart your IDE/editor completely** (not just "Reload Window")
2. **Verify command files exist:**
   ```bash
   ls .claude/skills/       # Claude Code
   ls .github/prompts/      # GitHub Copilot
   ls .gemini/commands/     # Gemini CLI
   ls .codebuddy/commands/  # CodeBuddy
   ```
3. **Ensure you're in the correct project directory** where `pdca init` was run

### `ModuleNotFoundError` when running locally

```bash
# Install dependencies:
uv pip install -e .
# Or:
pip install -e .
```

### Agent CLI tool not found

Some agents require their CLI to be installed separately. Run `pdca integration list` to see which agents require a CLI (`requires_cli: True`). Install the agent CLI first, or use `--ignore-agent-tools` during init:

```bash
pdca init my-project --integration claude --ignore-agent-tools
```

### Scripts not executable on Linux/macOS

```bash
chmod +x .pdca/scripts/bash/*.sh
```

Or force shell scripts during init:
```bash
pdca init my-project --integration copilot --script sh
```

### Duplicate slash commands after upgrade

Some IDE-based agents (Kilo Code, Windsurf) may show duplicates. Delete old command files from the agent's commands folder and restart the IDE.

---

## Next Steps

- Read the [Quick Start Guide](quickstart.md) for a detailed walkthrough
- Explore [all supported integrations](reference/integrations.md)
- Browse [community presets and extensions](community/presets.md)
- Read the [full PDCA methodology](pdca-driven.md)
- Report issues on [GitHub](https://github.com/billqbwen/pdca-kit/issues)

---

<p class="text-end small text-body-secondary">Last updated: June 2026</p>
