from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from kiwoom_api import KiwoomDataClient
from us_data import get_us_daily_ohlcv

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    market: str
    symbol: str
    name: str
    date: str
    close: float
    low: float
    high: float
    ma120: float
    ma200: float
    cond_close_le_120: bool
    cond_close_le_200: bool
    cond_touch_120: bool
    cond_touch_200: bool


class StockScanner:
    def __init__(self, stocks_csv: str = "stocks.csv") -> None:
        self.stocks_csv = Path(stocks_csv)
        self.kiwoom = KiwoomDataClient()

    def _read_stocks(self) -> pd.DataFrame:
        if not self.stocks_csv.exists():
            raise FileNotFoundError(f"종목 파일이 없습니다: {self.stocks_csv}")

        df = pd.read_csv(self.stocks_csv)
        required = ["market", "symbol", "name"]
        if any(col not in df.columns for col in required):
            raise ValueError(f"stocks.csv에는 다음 컬럼이 필요합니다: {required}")

        df["market"] = df["market"].astype(str).str.upper().str.strip()
        df["symbol"] = df["symbol"].astype(str).str.strip()
        df["name"] = df["name"].astype(str).str.strip()
        return df

    @staticmethod
    def _calc_conditions(df: pd.DataFrame) -> Tuple[bool, bool, bool, bool]:
        row = df.iloc[-1]
        cond1 = row["close"] <= row["ma120"]
        cond2 = row["close"] <= row["ma200"]
        cond3 = row["low"] <= row["ma120"] <= row["high"]
        cond4 = row["low"] <= row["ma200"] <= row["high"]
        return bool(cond1), bool(cond2), bool(cond3), bool(cond4)

    def _fetch_by_market(self, market: str, symbol: str) -> pd.DataFrame:
        if market == "KR":
            return self.kiwoom.get_daily_ohlcv(symbol, count=260)
        if market == "US":
            return get_us_daily_ohlcv(symbol, period="2y").tail(260)
        raise ValueError(f"지원하지 않는 market 값입니다: {market}")

    def run_scan(self) -> Tuple[List[ScanResult], str]:
        stocks = self._read_stocks()
        results: List[ScanResult] = []

        for _, item in stocks.iterrows():
            market, symbol, name = item["market"], item["symbol"], item["name"]
            try:
                daily = self._fetch_by_market(market, symbol)
                if len(daily) < 200:
                    logger.warning("데이터 부족으로 스킵: %s/%s (%s일)", market, symbol, len(daily))
                    continue

                daily = daily.copy()
                daily["ma120"] = daily["close"].rolling(120).mean()
                daily["ma200"] = daily["close"].rolling(200).mean()
                daily = daily.dropna(subset=["ma120", "ma200"])
                if daily.empty:
                    continue

                cond1, cond2, cond3, cond4 = self._calc_conditions(daily)
                if cond1 or cond2 or cond3 or cond4:
                    last = daily.iloc[-1]
                    results.append(
                        ScanResult(
                            market=market,
                            symbol=symbol,
                            name=name,
                            date=last["date"].strftime("%Y-%m-%d"),
                            close=float(last["close"]),
                            low=float(last["low"]),
                            high=float(last["high"]),
                            ma120=float(last["ma120"]),
                            ma200=float(last["ma200"]),
                            cond_close_le_120=cond1,
                            cond_close_le_200=cond2,
                            cond_touch_120=cond3,
                            cond_touch_200=cond4,
                        )
                    )
                    logger.info("조건 충족: %s/%s", market, symbol)

            except Exception as exc:  # noqa: BLE001
                logger.exception("스캔 중 오류: %s/%s - %s", market, symbol, exc)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"scan_result_{timestamp}.csv"
        self._save_results(results, out_path)
        return results, out_path

    @staticmethod
    def _save_results(results: List[ScanResult], out_path: str) -> None:
        df = pd.DataFrame([r.__dict__ for r in results])
        if df.empty:
            df = pd.DataFrame(
                columns=[
                    "market",
                    "symbol",
                    "name",
                    "date",
                    "close",
                    "low",
                    "high",
                    "ma120",
                    "ma200",
                    "cond_close_le_120",
                    "cond_close_le_200",
                    "cond_touch_120",
                    "cond_touch_200",
                ]
            )
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        logger.info("결과 CSV 저장 완료: %s", out_path)
