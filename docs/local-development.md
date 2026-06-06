# Local Development Guide

This guide shows how to iterate on the `pdca` CLI locally without publishing a release or committing to `main` first.

> Scripts now have both Bash (`.sh`) and PowerShell (`.ps1`) variants. The CLI auto-selects based on OS unless you pass `--script sh|ps`.

## 1. Clone and Switch Branches

```bash
git clone https://github.com/github/pdca-kit.git
cd pdca-kit
# Work on a feature branch
git checkout -b your-feature-branch
```

## 2. Run the CLI Directly (Fastest Feedback)

You can execute the CLI via the module entrypoint without installing anything:

```bash
# From repo root
python -m src.pdca_cli --help
python -m src.pdca_cli init demo-project --integration claude --ignore-agent-tools --script sh
```

If you prefer invoking the script file style (uses shebang):

```bash
python src/pdca_cli/__init__.py init demo-project --script ps
```

## 3. Use Editable Install (Isolated Environment)

Create an isolated environment using `uv` so dependencies resolve exactly like end users get them:

```bash
# Create & activate virtual env (uv auto-manages .venv)
uv venv
source .venv/bin/activate  # or on Windows PowerShell: .venv\Scripts\Activate.ps1

# Install project in editable mode
uv pip install -e .

# Now 'pdca' entrypoint is available
pdca --help
```

Re-running after code edits requires no reinstall because of editable mode.

## 4. Invoke with uvx Directly From Git (Current Branch)

`uvx` can run from a local path (or a Git ref) to simulate user flows:

```bash
uvx --from . pdca init demo-uvx --integration copilot --ignore-agent-tools --script sh
```

You can also point uvx at a specific branch without merging:

```bash
# Push your working branch first
git push origin your-feature-branch
uvx --from git+https://github.com/github/pdca-kit.git@your-feature-branch pdca init demo-branch-test --script ps
```

### 4a. Absolute Path uvx (Run From Anywhere)

If you're in another directory, use an absolute path instead of `.`:

```bash
uvx --from /mnt/c/GitHub/pdca-kit pdca --help
uvx --from /mnt/c/GitHub/pdca-kit pdca init demo-anywhere --integration copilot --ignore-agent-tools --script sh
```

Set an environment variable for convenience:

```bash
export SPEC_KIT_SRC=/mnt/c/GitHub/pdca-kit
uvx --from "$SPEC_KIT_SRC" pdca init demo-env --integration copilot --ignore-agent-tools --script ps
```

(Optional) Define a shell function:

```bash
pdca-dev() { uvx --from /mnt/c/GitHub/pdca-kit pdca "$@"; }
# Then
pdca-dev --help
```

## 5. Testing Script Permission Logic

After running an `init`, check that shell scripts are executable on POSIX systems:

```bash
ls -l scripts | grep .sh
# Expect owner execute bit (e.g. -rwxr-xr-x)
```

On Windows you will instead use the `.ps1` scripts (no chmod needed).

## 6. Run Lint / Basic Checks (Add Your Own)

Currently no enforced lint config is bundled, but you can quickly sanity check importability:

```bash
python -c "import pdca_cli; print('Import OK')"
```

## 7. Build a Wheel Locally (Optional)

Validate packaging before publishing:

```bash
uv build
ls dist/
```

Install the built artifact into a fresh throwaway environment if needed.

## 8. Using a Temporary Workspace

When testing `init --here` in a dirty directory, create a temp workspace:

```bash
mkdir /tmp/spec-test && cd /tmp/spec-test
python -m src.pdca_cli init --here --integration claude --ignore-agent-tools --script sh  # if repo copied here
```

Or copy only the modified CLI portion if you want a lighter sandbox.

## 9. Debug Network / TLS Issues

> **Deprecated:** The `--skip-tls` flag is a no-op and has no effect.
> It was previously used to bypass TLS validation during local testing.
> If you encounter TLS errors (e.g., on a corporate network), configure your
> environment's certificate store or proxy instead.
>
> For example, set `SSL_CERT_FILE` or configure `HTTPS_PROXY` / `HTTP_PROXY`.

## 10. Rapid Edit Loop Summary

| Action | Command |
|--------|---------|
| Run CLI directly | `python -m src.pdca_cli --help` |
| Editable install | `uv pip install -e .` then `pdca ...` |
| Local uvx run (repo root) | `uvx --from . pdca ...` |
| Local uvx run (abs path) | `uvx --from /mnt/c/GitHub/pdca-kit pdca ...` |
| Git branch uvx | `uvx --from git+URL@branch pdca ...` |
| Build wheel | `uv build` |

## 11. Cleaning Up

Remove build artifacts / virtual env quickly:

```bash
rm -rf .venv dist build *.egg-info
```

## 12. Common Issues

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: typer` | Run `uv pip install -e .` |
| Scripts not executable (Linux) | Re-run init or `chmod +x scripts/*.sh` |
| Git step skipped | You passed `--no-git` or Git not installed |
| Wrong script type downloaded | Pass `--script sh` or `--script ps` explicitly |
| TLS errors on corporate network | Configure your environment's certificate store or proxy. The `--skip-tls` flag is deprecated and has no effect. |

## 13. Next Steps

- Update docs and run through Quick Start using your modified CLI
- Open a PR when satisfied
- (Optional) Tag a release once changes land in `main`
