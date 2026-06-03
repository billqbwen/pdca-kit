# Lean Workflow

A minimal preset that strips the PDCA Kit workflow down to its essentials — just the prompt, just the artifact.

## When to Use

Use Lean when you want the structured specify → plan → tasks → implement pipeline without the ceremony of the full templates. Each command produces a single focused Markdown file with no boilerplate sections to fill in.

## Commands Included

| Command | Output | Description |
|---------|--------|-------------|
| `pdca.define` | `spec.md` | Create a specification from a feature description |
| `pdca.plan` | `plan.md` | Create an implementation plan from the spec |
| `pdca.tasks` | `tasks.md` | Create dependency-ordered tasks from spec and plan |
| `pdca.implement` | *(code)* | Execute all tasks in order, marking progress |
| `pdca.constitution` | `constitution.md` | Create or update the project constitution |

## What It Replaces

Lean overrides the five core workflow commands with self-contained prompts that produce each artifact directly — no separate template files involved. The result is a shorter, more direct workflow.

## Installation

```bash
# Lean is a bundled preset — no download needed
pdca preset add lean
```

## Development

```bash
# Test from local directory
pdca preset add --dev ./presets/lean

# Verify commands resolve
pdca preset resolve pdca.define

# Remove when done
pdca preset remove lean
```

## License

MIT
