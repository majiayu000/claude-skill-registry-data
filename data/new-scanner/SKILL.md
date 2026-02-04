---
name: "new-scanner"
description: "Use this skill ONLY when creating a new data scanner (e.g., Twitter scanner, Bloomberg scanner). Do not use for agents or strategies."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Scanner files go in `src/alpacalyzer/scanners/{name}_scanner.py`
- Tests go in `tests/test_{name}_scanner.py`
- Scanners discover trading opportunities from external data sources

# Template Placeholders

- `<scanner>` - lowercase with underscores (e.g., `twitter_scanner`, `bloomberg_scanner`)
- `<Scanner>` - PascalCase (e.g., `TwitterScanner`, `BloombergScanner`)

# Procedural Steps

## 1. Review Existing Scanner Patterns

Before creating a new scanner, understand the established patterns:

```bash
# Look at existing scanner implementations
cat src/alpacalyzer/scanners/reddit_scanner.py
cat src/alpacalyzer/scanners/finviz_scanner.py
cat src/alpacalyzer/scanners/social_scanner.py
```

**Key patterns to observe**:

- Scanners return lists of ticker symbols (strings)
- Scanners handle API failures gracefully
- Scanners deduplicate results
- Scanners may cache results to avoid rate limits

## 2. Determine Scanner Protocol (Post-Migration)

**Current state**: Scanners are simple classes with `scan()` methods.

**Migration target** (Phase 4): Scanners will implement a `Scanner` protocol:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Scanner(Protocol):
    """Protocol for opportunity scanners."""

    def scan(self) -> list[str]:
        """Scan for trading opportunities, return ticker symbols."""
        ...
```

**For now**: Create scanners following existing patterns. Protocol will be added during Phase 4 migration.

## 3. Create Scanner File

Location: `src/alpacalyzer/scanners/<scanner>_scanner.py`

**Template structure**:

```python
"""<Scanner> for discovering trading opportunities from <data source>."""

import logging
from typing import Optional

# Import relevant libraries for data source
# Examples: requests, praw (Reddit), tweepy (Twitter), etc.

logger = logging.getLogger(__name__)


class <Scanner>Scanner:
    """
    Scanner that discovers trading opportunities from <data source>.

    Data Source: <URL or API description>
    Rate Limits: <describe rate limits>
    Authentication: <describe if API key needed>
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize <Scanner> scanner.

        Args:
            api_key: Optional API key for <data source>
        """
        self.api_key = api_key
        # Initialize API client if needed
        self._client = None
        if api_key:
            self._client = self._initialize_client(api_key)

    def _initialize_client(self, api_key: str):
        """Initialize API client for <data source>."""
        # Example: return TwitterAPI(api_key)
        pass

    def scan(self) -> list[str]:
        """
        Scan <data source> for trending stocks.

        Returns:
            List of ticker symbols (e.g., ["AAPL", "MSFT", "TSLA"])
        """
        try:
            logger.info("Scanning <data source> for opportunities...")

            # Fetch data from source
            raw_data = self._fetch_data()

            # Extract ticker symbols
            tickers = self._extract_tickers(raw_data)

            # Deduplicate and filter
            tickers = self._deduplicate_and_filter(tickers)

            logger.info(f"Found {len(tickers)} opportunities: {tickers}")
            return tickers

        except Exception as e:
            logger.error(f"<Scanner> scan failed: {e}")
            return []

    def _fetch_data(self) -> list:
        """
        Fetch raw data from <data source>.

        Returns:
            Raw data from source (format depends on API)
        """
        # Example for REST API:
        # response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        # return response.json()

        # Example for Reddit:
        # subreddit = self._client.subreddit("wallstreetbets")
        # return list(subreddit.hot(limit=100))

        raise NotImplementedError("Implement data fetching logic")

    def _extract_tickers(self, raw_data: list) -> list[str]:
        """
        Extract ticker symbols from raw data.

        Args:
            raw_data: Raw data from data source

        Returns:
            List of ticker symbols
        """
        tickers = []

        # Example: Extract tickers from text using regex
        # import re
        # ticker_pattern = r'\b[A-Z]{1,5}\b'
        # for item in raw_data:
        #     text = item.get('text', '')
        #     found = re.findall(ticker_pattern, text)
        #     tickers.extend(found)

        raise NotImplementedError("Implement ticker extraction logic")

    def _deduplicate_and_filter(self, tickers: list[str]) -> list[str]:
        """
        Remove duplicates and filter invalid tickers.

        Args:
            tickers: Raw list of ticker symbols

        Returns:
            Cleaned list of unique, valid tickers
        """
        # Remove duplicates
        unique_tickers = list(set(tickers))

        # Filter invalid (e.g., too short, too long, common words)
        invalid_symbols = {"A", "I", "DD", "OR", "AT", "IT", "BE", "BY", "CEO", "WSB"}
        filtered = [t for t in unique_tickers if t not in invalid_symbols]

        # Optional: Validate against known ticker list
        # filtered = [t for t in filtered if self._is_valid_ticker(t)]

        return filtered[:20]  # Limit to top 20

    def _is_valid_ticker(self, ticker: str) -> bool:
        """
        Validate ticker symbol.

        Args:
            ticker: Ticker symbol to validate

        Returns:
            True if valid ticker
        """
        # Example: Check ticker exists in yfinance or Alpaca
        # try:
        #     import yfinance as yf
        #     stock = yf.Ticker(ticker)
        #     info = stock.info
        #     return 'regularMarketPrice' in info
        # except:
        #     return False
        return True
