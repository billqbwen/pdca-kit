# Upgrade Guide

> You have PDCA Kit installed and want to upgrade to the latest version to get new features, bug fixes, or updated slash commands. This guide covers both upgrading the CLI tool and updating your project files.

---

## Quick Reference

| What to Upgrade | Command | When to Use |
|----------------|---------|-------------|
| **CLI Tool Only** | `uv tool install pdca-cli --force --from git+https://github.com/github/pdca-kit.git@vX.Y.Z` | Get latest CLI features without touching project files |
| **CLI Tool Only (pipx)** | `pipx install --force git+https://github.com/github/pdca-kit.git@vX.Y.Z` | Reinstall/upgrade a pipx-installed CLI to a specific release |
| **Project Files** | `pdca init --here --force --integration <your-agent>` | Update slash commands, templates, and scripts in your project |
| **Both** | Run CLI upgrade, then project update | Recommended for major version updates |

---

## Part 1: Upgrade the CLI Tool

The CLI tool (`specify`) is separate from your project files. Upgrade it to get the latest features and bug fixes.

Before upgrading, you can check whether a newer released version is available:

```bash
specify self check
```

### If you installed with `uv tool install`

Upgrade to a specific release (check [Releases](https://github.com/github/pdca-kit/releases) for the latest tag):

```bash
uv tool install pdca-cli --force --from git+https://github.com/github/pdca-kit.git@vX.Y.Z
```

### If you use one-shot `uvx` commands

Specify the desired release tag:

```bash
uvx --from git+https://github.com/github/pdca-kit.git@vX.Y.Z pdca init --here --integration copilot
```

`uvx` runs a temporary copy of PDCA Kit for that single command. It does not update a persistent `specify` installed with `uv tool install`, `pipx`, or another tool manager. If a newer feature works through `uvx` but your local `specify` still reports an older version, upgrade the persistent CLI with the command that matches your install method.

### If you installed with `pipx`

Upgrade to a specific release:

```bash
pipx install --force git+https://github.com/github/pdca-kit.git@vX.Y.Z
```

### Verify the upgrade

```bash
pdca check
```

This shows installed tools and confirms the CLI is working. Use `pdca version` to confirm which persistent CLI version is currently on your `PATH`.

---

## Part 2: Updating Project Files

When PDCA Kit releases new features (like new slash commands or updated templates), you need to refresh your project's PDCA Kit files.

### What gets updated?

Running `pdca init --here --force` will update:

- ✅ **Slash command files** (`.claude/commands/`, `.github/prompts/`, etc.)
- ✅ **Script files** (`.pdca/scripts/`) — **only with `--force`**; without it, only missing files are added
- ✅ **Template files** (`.pdca/templates/`) — **only with `--force`**; without it, only missing files are added
- ✅ **Shared memory files** (`.pdca/memory/`) - **⚠️ See warnings below**

### What stays safe?

These files are **never touched** by the upgrade—the template packages don't even contain them:

- ✅ **Your specifications** (`specs/001-my-feature/spec.md`, etc.) - **CONFIRMED SAFE**
- ✅ **Your implementation plans** (`specs/001-my-feature/plan.md`, `tasks.md`, etc.) - **CONFIRMED SAFE**
- ✅ **Your source code** - **CONFIRMED SAFE**
- ✅ **Your git history** - **CONFIRMED SAFE**

The `specs/` directory is completely excluded from template packages and will never be modified during upgrades.

### Update command

Run this inside your project directory:

```bash
pdca init --here --force --integration <your-agent>
```

Replace `<your-agent>` with your AI coding agent. Refer to this list of [Supported AI Coding Agent Integrations](reference/integrations.md)

**Example:**

```bash
pdca init --here --force --integration copilot
```

### Understanding the `--force` flag

Without `--force`, the CLI warns you and asks for confirmation:

```text
Warning: Current directory is not empty (25 items)
Template files will be merged with existing content and may overwrite existing files
Proceed? [y/N]
```

With `--force`, it skips the confirmation and proceeds immediately. It also **overwrites shared infrastructure files** (`.pdca/scripts/` and `.pdca/templates/`) with the latest versions from the installed PDCA Kit release.

Without `--force`, shared infrastructure files that already exist are skipped — the CLI will print a warning listing the skipped files so you know which ones were not updated.

**Important: Your `specs/` directory is always safe.** The `--force` flag only affects template files (commands, scripts, templates, memory). Your feature specifications, plans, and tasks in `specs/` are never included in upgrade packages and cannot be overwritten.

---

## ⚠️ Important Warnings

### 1. Constitution file will be overwritten

**Known issue:** `pdca init --here --force` currently overwrites `.pdca/memory/constitution.md` with the default template, erasing any customizations you made.

**Workaround:**

```bash
# 1. Back up your constitution before upgrading
cp .pdca/memory/constitution.md .pdca/memory/constitution-backup.md

# 2. Run the upgrade
pdca init --here --force --integration copilot

# 3. Restore your customized constitution
mv .pdca/memory/constitution-backup.md .pdca/memory/constitution.md
```

Or use git to restore it:

```bash
# After upgrade, restore from git history
git restore .pdca/memory/constitution.md
```

### 2. Custom script or template modifications

If you customized files in `.pdca/scripts/` or `.pdca/templates/`, the `--force` flag will overwrite them. Back them up first:

```bash
# Back up custom templates and scripts
cp -r .pdca/templates .pdca/templates-backup
cp -r .pdca/scripts .pdca/scripts-backup

# After upgrade, merge your changes back manually
```

### 3. Duplicate slash commands (IDE-based agents)

Some IDE-based agents (like Kilo Code, Windsurf) may show **duplicate slash commands** after upgrading—both old and new versions appear.

**Solution:** Manually delete the old command files from your agent's folder.

**Example for Kilo Code:**

```bash
# Navigate to the agent's commands folder
cd .kilocode/rules/

# List files and identify duplicates
ls -la

# Delete old versions (example filenames - yours may differ)
rm pdca.define-old.md
rm pdca.plan-v1.md
```

Restart your IDE to refresh the command list.

---

## Common Scenarios

### Scenario 1: "I just want new slash commands"

```bash
# Upgrade CLI (if using persistent install)
uv tool install pdca-cli --force --from git+https://github.com/github/pdca-kit.git

# Update project files to get new commands
pdca init --here --force --integration copilot

# Restore your constitution if customized
git restore .pdca/memory/constitution.md
```

### Scenario 2: "I customized templates and constitution"

```bash
# 1. Back up customizations
cp .pdca/memory/constitution.md /tmp/constitution-backup.md
cp -r .pdca/templates /tmp/templates-backup

# 2. Upgrade CLI
uv tool install pdca-cli --force --from git+https://github.com/github/pdca-kit.git

# 3. Update project
pdca init --here --force --integration copilot

# 4. Restore customizations
mv /tmp/constitution-backup.md .pdca/memory/constitution.md
# Manually merge template changes if needed
```

### Scenario 3: "I see duplicate slash commands in my IDE"

This happens with IDE-based agents (Kilo Code, Windsurf, Roo Code, etc.).

```bash
# Find the agent folder (example: .kilocode/rules/)
cd .kilocode/rules/

# List all files
ls -la

# Delete old command files
rm pdca.old-command-name.md

# Restart your IDE
```

### Scenario 4: "I'm working on a project without Git"

If you initialized your project with `--no-git`, you can still upgrade:

```bash
# Manually back up files you customized
cp .pdca/memory/constitution.md /tmp/constitution-backup.md

# Run upgrade
pdca init --here --force --integration copilot --no-git

# Restore customizations
mv /tmp/constitution-backup.md .pdca/memory/constitution.md
```

The `--no-git` flag skips git initialization but doesn't affect file updates.

---

## Using `--no-git` Flag

The `--no-git` flag tells PDCA Kit to **skip git repository initialization**. This is useful when:

- You manage version control differently (Mercurial, SVN, etc.)
- Your project is part of a larger monorepo with existing git setup
- You're experimenting and don't want version control yet

**During initial setup:**

```bash
pdca init my-project --integration copilot --no-git
```

**During upgrade:**

```bash
pdca init --here --force --integration copilot --no-git
```

### What `--no-git` does NOT do

❌ Does NOT prevent file updates
❌ Does NOT skip slash command installation
❌ Does NOT affect template merging

It **only** skips running `git init` and creating the initial commit.

### Working without Git

If you use `--no-git`, you'll need to manage feature directories manually:

**Set the `PDCA_FEATURE` environment variable** before using planning commands:

```bash
# Bash/Zsh
export PDCA_FEATURE="001-my-feature"

# PowerShell
$env:PDCA_FEATURE = "001-my-feature"
```

This tells PDCA Kit which feature directory to use when creating specs, plans, and tasks.

**Why this matters:** Without git, PDCA Kit can't detect your current branch name to determine the active feature. The environment variable provides that context manually.

---

## Troubleshooting

### "Slash commands not showing up after upgrade"

**Cause:** Agent didn't reload the command files.

**Fix:**

1. **Restart your IDE/editor** completely (not just reload window)
2. **For CLI-based agents**, verify files exist:

   ```bash
   ls -la .claude/commands/      # Claude Code
   ls -la .gemini/commands/      # Gemini
   ls -la .cursor/skills/      # Cursor
   ls -la .pi/prompts/           # Pi Coding Agent
   ```

3. **Check agent-specific setup:**
   - Codex requires `CODEX_HOME` environment variable
   - Some agents need workspace restart or cache clearing

### "I lost my constitution customizations"

**Fix:** Restore from git or backup:

```bash
# If you committed before upgrading
git restore .pdca/memory/constitution.md

# If you backed up manually
cp /tmp/constitution-backup.md .pdca/memory/constitution.md
```

**Prevention:** Always commit or back up `constitution.md` before upgrading.

### "Warning: Current directory is not empty"

**Full warning message:**

```text
Warning: Current directory is not empty (25 items)
Template files will be merged with existing content and may overwrite existing files
Do you want to continue? [y/N]
```

**What this means:**

This warning appears when you run `pdca init --here` (or `pdca init .`) in a directory that already has files. It's telling you:

1. **The directory has existing content** - In the example, 25 files/folders
2. **Files will be merged** - New template files will be added alongside your existing files
3. **Some files may be overwritten** - If you already have PDCA Kit files (`.claude/`, `.pdca/`, etc.), they'll be replaced with the new versions

**What gets overwritten:**

Only PDCA Kit infrastructure files:

- Agent command files (`.claude/commands/`, `.github/prompts/`, etc.)
- Scripts in `.pdca/scripts/`
- Templates in `.pdca/templates/`
- Memory files in `.pdca/memory/` (including constitution)

**What stays untouched:**

- Your `specs/` directory (specifications, plans, tasks)
- Your source code files
- Your `.git/` directory and git history
- Any other files not part of PDCA Kit templates

**How to respond:**

- **Type `y` and press Enter** - Proceed with the merge (recommended if upgrading)
- **Type `n` and press Enter** - Cancel the operation
- **Use `--force` flag** - Skip this confirmation entirely:

  ```bash
  pdca init --here --force --integration copilot
  ```

**When you see this warning:**

- ✅ **Expected** when upgrading an existing PDCA Kit project
- ✅ **Expected** when adding PDCA Kit to an existing codebase
- ⚠️ **Unexpected** if you thought you were creating a new project in an empty directory

**Prevention tip:** Before upgrading, commit or back up your `.pdca/memory/constitution.md` if you customized it.

### "CLI upgrade doesn't seem to work"

If a command behaves like an older PDCA Kit version, first check for local CLI drift:

```bash
specify self check
```

`pdca check` is an offline environment scan; `specify self check` is the CLI version lookup.

Verify the installation:

```bash
# Check installed tools
uv tool list

# Should show pdca-cli

# Verify path
which specify

# Should point to the uv tool installation directory
```

If not found, reinstall:

```bash
uv tool uninstall pdca-cli
uv tool install pdca-cli --from git+https://github.com/github/pdca-kit.git
```

### "Do I need to run specify every time I open my project?"

**Short answer:** No, you only run `pdca init` once per project (or when upgrading).

**Explanation:**

The `specify` CLI tool is used for:

- **Initial setup:** `pdca init` to bootstrap PDCA Kit in your project
- **Upgrades:** `pdca init --here --force` to update templates and commands
- **Diagnostics:** `pdca check` to verify tool installation

Once you've run `pdca init`, the slash commands (like `/pdca.define`, `/pdca.plan`, etc.) are **permanently installed** in your project's agent folder (`.claude/`, `.github/prompts/`, `.pi/prompts/`, etc.). Your AI coding agent reads these command files directly—no need to run `specify` again.

**If your agent isn't recognizing slash commands:**

1. **Verify command files exist:**

   ```bash
   # For GitHub Copilot
   ls -la .github/prompts/

   # For Claude
   ls -la .claude/commands/

   # For Pi
   ls -la .pi/prompts/
   ```

2. **Restart your IDE/editor completely** (not just reload window)

3. **Check you're in the correct directory** where you ran `pdca init`

4. **For some agents**, you may need to reload the workspace or clear cache

**Related issue:** If Copilot can't open local files or uses PowerShell commands unexpectedly, this is typically an IDE context issue, not related to `specify`. Try:

- Restarting VS Code
- Checking file permissions
- Ensuring the workspace folder is properly opened

---

## Version Compatibility

PDCA Kit follows semantic versioning for major releases. The CLI and project files are designed to be compatible within the same major version.

**Best practice:** Keep both CLI and project files in sync by upgrading both together during major version changes.

---

## Next Steps

After upgrading:

- **Test new slash commands:** Run `/pdca.constitution` or another command to verify everything works
- **Review release notes:** Check [GitHub Releases](https://github.com/github/pdca-kit/releases) for new features and breaking changes
- **Update workflows:** If new commands were added, update your team's development workflows
- **Check documentation:** Visit [github.io/pdca-kit](https://github.github.io/pdca-kit/) for updated guides
