"""Tests for pdca_cli.agents — CommandRegistrar additional unit tests.

Path-traversal guards are already covered by test_registrar_path_traversal.py.
This module adds coverage for parsing, rendering, name computation, and helper
methods.
"""

from pathlib import Path

import pytest

from pdca_cli.agents import CommandRegistrar, _build_agent_configs


# ---------------------------------------------------------------------------
# _build_agent_configs
# ---------------------------------------------------------------------------

class TestBuildAgentConfigs:
    """Tests for _build_agent_configs helper."""

    def test_returns_dict(self):
        configs = _build_agent_configs()
        assert isinstance(configs, dict)

    def test_excludes_generic_key(self):
        configs = _build_agent_configs()
        assert "generic" not in configs

    def test_includes_known_agents(self):
        configs = _build_agent_configs()
        # At least some well-known agents should be present
        assert "claude" in configs or len(configs) > 0

    def test_each_entry_has_required_keys(self):
        configs = _build_agent_configs()
        for key, cfg in configs.items():
            assert "dir" in cfg, f"{key} missing 'dir'"
            assert "format" in cfg, f"{key} missing 'format'"
            assert "args" in cfg, f"{key} missing 'args'"
            assert "extension" in cfg, f"{key} missing 'extension'"


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    """Tests for CommandRegistrar.parse_frontmatter."""

    def test_parses_valid_frontmatter(self):
        content = "---\ndescription: test command\n---\n\nBody text here."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {"description": "test command"}
        assert body == "Body text here."

    def test_no_frontmatter_returns_empty_dict(self):
        content = "Just body text, no frontmatter."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {}
        assert body == "Just body text, no frontmatter."

    def test_missing_closing_delimiter(self):
        content = "---\ndescription: test\nBody without closing."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {}
        assert body == content

    def test_invalid_yaml_frontmatter(self):
        content = "---\n{invalid: [yaml\n---\n\nBody."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {}
        assert body == "Body."

    def test_frontmatter_is_list_not_dict(self):
        content = "---\n- item1\n- item2\n---\n\nBody."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {}
        assert body == "Body."

    def test_empty_frontmatter(self):
        content = "---\n---\n\nBody."
        fm, body = CommandRegistrar.parse_frontmatter(content)
        assert fm == {}
        assert body == "Body."


# ---------------------------------------------------------------------------
# render_frontmatter
# ---------------------------------------------------------------------------

class TestRenderFrontmatter:
    """Tests for CommandRegistrar.render_frontmatter."""

    def test_renders_dict(self):
        fm = {"description": "test"}
        result = CommandRegistrar.render_frontmatter(fm)
        assert result.startswith("---\n")
        assert "description: test" in result
        assert result.strip().endswith("---")

    def test_empty_dict_returns_empty_string(self):
        result = CommandRegistrar.render_frontmatter({})
        assert result == ""


# ---------------------------------------------------------------------------
# _render_basic_toml_string
# ---------------------------------------------------------------------------

class TestRenderBasicTomlString:
    """Tests for CommandRegistrar._render_basic_toml_string."""

    def test_simple_string(self):
        result = CommandRegistrar._render_basic_toml_string("hello")
        assert result == '"hello"'

    def test_escapes_quotes(self):
        result = CommandRegistrar._render_basic_toml_string('say "hi"')
        assert result == '"say \\"hi\\""'

    def test_escapes_backslash(self):
        result = CommandRegistrar._render_basic_toml_string("path\\to")
        assert result == '"path\\\\to"'

    def test_escapes_newline(self):
        result = CommandRegistrar._render_basic_toml_string("line1\nline2")
        assert "\\n" in result

    def test_escapes_tab(self):
        result = CommandRegistrar._render_basic_toml_string("col1\tcol2")
        assert "\\t" in result

    def test_escapes_carriage_return(self):
        result = CommandRegistrar._render_basic_toml_string("line\r")
        assert "\\r" in result


# ---------------------------------------------------------------------------
# render_toml_command
# ---------------------------------------------------------------------------

