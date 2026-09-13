"""Tests for Mission Control pure logic (stdlib unittest — no external deps)."""

import unittest
from unittest import mock
from datetime import datetime, timezone, timedelta

import fetch_market_data as fmd

HKT = timezone(timedelta(hours=8))


class TestParseRssDate(unittest.TestCase):
    def test_empty_returns_none(self):
        self.assertIsNone(fmd.parse_rss_date(""))
        self.assertIsNone(fmd.parse_rss_date(None))

    def test_parses_rfc822_date(self):
        # Sun, 13 Sep 2026 00:00:00 GMT
        out = fmd.parse_rss_date("Sun, 13 Sep 2026 00:00:00 GMT")
        self.assertIsNotNone(out)
        # Converted to HKT => +8h
        self.assertIn("2026-09-13T08:00:00", out)

    def test_invalid_returns_none(self):
        self.assertIsNone(fmd.parse_rss_date("not a date"))


class TestFetchJson(unittest.TestCase):
    def test_returns_dict_on_valid_json(self):
        body = b'{"rates": {"HKD": 7.8}}'
        with mock.patch.object(fmd.urllib.request, "urlopen", return_value=mock.Mock(
            read=lambda: body, __enter__=lambda s: s, __exit__=lambda *a: None,
        )):
            self.assertEqual(fmd.fetch_json("http://x"), {"rates": {"HKD": 7.8}})

    def test_returns_empty_dict_on_error(self):
        with mock.patch.object(fmd.urllib.request, "urlopen", side_effect=Exception("boom")):
            self.assertEqual(fmd.fetch_json("http://x"), {})

    def test_returns_empty_dict_on_bad_json(self):
        with mock.patch.object(fmd.urllib.request, "urlopen", return_value=mock.Mock(
            read=lambda: b"not json", __enter__=lambda s: s, __exit__=lambda *a: None,
        )):
            self.assertEqual(fmd.fetch_json("http://x"), {})


class TestFetchRss(unittest.TestCase):
    def test_parses_items(self):
        xml = b"""<?xml version="1.0"?>
        <rss><channel>
          <item><title>Hello World</title><link>http://a</link><pubDate>Sun, 13 Sep 2026 00:00:00 GMT</pubDate></item>
          <item><title></title></item>
        </channel></rss>"""
        with mock.patch.object(fmd.urllib.request, "urlopen", return_value=mock.Mock(
            read=lambda: xml, __enter__=lambda s: s, __exit__=lambda *a: None,
        )):
            items = fmd.fetch_rss("http://x")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Hello World")
        self.assertEqual(items[0]["link"], "http://a")

    def test_returns_empty_list_on_error(self):
        with mock.patch.object(fmd.urllib.request, "urlopen", side_effect=Exception("boom")):
            self.assertEqual(fmd.fetch_rss("http://x"), [])


class TestFetchStock(unittest.TestCase):
    def test_returns_price_and_change(self):
        fake = mock.Mock()
        fake.fast_info.last_price = 110
        fake.fast_info.regular_market_previous_close = 100
        yf_mod = mock.Mock()
        yf_mod.Ticker.return_value = fake
        with mock.patch.dict("sys.modules", {"yfinance": yf_mod}):
            out = fmd.fetch_stock("VOO")
        self.assertEqual(out["price"], 110)
        self.assertAlmostEqual(out["changePct"], 10.0)

    def test_returns_none_on_error(self):
        yf_mod = mock.Mock()
        yf_mod.Ticker.side_effect = Exception("boom")
        with mock.patch.dict("sys.modules", {"yfinance": yf_mod}):
            self.assertIsNone(fmd.fetch_stock("VOO"))


if __name__ == "__main__":
    unittest.main()
