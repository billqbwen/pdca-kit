# Presets

Presets are stackable, priority-ordered collections of template and command overrides for PDCA Kit. They let you customize both the artifacts produced by the Spec-Driven Development workflow (specs, plans, tasks, checklists, constitutions) and the commands that guide the LLM in creating them — without forking or modifying core files.

## How It Works

When PDCA Kit needs a template (e.g. `spec-template`), it walks a resolution stack:

1. `.pdca/templates/overrides/` — project-local one-off overrides
2. `.pdca/presets/<preset-id>/templates/` — installed presets (sorted by priority)
3. `.pdca/extensions/<ext-id>/templates/` — extension-provided templates
4. `.pdca/templates/` — core templates shipped with PDCA Kit

If no preset is installed, core templates are used — exactly the same behavior as before presets existed.

Template resolution happens **at runtime** — although preset files are copied into `.pdca/presets/<id>/` during installation, PDCA Kit walks the resolution stack on every template lookup rather than merging templates into a single location.

For detailed resolution and command registration flows, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Command Overrides

Presets can also override the commands that guide the SDD workflow. Templates define *what* gets produced (specs, plans, constitutions); commands define *how* the LLM produces them (the step-by-step instructions).

Unlike templates, command overrides are applied **at install time**. When a preset includes `type: "command"` entries, the commands are registered into all detected agent directories (`.claude/commands/`, `.gemini/commands/`, etc.) in the correct format (Markdown or TOML with appropriate argument placeholders). When the preset is removed, the registered commands are cleaned up.

## Quick Start

```bash
# Search available presets
pdca preset search

# Install a preset from the catalog
pdca preset add healthcare-compliance

# Install from a local directory (for development)
pdca preset add --dev ./my-preset

# Install with a specific priority (lower = higher precedence)
pdca preset add healthcare-compliance --priority 5

# List installed presets
pdca preset list

# See which template a name resolves to
pdca preset resolve spec-template

# Get detailed info about a preset
pdca preset info healthcare-compliance

# Remove a preset
pdca preset remove healthcare-compliance
```

## Stacking Presets

Multiple presets can be installed simultaneously. The `--priority` flag controls which one wins when two presets provide the same template (lower number = higher precedence):

```bash
pdca preset add enterprise-safe --priority 10      # base layer
pdca preset add healthcare-compliance --priority 5  # overrides enterprise-safe
pdca preset add pm-workflow --priority 1            # overrides everything
```

Presets **override by default**, they don't merge. If two presets both provide `spec-template` with the default `replace` strategy, the one with the lowest priority number wins entirely. However, presets can use **composition strategies** to augment rather than replace content.

### Composition Strategies

Presets can declare a `strategy` per template to control how content is combined. The `name` field identifies which template to compose with in the priority stack, while `file` points to the actual content file (which can differ from the convention path `templates/<name>.md`):

```yaml
provides:
  templates:
    - type: "template"
      name: "spec-template"
      file: "templates/spec-addendum.md"
      strategy: "append"        # adds content after the core template
```

| Strategy | Description |
|----------|-------------|
| `replace` (default) | Fully replaces the lower-priority template |
| `prepend` | Places content **before** the resolved lower-priority template, separated by a blank line |
| `append` | Places content **after** the resolved lower-priority template, separated by a blank line |
| `wrap` | Content contains `{CORE_TEMPLATE}` placeholder (or `$CORE_SCRIPT` for scripts) replaced with the lower-priority content |

**Supported combinations:**

| Type | `replace` | `prepend` | `append` | `wrap` |
|------|-----------|-----------|----------|--------|
| **template** | ✓ (default) | ✓ | ✓ | ✓ |
| **command** | ✓ (default) | ✓ | ✓ | ✓ |
| **script** | ✓ (default) | — | — | ✓ |

Multiple composing presets chain recursively. For example, a security preset with `prepend` and a compliance preset with `append` will produce: security header + core content + compliance footer.

## Catalog Management

Presets are discovered through catalogs. By default, PDCA Kit uses the official and community catalogs:

> [!NOTE]
> Community presets are independently created and maintained by their respective authors. Maintainers only verify that catalog entries are complete and correctly formatted — they do **not review, audit, endorse, or support the preset code itself**. Review preset source code before installation and use at your own discretion.

```bash
# List active catalogs
pdca preset catalog list

# Add a custom catalog
pdca preset catalog add https://example.com/catalog.json --name my-org --install-allowed

# Remove a catalog
pdca preset catalog remove my-org
```

## Creating a Preset

See [scaffold/](scaffold/) for a scaffold you can copy to create your own preset.

1. Copy `scaffold/` to a new directory
2. Edit `preset.yml` with your preset's metadata
3. Add or replace templates in `templates/`
4. Test locally with `pdca preset add --dev .`
5. Verify with `pdca preset resolve spec-template`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PDCA_PRESET_CATALOG_URL` | Override the full catalog stack with a single URL (replaces all defaults) | Built-in default stack |
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub token for authenticated requests to GitHub-hosted URLs (`raw.githubusercontent.com`, `github.com`, `api.github.com`, `codeload.github.com`). Required when your catalog JSON or preset ZIPs are hosted in a private GitHub repository. | None |

#### Example: Using a private GitHub-hosted catalog

```bash
# Authenticate with a token (gh CLI, PAT, or GITHUB_TOKEN in CI)
export GITHUB_TOKEN=$(gh auth token)

# Search a private catalog added via `pdca preset catalog add`
pdca preset search my-template

# Install from a private catalog
pdca preset add my-template
```

The token is attached automatically to requests targeting GitHub domains. Non-GitHub catalog URLs are always fetched without credentials.

## Configuration Files

| File | Scope | Description |
|------|-------|-------------|
| `.pdca/preset-catalogs.yml` | Project | Custom catalog stack for this project |
| `~/.pdca/preset-catalogs.yml` | User | Custom catalog stack for all projects |

## Future Considerations

The following enhancements are under consideration for future releases:

- **Structural merge strategies** — Parsing Markdown sections for per-section granularity (e.g., "replace only ## Security").
- **Conflict detection** — `pdca preset lint` / `pdca preset doctor` for detecting composition conflicts.
