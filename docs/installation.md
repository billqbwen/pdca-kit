# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows; PowerShell scripts now supported without WSL)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Codebuddy CLI](https://www.codebuddy.ai/cli), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or [Pi Coding Agent](https://pi.dev)
- [uv](https://docs.astral.sh/uv/) for package management (recommended) or [pipx](https://pipx.pypa.io/) for persistent installation
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

> [!IMPORTANT]
> The only official, maintained packages for PDCA Kit come from the [github/pdca-kit](https://github.com/github/pdca-kit) GitHub repository. Any packages with the same name available on PyPI (e.g. `pdca-cli` on pypi.org) are **not** affiliated with this project and are not maintained by the PDCA Kit maintainers. For normal installs, use the GitHub-based commands shown below. For offline or air-gapped environments, locally built wheels created from this repository are also valid.

### Persistent Installation (Recommended)

Install once and use everywhere. Replace `vX.Y.Z` with a tag from [Releases](https://github.com/github/pdca-kit/releases):

> [!NOTE]
> The command below requires **[uv](https://docs.astral.sh/uv/)**. If you see `command not found: uv`, [install uv first](./install/uv.md).

```bash
uv tool install pdca-cli --from git+https://github.com/github/pdca-kit.git@vX.Y.Z
```

Then initialize a project:

```bash
pdca init <PROJECT_NAME> --integration copilot
```

### One-time Usage

Run directly without installing — see the [One-time usage (uvx)](install/one-time.md) guide.

### Alternative Package Managers

- **pipx** — see the [pipx installation guide](install/pipx.md)
- **Enterprise / Air-Gapped** — see the [air-gapped installation guide](install/air-gapped.md)

### Integration Selection

Interactive terminals prompt you to choose a coding agent integration during initialization. Non-interactive sessions, such as CI or piped runs, default to GitHub Copilot unless you pass `--integration`.

You can proactively specify your coding agent integration during initialization:

```bash
pdca init <project_name> --integration claude
pdca init <project_name> --integration gemini
pdca init <project_name> --integration copilot
pdca init <project_name> --integration codebuddy
pdca init <project_name> --integration pi
```

### Specify Script Type (Shell vs PowerShell)

All automation scripts now have both Bash (`.sh`) and PowerShell (`.ps1`) variants.

Auto behavior:

- Windows default: `ps`
- Other OS default: `sh`
- Interactive mode: you'll be prompted unless you pass `--script`

Force a specific script type:

```bash
pdca init <project_name> --script sh
pdca init <project_name> --script ps
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
pdca init <project_name> --integration claude --ignore-agent-tools
```

## Verification

After installation, run the following command to confirm the correct version is installed:

```bash
pdca version
```

This helps verify you are running the official PDCA Kit build from GitHub, not an unrelated package with the same name.

After initialization, you should see the following commands available in your coding agent:

- `/pdca.define` - Create specifications
- `/pdca.plan` - Generate implementation plans  
- `/pdca.tasks` - Break down into actionable tasks

Scripts are installed into a variant subdirectory matching the chosen script type:

- `.pdca/scripts/bash/` — contains `.sh` scripts (default on Linux/macOS)
- `.pdca/scripts/powershell/` — contains `.ps1` scripts (default on Windows)

## Troubleshooting

### Enterprise / Air-Gapped Installation

If your environment blocks access to PyPI or GitHub, see the [Enterprise / Air-Gapped Installation](install/air-gapped.md) guide for step-by-step instructions on creating portable wheel bundles.

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, see the [Air-Gapped Installation guide](install/air-gapped.md#git-credential-manager-on-linux) for Git Credential Manager setup instructions.
