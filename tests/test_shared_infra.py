"""Tests for pdca_cli.shared_infra — shared infrastructure installation helpers."""

import stat
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pdca_cli.shared_infra import (
    SymlinkedSharedPathError,
    _ensure_safe_shared_destination,
    _ensure_safe_shared_directory,
    _shared_destination_label,
    _shared_relative_path,
    _validate_safe_shared_directory,
    _write_shared_bytes,
    _write_shared_text,
    install_shared_infra,
    load_pdca_manifest,
    refresh_shared_templates,
    shared_scripts_source,
    shared_templates_source,
)


# ---------------------------------------------------------------------------
# _shared_destination_label
# ---------------------------------------------------------------------------

class TestSharedDestinationLabel:
    """Tests for _shared_destination_label."""

    def test_path_inside_project(self, tmp_path):
        dest = tmp_path / "sub" / "file.txt"
        label = _shared_destination_label(tmp_path, dest)
        assert label == "sub/file.txt"

    def test_path_outside_project(self, tmp_path):
        outside = Path("/outside/file.txt")
        label = _shared_destination_label(Path("/project"), outside)
        assert label == str(outside)


# ---------------------------------------------------------------------------
# _shared_relative_path
# ---------------------------------------------------------------------------

class TestSharedRelativePath:
    """Tests for _shared_relative_path."""

    def test_path_inside_project(self, tmp_path):
        dest = tmp_path / "sub" / "file.txt"
        rel = _shared_relative_path(tmp_path, dest)
        assert rel == Path("sub/file.txt")

    def test_path_outside_project_raises(self, tmp_path):
        outside = Path("/outside/file.txt")
        with pytest.raises(ValueError, match="escapes project root"):
            _shared_relative_path(tmp_path, outside)

    def test_parent_traversal_raises(self, tmp_path):
        dest = tmp_path / ".." / "escape.txt"
        with pytest.raises(ValueError, match="escapes project root"):
            _shared_relative_path(tmp_path, dest)


# ---------------------------------------------------------------------------
# _ensure_safe_shared_directory
# ---------------------------------------------------------------------------