```

## 4. Register Scanner

Edit `src/alpacalyzer/scanners/__init__.py`:

```python
from alpacalyzer.scanners.<scanner>_scanner import <Scanner>Scanner

__all__ = [
    # ... existing scanners ...
    "<Scanner>Scanner",
]
```

## 5. Integrate with Opportunity Pipeline

**Current integration** (pre-migration):

Edit `src/alpacalyzer/cli.py` or wherever scanners are called:

```python
from alpacalyzer.scanners.<scanner>_scanner import <Scanner>Scanner

# In the scanning function:
<scanner>_scanner = <Scanner>Scanner(api_key=os.getenv("<API_KEY_ENV_VAR>"))
<scanner>_results = <scanner>_scanner.scan()
```

**Future integration** (Phase 4 migration):

Scanners will be registered in `ScannerRegistry` and called by `OpportunityAggregator`. See `migration_plan.md` Phase 4 for details.

## 6. Write Tests

Location: `tests/test_<scanner>_scanner.py`

**Test template**:

```python
"""Tests for <Scanner> scanner."""

from unittest.mock import MagicMock, patch
import pytest

from alpacalyzer.scanners.<scanner>_scanner import <Scanner>Scanner


@pytest.fixture
def mock_<scanner>_data():
    """Mock data from <data source>."""
    return [
        {"text": "Bullish on $AAPL and $MSFT", "score": 100},
        {"text": "$TSLA to the moon 🚀", "score": 85},
        {"text": "Thoughts on $GOOGL?", "score": 50},
    ]


def test_<scanner>_scan_success(mock_<scanner>_data):
    """Test successful scan returns ticker list."""

    scanner = <Scanner>Scanner(api_key="test_key")

    # Mock the data fetching
    with patch.object(scanner, '_fetch_data', return_value=mock_<scanner>_data):
        with patch.object(scanner, '_extract_tickers', return_value=["AAPL", "MSFT", "TSLA", "GOOGL"]):
            tickers = scanner.scan()

    # Should return list of strings
    assert isinstance(tickers, list)
    assert all(isinstance(t, str) for t in tickers)
    assert len(tickers) > 0


def test_<scanner>_scan_handles_api_failure():
    """Test scanner handles API failures gracefully."""

    scanner = <Scanner>Scanner(api_key="test_key")

    # Mock API failure
    with patch.object(scanner, '_fetch_data', side_effect=Exception("API Error")):
        tickers = scanner.scan()

    # Should return empty list, not raise exception
    assert tickers == []


def test_<scanner>_deduplicate():
    """Test scanner removes duplicate tickers."""

    scanner = <Scanner>Scanner()

    # Duplicate tickers
    tickers = ["AAPL", "MSFT", "AAPL", "TSLA", "MSFT", "AAPL"]

    result = scanner._deduplicate_and_filter(tickers)

    # Should have no duplicates
    assert len(result) == len(set(result))
    assert "AAPL" in result
    assert "MSFT" in result
    assert "TSLA" in result