class TestRenderTomlCommand:
    """Tests for render_toml_command."""

    def test_basic_toml_output(self):
        registrar = CommandRegistrar()
        result = registrar.render_toml_command(
            {"description": "Test command"},
            "Do something",
            "test-source",
        )
        assert 'description = "Test command"' in result
        assert "# Source: test-source" in result
        assert "Do something" in result

    def test_no_description_in_frontmatter(self):
        registrar = CommandRegistrar()
        result = registrar.render_toml_command(
            {"name": "test"},
            "Body only",
            "src",
        )
        assert 'description' not in result or "name" not in result

    def test_body_with_triple_double_quotes_falls_back_to_single(self):
        registrar = CommandRegistrar()
        result = registrar.render_toml_command(
            {"description": "test"},
            'Text with """ in body',
            "src",
        )
        assert "'''" in result

    def test_body_with_both_triple_quotes_falls_back_to_basic(self):
        registrar = CommandRegistrar()
        result = registrar.render_toml_command(
            {"description": "test"},
            'Text with """ and \'\'\' in body',
            "src",
        )
        # Should use basic string escaping (double-quoted with escapes)
        assert 'prompt = "' in result


# ---------------------------------------------------------------------------
# render_markdown_command
# ---------------------------------------------------------------------------

class TestRenderMarkdownCommand:
    """Tests for render_markdown_command."""

    def test_basic_markdown_output(self):
        registrar = CommandRegistrar()
        result = registrar.render_markdown_command(
            {"description": "Test command"},
            "Do something with $ARGUMENTS",
            "myext",
        )
        assert "description: Test command" in result
        assert "<!-- Source: myext -->" in result
        assert "Do something with $ARGUMENTS" in result

    def test_custom_context_note(self):
        registrar = CommandRegistrar()
        result = registrar.render_markdown_command(
            {"description": "Test"},
            "Body",
            "myext",
            context_note="\n<!-- Custom note -->\n",
        )
        assert "<!-- Custom note -->" in result


# ---------------------------------------------------------------------------
# _hyphenate_frontmatter_refs and _hyphenate_body_refs
# ---------------------------------------------------------------------------

class TestHyphenateRefs:
    """Tests for pdca. reference hyphenation (Cline extension)."""

    def test_hyphenate_frontmatter_dict(self):
        fm = {"scripts": {"sh": "pdca.myext.command"}}
        result = CommandRegistrar._hyphenate_frontmatter_refs(fm)
        assert result["scripts"]["sh"] == "pdca-myext-command"

    def test_hyphenate_frontmatter_list(self):
        data = ["pdca.a.b", "pdca.c"]
        result = CommandRegistrar._hyphenate_frontmatter_refs(data)
        assert result == ["pdca-a-b", "pdca-c"]

    def test_hyphenate_frontmatter_nested(self):
        data = {"a": {"b": ["pdca.x.y"]}}
        result = CommandRegistrar._hyphenate_frontmatter_refs(data)
        assert result["a"]["b"] == ["pdca-x-y"]

    def test_hyphenate_body_refs(self):
        body = "Use /pdca.myext.command for this."
        result = CommandRegistrar._hyphenate_body_refs(body)
        assert "pdca-myext-command" in result
        assert "pdca.myext.command" not in result

    def test_non_pdca_refs_unchanged(self):
        body = "Use some.other.ref here."
        result = CommandRegistrar._hyphenate_body_refs(body)
        assert result == body

    def test_non_string_passed_through(self):
        result = CommandRegistrar._hyphenate_frontmatter_refs(42)
        assert result == 42


# ---------------------------------------------------------------------------
# rewrite_project_relative_paths
# ---------------------------------------------------------------------------

