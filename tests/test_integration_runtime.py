"""Tests for pdca_cli.integration_runtime — runtime helpers for integration commands."""

import pytest

from pdca_cli.integration_runtime import (
    invoke_separator_for_integration,
    resolve_integration_options,
    with_integration_setting,
)


# ---------------------------------------------------------------------------
# Dummy integration class used throughout the tests
# ---------------------------------------------------------------------------

class DummyIntegration:
    """Minimal integration-like object for testing."""
    key = "dummy"

    @staticmethod
    def effective_invoke_separator(parsed_options):
        if parsed_options and parsed_options.get("separator"):
            return parsed_options["separator"]
        return "."


# ---------------------------------------------------------------------------
# resolve_integration_options
# ---------------------------------------------------------------------------

class TestResolveIntegrationOptions:
    """Tests for resolve_integration_options."""

    def test_raw_options_provided_parsed_immediately(self):
        """When raw_options is provided, parse it and return both raw and parsed."""
        def parse_opts(_integration, raw):
            return {"key": raw}

        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, {}, "dummy", "--flag",
            parse_options=parse_opts,
        )
        assert raw == "--flag"
        assert parsed == {"key": "--flag"}

    def test_no_raw_options_no_stored_setting(self):
        """When neither raw_options nor stored setting exists, return None, None."""
        def parse_opts(_integration, _raw):
            return None  # should not be called

        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, {}, "dummy", None,
            parse_options=parse_opts,
        )
        assert raw is None
        assert parsed is None

    def test_stored_raw_and_parsed_from_state(self):
        """When raw_options is None, read stored raw and parsed from state."""
        def parse_opts(_integration, _raw):
            return None  # should not be called

        state = {
            "integration_settings": {
                "dummy": {
                    "raw_options": "--stored",
                    "parsed_options": {"stored": True},
                }
            }
        }
        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, state, "dummy", None,
            parse_options=parse_opts,
        )
        assert raw == "--stored"
        assert parsed == {"stored": True}

    def test_stored_raw_no_parsed_triggers_parse(self):
        """When state has raw but no parsed, parse the stored raw."""
        def parse_opts(_integration, raw):
            return {"reparsed": raw}

        state = {
            "integration_settings": {
                "dummy": {
                    "raw_options": "--stored",
                }
            }
        }
        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, state, "dummy", None,
            parse_options=parse_opts,
        )
        assert raw == "--stored"
        assert parsed == {"reparsed": "--stored"}

    def test_stored_raw_is_none_string_coerced_to_none(self):
        """When stored raw_options is not a string, coerce to None."""
        def parse_opts(_integration, _raw):
            return None  # should not be called

        state = {
            "integration_settings": {
                "dummy": {
                    "raw_options": 123,
                }
            }
        }
        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, state, "dummy", None,
            parse_options=parse_opts,
        )
        assert raw is None
        assert parsed is None

    def test_stored_parsed_is_empty_dict_returns_none(self):
        """When stored parsed_options is an empty dict, return None for parsed."""
        def parse_opts(_integration, _raw):
            return None  # should not be called

        state = {
            "integration_settings": {
                "dummy": {
                    "raw_options": "--stored",
                    "parsed_options": {},
                }
            }
        }
        integration = DummyIntegration()
        raw, parsed = resolve_integration_options(
            integration, state, "dummy", None,
            parse_options=parse_opts,
        )
        assert raw == "--stored"
        assert parsed is None


# ---------------------------------------------------------------------------
# with_integration_setting
# ---------------------------------------------------------------------------

