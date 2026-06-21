"""Tests for pdca_cli._utils — additional coverage for utility functions.

Merge-related tests are already covered by test_merge.py.
Check_tool tests are covered by test_check_tool.py.
This module covers run_command, is_git_repo, init_git_repo, and
_display_project_path.
"""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pdca_cli._utils import (
    _display_project_path,
    init_git_repo,
    is_git_repo,
    run_command,
)


# ---------------------------------------------------------------------------
# run_command
# ---------------------------------------------------------------------------

class TestRunCommand:
    """Tests for run_command."""

    def test_capture_output(self):
        result = run_command(["echo", "hello"], capture=True)
        assert result == "hello"

    def test_no_capture_returns_none(self):
        result = run_command(["echo", "hello"], capture=False)
        assert result is None

    def test_check_return_false_on_error(self):
        import sys
        result = run_command(
            [sys.executable, "-c", "import sys; sys.exit(1)"],
            check_return=False,
            capture=True,
        )
        # When check_return=False and the command fails,
        # subprocess.run returns a CompletedProcess with empty stdout;
        # run_command returns the stripped stdout, which is empty string.
        assert result == ""

    def test_check_return_true_raises_on_error(self):
        import sys
        with pytest.raises(subprocess.CalledProcessError):
            run_command(
                [sys.executable, "-c", "import sys; sys.exit(1)"],
                check_return=True,
                capture=True,
            )

    def test_shell_mode(self):
        result = run_command("echo shell_test", capture=True, shell=True)
        assert "shell_test" in result


# ---------------------------------------------------------------------------
# is_git_repo
# ---------------------------------------------------------------------------

class TestIsGitRepo:
    """Tests for is_git_repo."""

    def test_returns_false_for_non_git_dir(self, tmp_path):
        assert is_git_repo(tmp_path) is False

    def test_returns_false_for_nonexistent_path(self, tmp_path):
        assert is_git_repo(tmp_path / "nonexistent") is False

    def test_returns_false_when_git_not_installed(self, tmp_path, monkeypatch):
        """When git command is not found, should return False."""
        monkeypatch.setattr(subprocess, "run", MagicMock(side_effect=FileNotFoundError))
        assert is_git_repo(tmp_path) is False

    def test_returns_false_when_not_in_work_tree(self, tmp_path, monkeypatch):
        """When git rev-parse fails, return False."""
        monkeypatch.setattr(
            subprocess, "run",
            MagicMock(side_effect=subprocess.CalledProcessError(128, "git")),
        )
        assert is_git_repo(tmp_path) is False

    def test_default_path_is_cwd(self, monkeypatch):
        """When path is None, uses Path.cwd()."""
        monkeypatch.setattr(subprocess, "run", MagicMock(return_value=MagicMock()))
        result = is_git_repo()
        assert result is True


# ---------------------------------------------------------------------------
# init_git_repo
# ---------------------------------------------------------------------------

class TestInitGitRepo:
    """Tests for init_git_repo."""

    def test_successful_init(self, tmp_path, monkeypatch):
        """Test init_git_repo with mocked subprocess to avoid filesystem issues."""
        root = tmp_path.resolve()

        # Mock subprocess.run to simulate successful git init/add/commit
        def mock_run(cmd, **kwargs):
            # Simulate creating .git dir on 'git init'
            if isinstance(cmd, list) and cmd[0] == "git":
                if "init" in cmd:
                    (root / ".git").mkdir(exist_ok=True)
            return MagicMock(returncode=0)

        monkeypatch.setattr(subprocess, "run", mock_run)
        success, error = init_git_repo(root, quiet=True)
        assert success is True
        assert error is None
        assert (root / ".git").is_dir()

    def test_failed_init_returns_error(self, tmp_path, monkeypatch):
        """When git init fails, return False and error message."""
        def failing_run(cmd, **kwargs):
            if cmd[0] == "git" and "init" in cmd:
                raise subprocess.CalledProcessError(
                    1, cmd, stderr="permission denied"
                )
            return MagicMock()

        monkeypatch.setattr(subprocess, "run", failing_run)
        root = tmp_path.resolve()
        success, error = init_git_repo(root, quiet=True)
        assert success is False
        assert error is not None
        assert "permission denied" in error


# ---------------------------------------------------------------------------
# _display_project_path
# ---------------------------------------------------------------------------

class TestDisplayProjectPath:
    """Tests for _display_project_path."""

    def test_relative_path_unchanged(self, tmp_path):
        result = _display_project_path(tmp_path, "subdir/file.txt")
        assert result == "subdir/file.txt"

    def test_absolute_path_inside_project(self, tmp_path):
        abs_path = tmp_path / "subdir" / "file.txt"
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        result = _display_project_path(tmp_path, abs_path)
        assert result == "subdir/file.txt"

    def test_path_outside_project_returns_as_is(self, tmp_path):
        outside = Path("/outside/project/file.txt")
        result = _display_project_path(tmp_path, outside)
        assert "outside" in result

    def test_posix_style_output(self, tmp_path):
        result = _display_project_path(tmp_path, Path("subdir/file.txt"))
        assert "\\" not in result
