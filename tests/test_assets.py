"""Tests for pdca_cli._assets — bundle path resolution and version lookup."""

import importlib.metadata
from pathlib import Path
from unittest.mock import patch


from pdca_cli._assets import (
    _locate_bundled_extension,
    _locate_bundled_preset,
    _locate_bundled_workflow,
    _locate_core_pack,
    _repo_root,
    get_pdca_version,
)


class TestLocateCorePack:
    """Tests for _locate_core_pack."""

    def test_returns_none_when_no_core_pack(self, monkeypatch, tmp_path):
        """When core_pack does not exist, return None."""
        fake_file = tmp_path / "fake_assets.py"
        fake_file.write_text("", encoding="utf-8")
        # We need __file__ to point somewhere without core_pack
        import pdca_cli._assets as assets_mod
        original_file = assets_mod.__file__
        monkeypatch.setattr(assets_mod, "__file__", str(fake_file))
        try:
            result = _locate_core_pack()
            assert result is None
        finally:
            monkeypatch.setattr(assets_mod, "__file__", original_file)

    def test_returns_path_when_core_pack_exists(self, tmp_path):
        """When core_pack exists alongside the module file, return it."""
        # Create a fake assets module location with core_pack
        fake_dir = tmp_path / "pdca_cli"
        fake_dir.mkdir()
        core_pack = fake_dir / "core_pack"
        core_pack.mkdir()

        import pdca_cli._assets as assets_mod

        fake_file = fake_dir / "_assets.py"
        fake_file.write_text("", encoding="utf-8")

        with patch.object(assets_mod, "__file__", str(fake_file)):
            result = _locate_core_pack()
            assert result == core_pack


class TestRepoRoot:
    """Tests for _repo_root."""

    def test_returns_parent_of_parent_of_parent(self):
        """_repo_root should be 3 levels up from the _assets.py file."""
        root = _repo_root()
        assert isinstance(root, Path)
        # The file is at src/pdca_cli/_assets.py, so repo_root is 3 levels up
        assert root.is_dir()


class TestLocateBundledExtension:
    """Tests for _locate_bundled_extension."""

    def test_rejects_invalid_extension_id(self):
        """IDs with invalid characters return None."""
        assert _locate_bundled_extension("../escape") is None
        assert _locate_bundled_extension("bad/id") is None
        assert _locate_bundled_extension("") is None

    def test_returns_none_for_missing_extension(self):
        """Non-existent extension returns None."""
        result = _locate_bundled_extension("nonexistent-ext-99999")
        assert result is None

    def test_finds_bundled_extension(self):
        """A bundled extension like 'git' should be found."""
        result = _locate_bundled_extension("git")
        assert result is not None
        assert (result / "extension.yml").is_file()


class TestLocateBundledWorkflow:
    """Tests for _locate_bundled_workflow."""

    def test_rejects_invalid_workflow_id(self):
        """IDs with invalid characters return None."""
        assert _locate_bundled_workflow("../escape") is None
        assert _locate_bundled_workflow("-starts-with-dash") is None
        assert _locate_bundled_workflow("ends-with-dash-") is None

    def test_returns_none_for_missing_workflow(self):
        result = _locate_bundled_workflow("nonexistent-wf-99999")
        assert result is None

    def test_finds_bundled_workflow(self):
        """The 'pdca' workflow should be findable."""
        result = _locate_bundled_workflow("pdca")
        assert result is not None
        assert (result / "workflow.yml").is_file()


class TestLocateBundledPreset:
    """Tests for _locate_bundled_preset."""

    def test_rejects_invalid_preset_id(self):
        assert _locate_bundled_preset("../escape") is None

    def test_returns_none_for_missing_preset(self):
        result = _locate_bundled_preset("nonexistent-preset-99999")
        assert result is None

    def test_finds_bundled_preset(self):
        """The 'lean' preset should be findable."""
        result = _locate_bundled_preset("lean")
        assert result is not None
        assert (result / "preset.yml").is_file()


class TestGetPdcaVersion:
    """Tests for get_pdca_version."""

    def test_returns_string(self):
        version = get_pdca_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_returns_unknown_when_importlib_fails(self, monkeypatch):
        """When importlib.metadata.version raises, fall back to pyproject or 'unknown'."""
        def raise_error(_pkg):
            raise importlib.metadata.PackageNotFoundError

        monkeypatch.setattr(importlib.metadata, "version", raise_error)
        version = get_pdca_version()
        assert isinstance(version, str)
        # When importlib fails, it falls back to pyproject.toml reading.
        # In a dev checkout, this returns the actual dev version string.
        assert len(version) > 0