def test_<scanner>_filter_invalid_tickers():
    """Test scanner filters out invalid/common word tickers."""

    scanner = <Scanner>Scanner()

    # Mix of valid and invalid
    tickers = ["AAPL", "I", "MSFT", "A", "CEO", "TSLA", "DD"]

    result = scanner._deduplicate_and_filter(tickers)

    # Should filter out single letters and common words
    assert "AAPL" in result
    assert "MSFT" in result
    assert "TSLA" in result
    assert "I" not in result
    assert "A" not in result
    assert "CEO" not in result


def test_<scanner>_extract_tickers(mock_<scanner>_data):
    """Test ticker extraction from raw data."""

    scanner = <Scanner>Scanner()

    tickers = scanner._extract_tickers(mock_<scanner>_data)

    # Should extract ticker symbols
    assert isinstance(tickers, list)
    # Add specific assertions based on your extraction logic


def test_<scanner>_limits_result_count():
    """Test scanner limits number of returned tickers."""

    scanner = <Scanner>Scanner()

    # Many tickers
    tickers = [f"TICK{i}" for i in range(100)]

    result = scanner._deduplicate_and_filter(tickers)

    # Should limit to reasonable number (e.g., 20)
    assert len(result) <= 20
```

## 7. Add Environment Variables (if needed)

If scanner requires API key, add to `.env.example`:

```bash
# <Scanner> API
<API_KEY_ENV_VAR>=your_api_key_here
```

Document in README.md or AGENTS.md.

## 8. Run Tests and Verify

```bash
# Run new scanner tests
uv run pytest tests/test_<scanner>_scanner.py -v

# Run all scanner tests
uv run pytest tests/test_*_scanner.py

# Integration test (if integrated with CLI)
uv run alpacalyzer --analyze
```

# Reference: Existing Examples

- `src/alpacalyzer/scanners/reddit_scanner.py` - Reddit API integration (PRAW)
- `src/alpacalyzer/scanners/finviz_scanner.py` - Web scraping + fundamental filters
- `src/alpacalyzer/scanners/social_scanner.py` - Multi-source aggregation
- `src/alpacalyzer/scanners/stocktwits_scanner.py` - StockTwits trending API

# Special Considerations

1. **Rate Limiting**: Many APIs have rate limits. Implement retries and backoff strategies.

2. **Caching**: Consider caching scan results for a few minutes to avoid hitting rate limits during testing.

3. **Authentication**: Store API keys in environment variables, never hardcode.

4. **Error Handling**: Scanners should never crash the main application. Always return empty list on failure.

5. **Data Quality**: Filter out obvious spam, bots, and low-quality mentions. Consider confidence scores.

6. **Ticker Validation**: Not all extracted symbols are valid tickers. Validate against known ticker lists or APIs.

7. **Migration Awareness**: During Phase 4 migration, scanners will need to implement the `Scanner` protocol. Keep this in mind for future refactoring.

## Example: Twitter Scanner

For reference, here's a realistic Twitter scanner example:

```python
"""Twitter scanner for discovering trending stocks."""

import logging
import re
import os
from typing import Optional
import tweepy

logger = logging.getLogger(__name__)


class TwitterScanner:
    """Scanner for Twitter trending stocks."""

    def __init__(self):
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            logger.warning("Twitter API token not found")
            self.client = None
        else:
            self.client = tweepy.Client(bearer_token=bearer_token)

    def scan(self) -> list[str]:
        if not self.client:
            return []

        try:
            # Search recent tweets about stocks
            query = "($) -is:retweet lang:en"
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=100,
                tweet_fields=['public_metrics']
            )

            if not tweets.data:
                return []

            # Extract tickers
            tickers = []
            for tweet in tweets.data:
                found = re.findall(r'\$([A-Z]{1,5})\b', tweet.text)
                tickers.extend(found)

            # Deduplicate and filter
            return self._deduplicate_and_filter(tickers)

        except Exception as e:
            logger.error(f"Twitter scan failed: {e}")
            return []

    def _deduplicate_and_filter(self, tickers: list[str]) -> list[str]:
        unique = list(set(tickers))
        invalid = {"I", "A", "CEO", "IPO", "ETF", "WSB"}
        filtered = [t for t in unique if t not in invalid]
        return filtered[:20]
```