class TestRewriteProjectRelativePaths:
    """Tests for rewrite_project_relative_paths."""

    def test_rewrites_scripts_prefix(self):
        result = CommandRegistrar.rewrite_project_relative_paths(
            "Run scripts/helper.sh"
        )
        assert ".pdca/scripts/helper.sh" in result

    def test_rewrites_memory_prefix(self):
        result = CommandRegistrar.rewrite_project_relative_paths(
            "See memory/constitution.md"
        )
        assert ".pdca/memory/constitution.md" in result

    def test_rewrites_templates_prefix(self):
        result = CommandRegistrar.rewrite_project_relative_paths(
            "Use templates/plan.md"
        )
        assert ".pdca/templates/plan.md" in result

    def test_rewrites_parent_relative_paths(self):
        result = CommandRegistrar.rewrite_project_relative_paths(
            "../../scripts/helper.sh"
        )
        assert ".pdca/scripts/helper.sh" in result
        assert "../../scripts/" not in result

    def test_no_double_pdca_prefix(self):
        result = CommandRegistrar.rewrite_project_relative_paths(
            ".pdca/scripts/helper.sh"
        )
        assert ".pdca/.pdca/" not in result
        assert result == ".pdca/scripts/helper.sh"

    def test_empty_string_unchanged(self):
        assert CommandRegistrar.rewrite_project_relative_paths("") == ""

    def test_non_string_unchanged(self):
        assert CommandRegistrar.rewrite_project_relative_paths(None) is None
        assert CommandRegistrar.rewrite_project_relative_paths(42) == 42


# ---------------------------------------------------------------------------
# _is_safe_command_name
# ---------------------------------------------------------------------------

class TestIsSafeCommandName:
    """Tests for _is_safe_command_name."""

    def test_allows_normal_names(self):
        assert CommandRegistrar._is_safe_command_name("pdca.myext.hello") is True
        assert CommandRegistrar._is_safe_command_name("plan") is True
        assert CommandRegistrar._is_safe_command_name("my-command") is True

    def test_rejects_path_separator(self):
        assert CommandRegistrar._is_safe_command_name("sub/command") is False
        assert CommandRegistrar._is_safe_command_name("sub\\command") is False

    def test_rejects_dot_dot(self):
        assert CommandRegistrar._is_safe_command_name("../escape") is False

    def test_rejects_windows_drive_letter(self):
        assert CommandRegistrar._is_safe_command_name("C:evil") is False


# ---------------------------------------------------------------------------
# _compute_output_name
# ---------------------------------------------------------------------------

class TestComputeOutputName:
    """Tests for _compute_output_name."""

    def test_normal_agent_returns_name_unchanged(self):
        config = {"extension": ".md", "args": "$ARGUMENTS"}
        result = CommandRegistrar._compute_output_name("windsurf", "pdca.plan", config)
        assert result == "pdca.plan"

    def test_skill_agent_strips_prefix(self):
        config = {"extension": "/SKILL.md", "args": "$ARGUMENTS"}
        result = CommandRegistrar._compute_output_name("claude", "pdca.plan", config)
        assert result == "pdca-plan"

    def test_skill_agent_dots_to_hyphens(self):
        config = {"extension": "/SKILL.md", "args": "$ARGUMENTS"}
        result = CommandRegistrar._compute_output_name("claude", "pdca.myext.command", config)
        assert result == "pdca-myext-command"

    def test_skill_agent_no_pdca_prefix(self):
        config = {"extension": "/SKILL.md", "args": "$ARGUMENTS"}
        result = CommandRegistrar._compute_output_name("claude", "my-command", config)
        assert result == "pdca-my-command"

    def test_format_name_callback(self):
        def fmt(name):
            return f"custom-{name}"

        config = {"extension": ".md", "args": "$ARGUMENTS", "format_name": fmt}
        result = CommandRegistrar._compute_output_name("test", "plan", config)
        assert result == "custom-plan"


# ---------------------------------------------------------------------------
# _ensure_inside
# ---------------------------------------------------------------------------

class TestEnsureInside:
    """Tests for _ensure_inside."""

    def test_allows_path_inside_base(self):
        base = Path("/project/.gemini/commands")
        candidate = Path("/project/.gemini/commands/mycommand.toml")
        CommandRegistrar._ensure_inside(candidate, base)  # should not raise

    def test_rejects_path_outside_base(self):
        base = Path("/project/.gemini/commands")
        candidate = Path("/project/evil.toml")
        with pytest.raises(ValueError, match="escapes directory"):
            CommandRegistrar._ensure_inside(candidate, base)

    def test_rejects_parent_traversal(self):
        base = Path("/project/.gemini/commands")
        candidate = Path("/project/.gemini/commands/../evil.toml")
        with pytest.raises(ValueError, match="escapes directory"):
            CommandRegistrar._ensure_inside(candidate, base)


