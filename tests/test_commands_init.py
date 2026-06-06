"""Tests for pdca_cli.commands.init — init command helpers."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pdca_cli.commands.init import (
    _build_ai_deprecation_warning,
    _build_integration_equivalent,
    _stdin_is_interactive,
    ensure_constitution_from_template,
)


# ---------------------------------------------------------------------------
# _build_integration_equivalent
# ---------------------------------------------------------------------------

class TestBuildIntegrationEquivalent:
    """Tests for _build_integration_equivalent."""

    def test_standard_integration(self):
        result = _build_integration_equivalent("claude")
        assert "--integration claude" in result

    def test_generic_integration_with_commands_dir(self):
        result = _build_integration_equivalent("generic", ai_commands_dir=".myagent/commands/")
        assert "--integration generic" in result
        assert "--commands-dir" in result
        assert ".myagent/commands/" in result

    def test_generic_integration_without_commands_dir(self):
        result = _build_integration_equivalent("generic")
        assert "--integration generic" in result
        assert "--commands-dir" not in result


# ---------------------------------------------------------------------------
# _build_ai_deprecation_warning
# ---------------------------------------------------------------------------

class TestBuildAiDeprecationWarning:
    """Tests for _build_ai_deprecation_warning."""

    def test_warning_contains_replacement(self):
        result = _build_ai_deprecation_warning("claude")
        assert "--ai" in result
        assert "deprecated" in result.lower()
        assert "--integration claude" in result

    def test_warning_mentions_version(self):
        result = _build_ai_deprecation_warning("gemini")
        assert "0.10.0" in result


# ---------------------------------------------------------------------------
# _stdin_is_interactive
# ---------------------------------------------------------------------------

class TestStdinIsInteractive:
    """Tests for _stdin_is_interactive."""

    def test_returns_bool(self):
        result = _stdin_is_interactive()
        assert isinstance(result, bool)

    def test_returns_false_when_stdin_not_tty(self, monkeypatch):
        """When sys.stdin.isatty() returns False, result should be False."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = False
        monkeypatch.setattr("sys.stdin", mock_stdin)
        assert _stdin_is_interactive() is False

    def test_returns_true_when_stdin_is_tty(self, monkeypatch):
        """When sys.stdin.isatty() returns True, result should be True."""
        mock_stdin = MagicMock()
        mock_stdin.isatty.return_value = True
        monkeypatch.setattr("sys.stdin", mock_stdin)
        assert _stdin_is_interactive() is True


# ---------------------------------------------------------------------------
# ensure_constitution_from_template
# ---------------------------------------------------------------------------

class TestEnsureConstitutionFromTemplate:
    """Tests for ensure_constitution_from_template."""

    def test_copies_template_when_memory_missing(self, tmp_path):
        # Set up project structure
        (tmp_path / ".pdca" / "templates").mkdir(parents=True)
        (tmp_path / ".pdca" / "templates" / "constitution-template.md").write_text(
            "# Constitution Template\n\nProject principles here.\n",
            encoding="utf-8",
        )

        ensure_constitution_from_template(tmp_path)

        memory_file = tmp_path / ".pdca" / "memory" / "constitution.md"
        assert memory_file.exists()
        content = memory_file.read_text(encoding="utf-8")
        assert "Constitution Template" in content

    def test_preserves_existing_constitution(self, tmp_path):
        (tmp_path / ".pdca" / "memory").mkdir(parents=True)
        existing = tmp_path / ".pdca" / "memory" / "constitution.md"
        existing.write_text("# My Custom Constitution\n", encoding="utf-8")

        ensure_constitution_from_template(tmp_path)

        content = existing.read_text(encoding="utf-8")
        assert "My Custom Constitution" in content

    def test_template_missing_no_error(self, tmp_path):
        """When template doesn't exist, should not crash."""
        # No templates dir
        ensure_constitution_from_template(tmp_path)
        # Should not have created memory file
        assert not (tmp_path / ".pdca" / "memory" / "constitution.md").exists()

    def test_with_tracker_skip_existing(self, tmp_path):
        (tmp_path / ".pdca" / "memory").mkdir(parents=True)
        (tmp_path / ".pdca" / "memory" / "constitution.md").write_text("# Existing\n")

        tracker = MagicMock()
        ensure_constitution_from_template(tmp_path, tracker=tracker)

        tracker.add.assert_called_with("constitution", "Constitution setup")
        tracker.skip.assert_called_with("constitution", "existing file preserved")

    def test_with_tracker_copied_from_template(self, tmp_path):
        (tmp_path / ".pdca" / "templates").mkdir(parents=True)
        (tmp_path / ".pdca" / "templates" / "constitution-template.md").write_text("# Template\n")

        tracker = MagicMock()
        ensure_constitution_from_template(tmp_path, tracker=tracker)

        tracker.add.assert_called_with("constitution", "Constitution setup")
        tracker.complete.assert_called_with("constitution", "copied from template")

    def test_with_tracker_template_not_found(self, tmp_path):
        tracker = MagicMock()
        ensure_constitution_from_template(tmp_path, tracker=tracker)

        tracker.add.assert_called_with("constitution", "Constitution setup")
        tracker.error.assert_called_with("constitution", "template not found")

    def test_with_tracker_copy_error(self, tmp_path, monkeypatch):
        (tmp_path / ".pdca" / "templates").mkdir(parents=True)
        (tmp_path / ".pdca" / "templates" / "constitution-template.md").write_text("# Template\n")

        # Force shutil.copy2 to fail
        import shutil
        def failing_copy2(src, dst):
            raise OSError("Simulated copy error")
        monkeypatch.setattr(shutil, "copy2", failing_copy2)

        tracker = MagicMock()
        ensure_constitution_from_template(tmp_path, tracker=tracker)
        tracker.add.assert_called_with("constitution", "Constitution setup")
        assert tracker.error.called
