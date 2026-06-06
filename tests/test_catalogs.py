"""Tests for pdca_cli.catalogs — CatalogEntry and CatalogStackBase."""

from pathlib import Path

import pytest
import yaml

from pdca_cli.catalogs import CatalogEntry, CatalogStackBase


class TestCatalogEntry:
    """CatalogEntry dataclass tests."""

    def test_create_minimal_entry(self):
        entry = CatalogEntry(url="https://example.com", name="test", priority=1, install_allowed=True)
        assert entry.url == "https://example.com"
        assert entry.name == "test"
        assert entry.priority == 1
        assert entry.install_allowed is True
        assert entry.description == ""

    def test_create_entry_with_description(self):
        entry = CatalogEntry(
            url="https://example.com",
            name="test",
            priority=2,
            install_allowed=False,
            description="A test catalog",
        )
        assert entry.description == "A test catalog"

    def test_entry_equality(self):
        e1 = CatalogEntry(url="https://a.com", name="a", priority=1, install_allowed=True)
        e2 = CatalogEntry(url="https://a.com", name="a", priority=1, install_allowed=True)
        assert e1 == e2

    def test_entry_inequality(self):
        e1 = CatalogEntry(url="https://a.com", name="a", priority=1, install_allowed=True)
        e2 = CatalogEntry(url="https://b.com", name="b", priority=2, install_allowed=False)
        assert e1 != e2


class ConcreteCatalog(CatalogStackBase):
    """Concrete subclass for testing CatalogStackBase."""
    CONFIG_FILENAME = "test-catalog.yml"


class TestCatalogStackBaseURLValidation:
    """Tests for _validate_catalog_url."""

    def test_accepts_https_url(self):
        ConcreteCatalog._validate_catalog_url("https://example.com/catalog")

    def test_accepts_http_localhost(self):
        ConcreteCatalog._validate_catalog_url("http://localhost:8080/catalog")

    def test_accepts_http_127_0_0_1(self):
        ConcreteCatalog._validate_catalog_url("http://127.0.0.1/catalog")

    def test_accepts_http_ipv6_localhost(self):
        ConcreteCatalog._validate_catalog_url("http://[::1]/catalog")

    def test_rejects_http_non_localhost(self):
        with pytest.raises(ValueError, match="must use HTTPS"):
            ConcreteCatalog._validate_catalog_url("http://example.com/catalog")

    def test_rejects_ftp_url(self):
        with pytest.raises(ValueError, match="must use HTTPS"):
            ConcreteCatalog._validate_catalog_url("ftp://example.com/catalog")

    def test_rejects_empty_url(self):
        # Empty string fails HTTPS check first (scheme is empty, not https)
        with pytest.raises(ValueError, match="must use HTTPS"):
            ConcreteCatalog._validate_catalog_url("")

    def test_rejects_url_without_host(self):
        with pytest.raises(ValueError, match="must be a valid URL with a host"):
            ConcreteCatalog._validate_catalog_url("https:///path")

    def test_rejects_url_with_no_scheme(self):
        # URL with no scheme — urlparse may treat "example.com" as path or netloc
        # depending on Python version; just verify it raises ValueError
        with pytest.raises(ValueError):
            ConcreteCatalog._validate_catalog_url("example.com")


