"""Tests for pdca_cli._console — StepTracker and console helpers."""

from io import StringIO

import pytest
from rich.console import Console

from pdca_cli._console import StepTracker


class TestStepTracker:
    """Tests for the StepTracker class."""

    def test_initialization(self):
        tracker = StepTracker("Test Title")
        assert tracker.title == "Test Title"
        assert tracker.steps == []

    def test_add_step(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["key"] == "step1"
        assert tracker.steps[0]["label"] == "First Step"
        assert tracker.steps[0]["status"] == "pending"
        assert tracker.steps[0]["detail"] == ""

    def test_add_duplicate_key_is_idempotent(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.add("step1", "Duplicate")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["label"] == "First Step"

    def test_start_step(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.start("step1", "running now")
        assert tracker.steps[0]["status"] == "running"
        assert tracker.steps[0]["detail"] == "running now"

    def test_complete_step(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.complete("step1", "done")
        assert tracker.steps[0]["status"] == "done"
        assert tracker.steps[0]["detail"] == "done"

    def test_error_step(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.error("step1", "failed")
        assert tracker.steps[0]["status"] == "error"
        assert tracker.steps[0]["detail"] == "failed"

    def test_skip_step(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.skip("step1", "skipped")
        assert tracker.steps[0]["status"] == "skipped"
        assert tracker.steps[0]["detail"] == "skipped"

    def test_update_unknown_key_adds_it(self):
        tracker = StepTracker("Test")
        tracker.start("unknown_step", "auto-added")
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["key"] == "unknown_step"
        assert tracker.steps[0]["status"] == "running"

    def test_update_preserves_existing_detail_when_empty(self):
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        tracker.complete("step1", "done")
        # Update without detail should keep old detail
        tracker.start("step1", "")
        assert tracker.steps[0]["detail"] == "done"

    def _render_to_str(self, tracker):
        """Render a StepTracker tree to a plain string via Rich Console."""
        buf = StringIO()
        console = Console(file=buf, force_terminal=False, color_system=None)
        console.print(tracker.render())
        return buf.getvalue()

    def test_render_produces_tree(self):
        tracker = StepTracker("My Title")
        tracker.add("a", "Task A")
        tracker.complete("a", "finished")
        tracker.add("b", "Task B")
        tracker.start("b", "in progress")
        rendered = self._render_to_str(tracker)
        assert "My Title" in rendered
        assert "Task A" in rendered
        assert "Task B" in rendered

    def test_render_pending_step(self):
        tracker = StepTracker("Test")
        tracker.add("pending", "Pending Task")
        rendered = self._render_to_str(tracker)
        assert "Pending Task" in rendered

    def test_render_skipped_step(self):
        tracker = StepTracker("Test")
        tracker.add("skip", "Skipped Task")
        tracker.skip("skip", "reason")
        rendered = self._render_to_str(tracker)
        assert "Skipped Task" in rendered
        assert "reason" in rendered

    def test_render_error_step(self):
        tracker = StepTracker("Test")
        tracker.add("err", "Error Task")
        tracker.error("err", "something broke")
        rendered = self._render_to_str(tracker)
        assert "Error Task" in rendered
        assert "something broke" in rendered

    def test_attach_refresh_callback(self):
        tracker = StepTracker("Test")
        called = []

        def refresh():
            called.append(True)

        tracker.attach_refresh(refresh)
        tracker.add("step1", "Step")
        assert len(called) == 1

    def test_refresh_callback_exception_is_silent(self):
        tracker = StepTracker("Test")

        def bad_refresh():
            raise RuntimeError("boom")

        tracker.attach_refresh(bad_refresh)
        # Should not raise
        tracker.add("step1", "Step")

    def test_multiple_steps_status_order(self):
        tracker = StepTracker("Test")
        tracker.add("a", "A")
        tracker.add("b", "B")
        tracker.add("c", "C")
        tracker.complete("a")
        tracker.start("b")
        tracker.error("c")
        # status_order defines sorting
        assert tracker.status_order["pending"] == 0
        assert tracker.status_order["running"] == 1
        assert tracker.status_order["done"] == 2
        assert tracker.status_order["error"] == 3
        assert tracker.status_order["skipped"] == 4