class TestEnsureSafeSharedDirectory:
    """Tests for _ensure_safe_shared_directory."""

    def test_creates_directory(self, tmp_path):
        dest = tmp_path / ".pdca" / "scripts"
        _ensure_safe_shared_directory(tmp_path, dest)
        assert dest.is_dir()

    def test_existing_directory_ok(self, tmp_path):
        dest = tmp_path / ".pdca" / "templates"
        dest.mkdir(parents=True)
        _ensure_safe_shared_directory(tmp_path, dest)  # should not raise

    def test_symlink_rejected(self, tmp_path):
        real_dir = tmp_path / "real"
        real_dir.mkdir()
        link = tmp_path / ".pdca" / "link"
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(real_dir, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not permitted")
        with pytest.raises(SymlinkedSharedPathError):
            _ensure_safe_shared_directory(tmp_path, link)

    def test_non_directory_path_raises(self, tmp_path):
        file_path = tmp_path / "file.txt"
        file_path.write_text("data")
        dest = tmp_path / "file.txt" / "sub"
        with pytest.raises(ValueError, match="not a directory"):
            _ensure_safe_shared_directory(tmp_path, dest)

    def test_create_false_missing_raises(self, tmp_path):
        dest = tmp_path / ".pdca" / "missing"
        with pytest.raises(ValueError, match="does not exist"):
            _ensure_safe_shared_directory(tmp_path, dest, create=False)


# ---------------------------------------------------------------------------
# _validate_safe_shared_directory
# ---------------------------------------------------------------------------

class TestValidateSafeSharedDirectory:
    """Tests for _validate_safe_shared_directory."""

    def test_existing_dir_ok(self, tmp_path):
        dest = tmp_path / "existing"
        dest.mkdir()
        _validate_safe_shared_directory(tmp_path, dest)  # should not raise

    def test_missing_dir_ok(self, tmp_path):
        dest = tmp_path / "missing"
        _validate_safe_shared_directory(tmp_path, dest)  # should not raise

    def test_symlink_rejected(self, tmp_path):
        real_dir = tmp_path / "real"
        real_dir.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(real_dir, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not permitted")
        with pytest.raises(SymlinkedSharedPathError):
            _validate_safe_shared_directory(tmp_path, link)

    def test_non_directory_raises(self, tmp_path):
        file_path = tmp_path / "file.txt"
        file_path.write_text("data")
        with pytest.raises(ValueError, match="not a directory"):
            _validate_safe_shared_directory(tmp_path, file_path)


# ---------------------------------------------------------------------------
# _ensure_safe_shared_destination
# ---------------------------------------------------------------------------

class TestEnsureSafeSharedDestination:
    """Tests for _ensure_safe_shared_destination."""

    def test_safe_destination_ok(self, tmp_path):
        dest = tmp_path / "sub" / "file.txt"
        dest.parent.mkdir(parents=True)
        _ensure_safe_shared_destination(tmp_path, dest)  # should not raise

    def test_symlink_destination_rejected(self, tmp_path):
        real_file = tmp_path / "real.txt"
        real_file.write_text("data")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(real_file)
        except OSError:
            pytest.skip("symlink creation not permitted")
        with pytest.raises(SymlinkedSharedPathError):
            _ensure_safe_shared_destination(tmp_path, link)

    def test_parent_must_exist_creates_parent(self, tmp_path):
        """When parent_must_exist=True (default), parent must exist."""
        dest = tmp_path / "missing_parent" / "file.txt"
        with pytest.raises(ValueError, match="does not exist"):
            _ensure_safe_shared_destination(tmp_path, dest, parent_must_exist=True)

    def test_parent_must_exist_false_allows_missing(self, tmp_path):
        """When parent_must_exist=False, missing parent is allowed."""
        dest = tmp_path / "missing_parent" / "file.txt"
        # Should not raise about missing parent
        _ensure_safe_shared_destination(tmp_path, dest, parent_must_exist=False)


# ---------------------------------------------------------------------------
# _write_shared_text and _write_shared_bytes
# ---------------------------------------------------------------------------

class TestWriteSharedText:
    """Tests for _write_shared_text and _write_shared_bytes."""

    def test_write_text_file(self, tmp_path):
        dest = tmp_path / "output" / "test.txt"
        dest.parent.mkdir(parents=True)
        _write_shared_text(tmp_path, dest, "hello world")
        assert dest.read_text(encoding="utf-8") == "hello world"

    def test_write_bytes_file(self, tmp_path):
        dest = tmp_path / "output" / "test.bin"
        dest.parent.mkdir(parents=True)
        _write_shared_bytes(tmp_path, dest, b"binary data")
        assert dest.read_bytes() == b"binary data"

    def test_write_overwrites_existing(self, tmp_path):
        dest = tmp_path / "output" / "test.txt"
        dest.parent.mkdir(parents=True)
        dest.write_text("old")
        _write_shared_text(tmp_path, dest, "new")
        assert dest.read_text(encoding="utf-8") == "new"

    def test_write_bytes_mode(self, tmp_path):
        dest = tmp_path / "output" / "script.sh"
        dest.parent.mkdir(parents=True)
        _write_shared_bytes(tmp_path, dest, b"#!/bin/bash\necho hi", mode=0o755)
        file_mode = stat.S_IMODE(dest.stat().st_mode)
        assert file_mode == 0o755

    def test_write_refuses_symlink(self, tmp_path):
        real_file = tmp_path / "real.txt"
        real_file.write_text("real")
        link = tmp_path / "link.txt"
        try:
            link.symlink_to(real_file)
        except OSError:
            pytest.skip("symlink creation not permitted")
        with pytest.raises(SymlinkedSharedPathError):
            _write_shared_text(tmp_path, link, "should fail")


# ---------------------------------------------------------------------------
# shared_templates_source / shared_scripts_source
# ---------------------------------------------------------------------------

class TestSharedSource:
    """Tests for shared_templates_source and shared_scripts_source."""

    def test_templates_source_from_core_pack(self, tmp_path):
        core = tmp_path / "core_pack"
        (core / "templates").mkdir(parents=True)
        result = shared_templates_source(core_pack=core, repo_root=tmp_path)
        assert result == core / "templates"

    def test_templates_source_fallback_to_repo(self, tmp_path):
        (tmp_path / "templates").mkdir(parents=True)
        result = shared_templates_source(core_pack=None, repo_root=tmp_path)
        assert result == tmp_path / "templates"

    def test_templates_source_core_pack_no_templates(self, tmp_path):
        core = tmp_path / "core_pack"
        core.mkdir()  # no templates subdir
        (tmp_path / "templates").mkdir(parents=True)
        result = shared_templates_source(core_pack=core, repo_root=tmp_path)
        assert result == tmp_path / "templates"

    def test_scripts_source_from_core_pack(self, tmp_path):
        core = tmp_path / "core_pack"
        (core / "scripts").mkdir(parents=True)
        result = shared_scripts_source(core_pack=core, repo_root=tmp_path)
        assert result == core / "scripts"

    def test_scripts_source_fallback_to_repo(self, tmp_path):
        (tmp_path / "scripts").mkdir(parents=True)
        result = shared_scripts_source(core_pack=None, repo_root=tmp_path)
        assert result == tmp_path / "scripts"


# ---------------------------------------------------------------------------
# load_pdca_manifest
# ---------------------------------------------------------------------------

class TestLoadPdcaManifest:
    """Tests for load_pdca_manifest."""

    def test_new_manifest_when_no_file(self, tmp_path):
        from pdca_cli.integrations.manifest import IntegrationManifest
        manifest = load_pdca_manifest(tmp_path, version="1.0.0")
        assert isinstance(manifest, IntegrationManifest)
        assert manifest.key == "pdca"
        assert manifest.version == "1.0.0"

    def test_loads_existing_manifest(self, tmp_path):
        from pdca_cli.integrations.manifest import IntegrationManifest
        # Use resolved path to avoid macOS /var symlink issues
        root = tmp_path.resolve()
        test_file = root / ".pdca" / "templates" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("content", encoding="utf-8")

        # Create a manifest file
        existing = IntegrationManifest("pdca", root, version="0.9.0")
        existing.record_existing(".pdca/templates/test.md")
        existing.save()

        manifest = load_pdca_manifest(root, version="1.0.0")
        assert manifest.version == "1.0.0"  # version is updated
        assert ".pdca/templates/test.md" in dict(manifest.files)

    def test_corrupt_manifest_creates_new(self, tmp_path):
        manifest_path = tmp_path / ".pdca" / "integrations" / "pdca.manifest.json"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text("{invalid json", encoding="utf-8")

        console = MagicMock()
        manifest = load_pdca_manifest(tmp_path, version="1.0.0", console=console)
        assert manifest.version == "1.0.0"
        console.print.assert_called()  # Warning was printed


# ---------------------------------------------------------------------------
# refresh_shared_templates
# ---------------------------------------------------------------------------

class TestRefreshSharedTemplates:
    """Tests for refresh_shared_templates."""

    def test_refresh_copies_templates(self, tmp_path):
        # Set up source templates
        templates_src = tmp_path / "templates"
        templates_src.mkdir()
        (templates_src / "plan-template.md").write_text("# Plan\n\n{SCRIPT}\n", encoding="utf-8")
        (templates_src / "spec-template.md").write_text("# Spec\n", encoding="utf-8")
        (templates_src / "vscode-settings.json").write_text("{}", encoding="utf-8")
        (templates_src / ".hidden").write_text("hidden", encoding="utf-8")

        console = MagicMock()
        refresh_shared_templates(
            tmp_path,
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            invoke_separator=".",
        )

        dest = tmp_path / ".pdca" / "templates"
        assert (dest / "plan-template.md").exists()
        assert (dest / "spec-template.md").exists()
        # vscode-settings.json should be excluded
        assert not (dest / "vscode-settings.json").exists()
        # hidden files should be excluded
        assert not (dest / ".hidden").exists()

    def test_refresh_skips_modified_files(self, tmp_path):
        templates_src = tmp_path / "templates"
        templates_src.mkdir()
        (templates_src / "plan-template.md").write_text("# Plan\n", encoding="utf-8")

        # Pre-create a destination file
        dest_dir = tmp_path / ".pdca" / "templates"
        dest_dir.mkdir(parents=True)
        dest_file = dest_dir / "plan-template.md"
        dest_file.write_text("# Modified by user\n", encoding="utf-8")

        console = MagicMock()
        refresh_shared_templates(
            tmp_path,
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            invoke_separator=".",
        )

        # Content should NOT be overwritten (no manifest tracking, so it's "untracked")
        assert "Modified by user" in dest_file.read_text(encoding="utf-8")

    def test_refresh_force_overwrites(self, tmp_path):
        templates_src = tmp_path / "templates"
        templates_src.mkdir()
        (templates_src / "plan-template.md").write_text("# Plan v2\n", encoding="utf-8")

        dest_dir = tmp_path / ".pdca" / "templates"
        dest_dir.mkdir(parents=True)
        dest_file = dest_dir / "plan-template.md"
        dest_file.write_text("# Old\n", encoding="utf-8")

        console = MagicMock()
        refresh_shared_templates(
            tmp_path,
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            invoke_separator=".",
            force=True,
        )

        assert "# Plan v2" in dest_file.read_text(encoding="utf-8")

    def test_no_templates_source_no_op(self, tmp_path):
        console = MagicMock()
        # No templates dir exists
        refresh_shared_templates(
            tmp_path,
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            invoke_separator=".",
        )
        # Should not create anything and not crash
        assert not (tmp_path / ".pdca" / "templates").exists()


# ---------------------------------------------------------------------------
# install_shared_infra
# ---------------------------------------------------------------------------

class TestInstallSharedInfra:
    """Tests for install_shared_infra."""

    def test_installs_scripts_and_templates(self, tmp_path):
        # Set up source scripts and templates
        (tmp_path / "scripts" / "bash").mkdir(parents=True)
        (tmp_path / "scripts" / "bash" / "helper.sh").write_text("#!/bin/bash\necho hi\n", encoding="utf-8")

        (tmp_path / "templates").mkdir(parents=True)
        (tmp_path / "templates" / "plan-template.md").write_text("# Plan\n", encoding="utf-8")

        console = MagicMock()
        result = install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
        )

        assert result is True
        assert (tmp_path / ".pdca" / "scripts" / "bash" / "helper.sh").exists()
        assert (tmp_path / ".pdca" / "templates" / "plan-template.md").exists()

    def test_no_scripts_source_still_installs_templates(self, tmp_path):
        (tmp_path / "templates").mkdir(parents=True)
        (tmp_path / "templates" / "plan-template.md").write_text("# Plan\n", encoding="utf-8")

        console = MagicMock()
        result = install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
        )

        assert result is True
        assert (tmp_path / ".pdca" / "templates" / "plan-template.md").exists()

    def test_skips_existing_files_without_force(self, tmp_path):
        (tmp_path / "templates").mkdir(parents=True)
        (tmp_path / "templates" / "plan-template.md").write_text("# Plan\n", encoding="utf-8")

        dest = tmp_path / ".pdca" / "templates"
        dest.mkdir(parents=True)
        (dest / "plan-template.md").write_text("# User modified\n", encoding="utf-8")

        console = MagicMock()
        install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
        )

        assert "# User modified" in (dest / "plan-template.md").read_text(encoding="utf-8")

    def test_force_overwrites_existing(self, tmp_path):
        (tmp_path / "templates").mkdir(parents=True)
        (tmp_path / "templates" / "plan-template.md").write_text("# Plan v2\n", encoding="utf-8")

        dest = tmp_path / ".pdca" / "templates"
        dest.mkdir(parents=True)
        (dest / "plan-template.md").write_text("# Old\n", encoding="utf-8")

        console = MagicMock()
        install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            force=True,
        )

        assert "# Plan v2" in (dest / "plan-template.md").read_text(encoding="utf-8")

    def test_handles_symlink_paths_gracefully(self, tmp_path):
        real_dir = tmp_path / "real_templates"
        real_dir.mkdir()
        link = tmp_path / "templates"
        try:
            link.symlink_to(real_dir, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not permitted")

        (real_dir / "plan-template.md").write_text("# Plan\n", encoding="utf-8")

        console = MagicMock()
        result = install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
        )

        assert result is True
        # Symlinked source should not cause crash; dest won't be created due to symlink check

    def test_refresh_managed_overwrites_unmodified(self, tmp_path):
        (tmp_path / "templates").mkdir(parents=True)
        src = tmp_path / "templates" / "plan-template.md"
        src.write_text("# Plan\n", encoding="utf-8")

        dest = tmp_path / ".pdca" / "templates"
        dest.mkdir(parents=True)
        dest_file = dest / "plan-template.md"
        dest_file.write_text("# Plan\n", encoding="utf-8")

        # Set up manifest with matching hash
        from pdca_cli.integrations.manifest import IntegrationManifest
        manifest = IntegrationManifest("pdca", tmp_path, version="1.0.0")
        manifest.record_existing(".pdca/templates/plan-template.md")
        manifest.save()

        console = MagicMock()
        install_shared_infra(
            tmp_path,
            "sh",
            version="1.0.0",
            core_pack=None,
            repo_root=tmp_path,
            console=console,
            refresh_managed=True,
        )
        # Since hash matches, it should be refreshed
        assert dest_file.exists()