class TestCatalogStackBaseLoadConfig:
    """Tests for _load_catalog_config."""

    def test_returns_none_when_file_missing(self, tmp_path):
        catalog = ConcreteCatalog()
        config_path = tmp_path / "nonexistent.yml"
        result = catalog._load_catalog_config(config_path)
        assert result is None

    def test_loads_valid_single_entry(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://example.com", "name": "test-cat", "priority": 1, "install_allowed": True}
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result is not None
        assert len(result) == 1
        assert result[0].url == "https://example.com"
        assert result[0].name == "test-cat"
        assert result[0].priority == 1
        assert result[0].install_allowed is True

    def test_loads_multiple_entries_sorted_by_priority(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://b.com", "name": "b", "priority": 10},
                    {"url": "https://a.com", "name": "a", "priority": 1},
                    {"url": "https://c.com", "name": "c", "priority": 5},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert len(result) == 3
        priorities = [e.priority for e in result]
        assert priorities == [1, 5, 10]

    def test_empty_catalogs_list_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text("catalogs: []\n", encoding="utf-8")
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="contains no 'catalogs' entries"):
            catalog._load_catalog_config(config_path)

    def test_missing_catalogs_key_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text("other: value\n", encoding="utf-8")
        catalog = ConcreteCatalog()
        # catalogs key is missing entirely → data.get("catalogs", []) returns []
        # which triggers "contains no 'catalogs' entries"
        with pytest.raises(ValueError, match="contains no 'catalogs' entries"):
            catalog._load_catalog_config(config_path)

    def test_root_not_a_dict_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text("- item1\n- item2\n", encoding="utf-8")
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="expected a YAML mapping"):
            catalog._load_catalog_config(config_path)

    def test_all_entries_skipped_no_url_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"name": "no-url-1", "priority": 1},
                    {"name": "no-url-2", "priority": 2},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="none have valid URLs"):
            catalog._load_catalog_config(config_path)

    def test_skips_entries_with_empty_url(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "", "name": "empty-url", "priority": 1},
                    {"url": "https://valid.com", "name": "valid", "priority": 2},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert len(result) == 1
        assert result[0].url == "https://valid.com"

    def test_rejects_invalid_url_in_entry(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "http://bad.example.com", "name": "bad", "priority": 1},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="Invalid catalog URL"):
            catalog._load_catalog_config(config_path)

    def test_entry_not_a_dict_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({"catalogs": ["not-a-dict"]}),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="expected a mapping"):
            catalog._load_catalog_config(config_path)

    def test_default_priority_uses_index(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a"},
                    {"url": "https://b.com", "name": "b"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].priority == 1  # index 0 + 1
        assert result[1].priority == 2  # index 1 + 1

    def test_bool_priority_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "priority": True},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="Invalid priority"):
            catalog._load_catalog_config(config_path)

    def test_string_priority_not_convertible_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "priority": "high"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="Invalid priority"):
            catalog._load_catalog_config(config_path)

    def test_string_priority_convertible_to_int(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "priority": "42"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].priority == 42

    def test_install_allowed_string_true(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "install_allowed": "true"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].install_allowed is True

    def test_install_allowed_string_yes(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "install_allowed": "yes"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].install_allowed is True

    def test_install_allowed_string_false(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "install_allowed": "false"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].install_allowed is False

    def test_auto_name_generation(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "priority": 1},
                    {"url": "https://b.com", "priority": 2},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].name == "catalog-1"
        assert result[1].name == "catalog-2"

    def test_description_field(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": "a", "description": "My catalog"},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].description == "My catalog"

    def test_null_yaml_root_treated_as_empty(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text("", encoding="utf-8")
        catalog = ConcreteCatalog()
        # Empty file: yaml.safe_load("") returns None, converted to {}
        # data.get("catalogs", []) returns [] → "contains no 'catalogs' entries"
        with pytest.raises(ValueError, match="contains no 'catalogs' entries"):
            catalog._load_catalog_config(config_path)

    def test_malformed_yaml_raises(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text("{invalid: [yaml", encoding="utf-8")
        catalog = ConcreteCatalog()
        with pytest.raises(ValueError, match="Failed to read catalog config"):
            catalog._load_catalog_config(config_path)

    def test_none_name_becomes_empty_auto_named(self, tmp_path):
        config_path = tmp_path / "catalog.yml"
        config_path.write_text(
            yaml.dump({
                "catalogs": [
                    {"url": "https://a.com", "name": None},
                ]
            }),
            encoding="utf-8",
        )
        catalog = ConcreteCatalog()
        result = catalog._load_catalog_config(config_path)
        assert result[0].name == "catalog-1"


class TestCatalogStackBaseErrorMethods:
    """Tests for _error and _validation_error factory methods."""

    def test_error_creates_correct_type(self):
        err = ConcreteCatalog._error("test error")
        assert isinstance(err, ValueError)
        assert str(err) == "test error"

    def test_validation_error_creates_correct_type(self):
        err = ConcreteCatalog._validation_error("validation error")
        assert isinstance(err, ValueError)
        assert str(err) == "validation error"


class TestCatalogStackBaseEntryMethod:
    """Tests for _entry factory method."""

    def test_entry_creates_catalog_entry(self):
        entry = ConcreteCatalog._entry(
            url="https://example.com",
            name="test",
            priority=1,
            install_allowed=True,
            description="desc",
        )
        assert isinstance(entry, CatalogEntry)
        assert entry.url == "https://example.com"
        assert entry.name == "test"
        assert entry.priority == 1
        assert entry.install_allowed is True
        assert entry.description == "desc"

    def test_entry_default_description(self):
        entry = ConcreteCatalog._entry(
            url="https://example.com",
            name="test",
            priority=1,
            install_allowed=True,
        )
        assert entry.description == ""