class TestWithIntegrationSetting:
    """Tests for with_integration_setting."""

    def test_adds_new_integration_key(self):
        integration = DummyIntegration()
        result = with_integration_setting(
            {}, "dummy", integration,
            script_type="sh",
        )
        assert "dummy" in result
        assert result["dummy"]["script"] == "sh"
        assert result["dummy"]["invoke_separator"] == "."

    def test_updates_existing_integration_key(self):
        state = {"integration_settings": {"dummy": {"script": "ps"}}}
        integration = DummyIntegration()
        result = with_integration_setting(
            state, "dummy", integration,
            script_type="sh",
        )
        assert result["dummy"]["script"] == "sh"

    def test_sets_raw_options(self):
        integration = DummyIntegration()
        result = with_integration_setting(
            {}, "dummy", integration,
            raw_options="--flag",
        )
        assert result["dummy"]["raw_options"] == "--flag"

    def test_sets_parsed_options(self):
        integration = DummyIntegration()
        result = with_integration_setting(
            {}, "dummy", integration,
            parsed_options={"skills": True},
        )
        assert result["dummy"]["parsed_options"] == {"skills": True}

    def test_raw_options_none_removes_existing_empty_raw(self):
        state = {"integration_settings": {"dummy": {"raw_options": ""}}}
        integration = DummyIntegration()
        result = with_integration_setting(
            state, "dummy", integration,
            raw_options=None,
        )
        assert "raw_options" not in result["dummy"]

    def test_raw_options_provided_clears_parsed(self):
        state = {"integration_settings": {"dummy": {"parsed_options": {"old": True}}}}
        integration = DummyIntegration()
        result = with_integration_setting(
            state, "dummy", integration,
            raw_options="--new",
        )
        assert "parsed_options" not in result["dummy"]
        assert result["dummy"]["raw_options"] == "--new"

    def test_parsed_options_overrides_invoke_separator(self):
        integration = DummyIntegration()
        result = with_integration_setting(
            {}, "dummy", integration,
            parsed_options={"separator": "-"},
        )
        assert result["dummy"]["invoke_separator"] == "-"

    def test_default_invoke_separator(self):
        integration = DummyIntegration()
        result = with_integration_setting({}, "dummy", integration)
        assert result["dummy"]["invoke_separator"] == "."

    def test_returns_new_settings_dict(self):
        """Should return a new dict, not modify the input."""
        state = {"integration_settings": {"other": {"script": "sh"}}}
        integration = DummyIntegration()
        result = with_integration_setting(
            state, "dummy", integration, script_type="sh",
        )
        # original state should be unchanged
        assert "dummy" not in state["integration_settings"]


# ---------------------------------------------------------------------------
# invoke_separator_for_integration
# ---------------------------------------------------------------------------

class TestInvokeSeparatorForIntegration:
    """Tests for invoke_separator_for_integration."""

    def test_uses_parsed_options_when_provided(self):
        integration = DummyIntegration()
        sep = invoke_separator_for_integration(
            integration, {}, "dummy",
            parsed_options={"separator": "-"},
        )
        assert sep == "-"

    def test_falls_back_to_stored_separator(self):
        state = {
            "integration_settings": {
                "dummy": {"invoke_separator": "/"}
            }
        }
        integration = DummyIntegration()
        sep = invoke_separator_for_integration(
            integration, state, "dummy",
        )
        assert sep == "/"

    def test_stored_separator_takes_priority(self):
        """stored invoke_separator takes priority over parsed_options."""
        state = {
            "integration_settings": {
                "dummy": {
                    "invoke_separator": "/",
                    "parsed_options": {"separator": "-"},
                }
            }
        }
        integration = DummyIntegration()
        sep = invoke_separator_for_integration(
            integration, state, "dummy",
        )
        # stored_separator is checked first, before parsed_options
        assert sep == "/"

    def test_defaults_to_integration_default(self):
        integration = DummyIntegration()
        sep = invoke_separator_for_integration(
            integration, {}, "dummy",
        )
        assert sep == "."

    def test_empty_stored_separator_ignored(self):
        state = {
            "integration_settings": {
                "dummy": {"invoke_separator": ""}
            }
        }
        integration = DummyIntegration()
        sep = invoke_separator_for_integration(
            integration, state, "dummy",
        )
        assert sep == "."