# ---------------------------------------------------------------------------
# build_skill_frontmatter
# ---------------------------------------------------------------------------

class TestBuildSkillFrontmatter:
    """Tests for build_skill_frontmatter."""

    def test_returns_expected_structure(self):
        fm = CommandRegistrar.build_skill_frontmatter(
            "claude", "pdca-plan", "Plan command", "core:plan.md"
        )
        assert fm["name"] == "pdca-plan"
        assert fm["description"] == "Plan command"
        assert fm["compatibility"] == "Requires pdca-kit project structure with .pdca/ directory"
        assert fm["metadata"]["author"] == "github-pdca-kit"
        assert fm["metadata"]["source"] == "core:plan.md"


# ---------------------------------------------------------------------------
# write_copilot_prompt
# ---------------------------------------------------------------------------

class TestWriteCopilotPrompt:
    """Tests for write_copilot_prompt."""

    def test_creates_prompt_file(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        (project / ".github" / "prompts").mkdir(parents=True)
        CommandRegistrar.write_copilot_prompt(project, "pdca.plan")
        prompt_file = project / ".github" / "prompts" / "pdca.plan.prompt.md"
        assert prompt_file.exists()
        content = prompt_file.read_text(encoding="utf-8")
        assert "agent: pdca.plan" in content


# ---------------------------------------------------------------------------
# _convert_argument_placeholder
# ---------------------------------------------------------------------------

class TestConvertArgumentPlaceholder:
    """Tests for _convert_argument_placeholder."""

    def test_converts_dollar_args_to_braces(self):
        registrar = CommandRegistrar()
        result = registrar._convert_argument_placeholder(
            "Use $ARGUMENTS here", "$ARGUMENTS", "{{args}}"
        )
        assert result == "Use {{args}} here"

    def test_no_placeholder_unchanged(self):
        registrar = CommandRegistrar()
        result = registrar._convert_argument_placeholder(
            "No placeholder", "$ARGUMENTS", "{{args}}"
        )
        assert result == "No placeholder"


# ---------------------------------------------------------------------------
# _resolve_agent_dir
# ---------------------------------------------------------------------------

class TestResolveAgentDir:
    """Tests for _resolve_agent_dir."""

    def test_relative_dir_resolves_under_project(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        agent_dir = project / ".windsurf" / "workflows"
        agent_dir.mkdir(parents=True)

        config = {"dir": ".windsurf/workflows"}
        result = CommandRegistrar._resolve_agent_dir("windsurf", config, project)
        assert result == agent_dir

    def test_absolute_dir_used_as_is(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        abs_dir = tmp_path / "abs" / "commands"
        abs_dir.mkdir(parents=True)

        config = {"dir": str(abs_dir)}
        result = CommandRegistrar._resolve_agent_dir("test", config, project)
        assert result == abs_dir

    def test_legacy_dir_fallback(self, tmp_path):
        project = tmp_path / "project"
        project.mkdir()
        legacy_dir = project / ".old" / "commands"
        legacy_dir.mkdir(parents=True)

        config = {"dir": ".new/commands", "legacy_dir": ".old/commands"}
        with pytest.warns(UserWarning, match="legacy"):
            result = CommandRegistrar._resolve_agent_dir("test", config, project)
        assert result == legacy_dir

    def test_home_relative_dir(self, tmp_path, monkeypatch):
        home = tmp_path / "home"
        home.mkdir()
        agent_dir = home / ".hermes" / "skills"
        agent_dir.mkdir(parents=True)

        monkeypatch.setattr(Path, "home", lambda: home)
        config = {"dir": "~/.hermes/skills"}
        result = CommandRegistrar._resolve_agent_dir("hermes", config, tmp_path / "project")
        assert result == agent_dir


# ---------------------------------------------------------------------------
# register_commands error cases
# ---------------------------------------------------------------------------

class TestRegisterCommandsErrors:
    """Tests for register_commands error handling."""

    def test_unsupported_agent_raises(self):
        registrar = CommandRegistrar()
        with pytest.raises(ValueError, match="Unsupported agent"):
            registrar.register_commands(
                "nonexistent-agent-xyz",
                [],
                "src",
                Path("/tmp"),
                Path("/tmp"),
            )
