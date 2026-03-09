from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def get_us_daily_ohlcv(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Fetch US daily OHLCV using yfinance.

    Returns columns: date, open, high, low, close, volume
    """
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError(
            "yfinance가 설치되어 있지 않습니다. `pip install yfinance` 후 다시 시도하세요."
        ) from exc

    try:
        hist = yf.Ticker(ticker).history(period=period, interval="1d", auto_adjust=False)
    except Exception as exc:  # noqa: BLE001
        logger.exception("미국 종목 데이터 조회 실패: %s", ticker)
        raise RuntimeError(f"미국 종목 데이터 조회 실패: {ticker}") from exc

    if hist is None or hist.empty:
        raise RuntimeError(f"미국 종목 데이터가 비어 있습니다: {ticker}")

    hist = hist.reset_index()
    date_col = "Date" if "Date" in hist.columns else "Datetime"
    required = [date_col, "Open", "High", "Low", "Close", "Volume"]
    if any(col not in hist.columns for col in required):
        raise RuntimeError(f"yfinance 데이터 포맷이 예상과 다릅니다: {ticker}")

    out = pd.DataFrame(
        {
            "date": pd.to_datetime(hist[date_col]).dt.tz_localize(None),
            "open": pd.to_numeric(hist["Open"], errors="coerce"),
            "high": pd.to_numeric(hist["High"], errors="coerce"),
            "low": pd.to_numeric(hist["Low"], errors="coerce"),
            "close": pd.to_numeric(hist["Close"], errors="coerce"),
            "volume": pd.to_numeric(hist["Volume"], errors="coerce"),
        }
    )
    out = out.dropna(subset=["date", "open", "high", "low", "close"])
    out = out.sort_values("date").reset_index(drop=True)
    return out
