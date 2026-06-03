# Extensions

Extensions add new capabilities to PDCA Kit — domain-specific commands, external tool integrations, quality gates, and more. They introduce new commands and templates that go beyond the built-in Spec-Driven Development workflow.

## Search Available Extensions

```bash
pdca extension search [query]
```

| Option       | Description                          |
| ------------ | ------------------------------------ |
| `--tag`      | Filter by tag                        |
| `--author`   | Filter by author                     |
| `--verified` | Show only verified extensions        |

Searches all active catalogs for extensions matching the query. Without a query, lists all available extensions.

## Install an Extension

```bash
pdca extension add <name>
```

| Option          | Description                                              |
| --------------- | -------------------------------------------------------- |
| `--dev`         | Install from a local directory (for development)         |
| `--from <url>`  | Install from a custom URL instead of the catalog         |
| `--priority <N>`| Resolution priority (default: 10; lower = higher precedence) |

Installs an extension from the catalog, a URL, or a local directory. Extension commands are automatically registered with the currently installed AI coding agent integration.

> **Note:** All extension commands require a project already initialized with `pdca init`.

## Remove an Extension

```bash
pdca extension remove <name>
```

| Option          | Description                                    |
| --------------- | ---------------------------------------------- |
| `--keep-config` | Preserve configuration files during removal    |
| `--force`       | Skip confirmation prompt                       |

Removes an installed extension. Configuration files are backed up by default; use `--keep-config` to leave them in place or `--force` to skip the confirmation.

## List Installed Extensions

```bash
pdca extension list
```

| Option        | Description                                        |
| ------------- | -------------------------------------------------- |
| `--available` | Show available (uninstalled) extensions            |
| `--all`       | Show both installed and available extensions       |

Lists installed extensions with their status, version, and command counts.

## Extension Info

```bash
pdca extension info <name>
```

Shows detailed information about an installed or available extension, including its description, version, commands, and configuration.

## Update Extensions

```bash
pdca extension update [<name>]
```

Updates a specific extension, or all installed extensions if no name is given.

## Enable / Disable an Extension

```bash
pdca extension enable <name>
pdca extension disable <name>
```

Disable an extension without removing it. Disabled extensions are not loaded and their commands are not available. Re-enable with `enable`.

## Set Extension Priority

```bash
pdca extension set-priority <name> <priority>
```

Changes the resolution priority of an extension. When multiple extensions provide a command with the same name, the extension with the lowest priority number takes precedence.

## Catalog Management

Extension catalogs control where `search` and `add` look for extensions. Catalogs are checked in priority order (lower number = higher precedence).

### List Catalogs

```bash
pdca extension catalog list
```

Shows all active catalogs in the stack with their priorities and install permissions.

### Add a Catalog

```bash
pdca extension catalog add <url>
```

| Option                               | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `--name <name>`                      | Required. Unique name for the catalog              |
| `--priority <N>`                     | Priority (default: 10; lower = higher precedence)  |
| `--install-allowed / --no-install-allowed` | Whether extensions can be installed from this catalog |
| `--description <text>`               | Optional description                               |

Adds a catalog to the project's `.pdca/extension-catalogs.yml`.

### Remove a Catalog

```bash
pdca extension catalog remove <name>
```

Removes a catalog from the project configuration.

### Catalog Resolution Order

Catalogs are resolved in this order (first match wins):

1. **Environment variable** — `PDCA_CATALOG_URL` overrides all catalogs
2. **Project config** — `.pdca/extension-catalogs.yml`
3. **User config** — `~/.pdca/extension-catalogs.yml`
4. **Built-in defaults** — official catalog + community catalog

Example `.pdca/extension-catalogs.yml`:

```yaml
catalogs:
  - name: "my-org-catalog"
    url: "https://example.com/catalog.json"
    priority: 5
    install_allowed: true
    description: "Our approved extensions"
```

## Extension Configuration

Most extensions include configuration files in their install directory:

```text
.pdca/extensions/<ext>/
├── <ext>-config.yml           # Project config (version controlled)
├── <ext>-config.local.yml     # Local overrides (gitignored)
└── <ext>-config.template.yml  # Template reference
```

Configuration is merged in this order (highest priority last):

1. **Extension defaults** (from `extension.yml`)
2. **Project config** (`<ext>-config.yml`)
3. **Local overrides** (`<ext>-config.local.yml`)
4. **Environment variables** (`PDCA_<EXT>_*`)

To set up configuration for a newly installed extension, copy the template:

```bash
cp .pdca/extensions/<ext>/<ext>-config.template.yml \
   .pdca/extensions/<ext>/<ext>-config.yml
```

## FAQ

### Why can't I find an extension with `search`?

Check the spelling of the extension name. The extension may not be published yet, or it may be in a catalog you haven't added. Use `pdca extension catalog list` to see which catalogs are active.

### Why doesn't the extension command appear in my AI coding agent?

Verify the extension is installed and enabled with `pdca extension list`. If it shows as installed, restart your AI coding agent — it may need to reload for it to take effect.

### How do I set up extension configuration?

Copy the config template that ships with the extension:

```bash
cp .pdca/extensions/<ext>/<ext>-config.template.yml \
   .pdca/extensions/<ext>/<ext>-config.yml
```

See [Extension Configuration](#extension-configuration) for details on config layers and overrides.

### How do I resolve an incompatible version error?

Update PDCA Kit to the version required by the extension.

### Who maintains extensions?

Most extensions are independently created and maintained by their respective authors. The PDCA Kit maintainers do not review, audit, endorse, or support extension code. Review an extension's source code before installing and use at your own discretion. For issues with a specific extension, contact its author or file an issue on the extension's repository.
