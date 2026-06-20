# Development Notes

PDCA Kit is a toolkit for spec-driven development. At its core, it is a coordinated set of prompts, templates, scripts, and CLI/integration assets that define and deliver a spec-driven workflow for AI coding agents. This document is a starting point for people modifying PDCA Kit itself, with a compact orientation to the key project documents and repository organization.

**Essential project documents:**

| Document                                                   | Role                                                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [README.md](README.md)                                     | Primary user-facing overview of PDCA Kit and its workflow.                            |
| [DEVELOPMENT.md](DEVELOPMENT.md)                           | This document.                                                                        |
| [spec-driven.md](spec-driven.md)                           | End-to-end explanation of the Spec-Driven Development workflow supported by PDCA Kit. |
| [RELEASE-PROCESS.md](.github/workflows/RELEASE-PROCESS.md) | Release workflow, versioning rules, and changelog generation process.                 |
| [docs/index.md](docs/index.md)                             | Entry point to the `docs/` documentation set.                                         |
| [CONTRIBUTING.md](CONTRIBUTING.md)                         | Contribution process, review expectations, testing, and required development practices. |
| [AGENTS.md](AGENTS.md)                                     | Integration architecture guide — how to add or modify AI agent integrations.          |
| [EXTENSION-API-REFERENCE.md](extensions/EXTENSION-API-REFERENCE.md) | Technical reference for the extension system manifest schema, hooks, and CLI commands. |

**Main repository components:**

| Directory          | Role                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `templates/`       | Prompt assets and templates that define the core workflow behavior and generated artifacts. |
| `scripts/`         | Supporting scripts used by the workflow, setup, and repository tooling.                     |
| `src/pdca_cli/` | Python source for the `pdca` CLI, including agent-specific assets.                       |
| `extensions/`      | Extension catalogs, manifests, and example/template extensions.                            |
| `presets/`         | Preset catalogs and supporting assets.                                                      |

## Development Quick Start

### Setup

```bash
uv sync --extra test
```

### Running Tests

```bash
# Full test suite
uv run pytest

# Specific test file
uv run pytest tests/test_workflow_engine.py -v

# Integration tests for a specific agent
uv run pytest tests/integrations/test_integration_claude.py -v

# With coverage
uv run pytest --cov=src/pdca_cli
```

### Linting

```bash
uvx ruff check src/ tests/
uvx ruff format --check src/ tests/
```

### Key Source Layout

| Source path | Purpose |
|---|---|
| `src/pdca_cli/__init__.py` | CLI entry point — Typer commands for init, integration, extension, preset management |
| `src/pdca_cli/workflows/` | Workflow engine, step types (command, shell, prompt, gate, if, switch, fan), expression evaluator |
| `src/pdca_cli/integrations/` | AI agent integration subpackages (33 agents) and registry |
| `src/pdca_cli/extensions.py` | Extension lifecycle management — discovery, install, upgrade, uninstall |
| `src/pdca_cli/presets.py` | Preset management — install, list, remove |
| `src/pdca_cli/shared_infra.py` | Shared infrastructure (templates, scripts) installation with safety checks |
| `src/pdca_cli/integrations/base.py` | Integration base classes — IntegrationBase, MarkdownIntegration, TomlIntegration, etc. |
| `src/pdca_cli/integrations/manifest.py` | File tracking via SHA-256 manifest, modified-file detection |
