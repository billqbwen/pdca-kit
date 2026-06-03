# Installing with pipx

[pipx](https://pipx.pypa.io/) is a tool for installing Python CLI applications in isolated environments. It does not require [uv](https://docs.astral.sh/uv/).

## Install PDCA CLI

Pin a specific release tag for stability (check [Releases](https://github.com/github/pdca-kit/releases) for the latest):

```bash
# Install a specific stable release (recommended — replace vX.Y.Z with the latest tag)
pipx install git+https://github.com/github/pdca-kit.git@vX.Y.Z

# Or install latest from main (may include unreleased changes)
pipx install git+https://github.com/github/pdca-kit.git
```

## Verify

```bash
pdca version
```

## Upgrade

```bash
pipx install --force git+https://github.com/github/pdca-kit.git@vX.Y.Z
```

## Uninstall

```bash
pipx uninstall pdca-cli
```

## Next steps

Head to the [Quick Start](../quickstart.md) to initialize your first project.
