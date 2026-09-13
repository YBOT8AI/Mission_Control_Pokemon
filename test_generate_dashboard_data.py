"""Tests for generate_dashboard_data.py pure helpers (stdlib unittest)."""

import unittest
from unittest import mock

import generate_dashboard_data as gdd


class TestRun(unittest.TestCase):
    def test_success_returns_stdout_and_true(self):
        with mock.patch.object(gdd.subprocess, "run") as r:
            r.return_value = mock.Mock(stdout="  output  \n", returncode=0)
            out, ok = gdd.run("echo hi")
        self.assertEqual(out, "output")
        self.assertTrue(ok)

    def test_failure_returns_stdout_and_false(self):
        with mock.patch.object(gdd.subprocess, "run") as r:
            r.return_value = mock.Mock(stdout="err", returncode=1)
            out, ok = gdd.run("false")
        self.assertEqual(out, "err")
        self.assertFalse(ok)

    def test_exception_returns_message_and_false(self):
        with mock.patch.object(gdd.subprocess, "run", side_effect=Exception("boom")):
            out, ok = gdd.run("bad")
        self.assertEqual(out, "boom")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
