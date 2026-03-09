from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class KiwoomDataClient:
    """Kiwoom OpenAPI+ daily candle client (Windows).

    Requirements (Windows):
    - Kiwoom OpenAPI+ installed
    - 32-bit Python recommended by Kiwoom
    - `pykiwoom` installed
    """

    def __init__(self) -> None:
        self._kiwoom = None
        self._initialized = False

    def _ensure_initialized(self) -> None:
        if self._initialized:
            return

        try:
            from pykiwoom.kiwoom import Kiwoom
        except ImportError as exc:
            raise RuntimeError(
                "pykiwoom이 설치되어 있지 않습니다. `pip install pykiwoom` 후 다시 시도하세요."
            ) from exc

        self._kiwoom = Kiwoom()
        logger.info("키움 OpenAPI+ 로그인 시도")
        self._kiwoom.CommConnect(block=True)
        self._initialized = True
        logger.info("키움 OpenAPI+ 로그인 완료")

    def get_daily_ohlcv(self, code: str, count: int = 250) -> pd.DataFrame:
        """Return daily OHLCV dataframe sorted by date ascending.

        Columns: date, open, high, low, close, volume
        """
        self._ensure_initialized()
        assert self._kiwoom is not None

        try:
            df = self._kiwoom.block_request(
                "opt10081",
                종목코드=code,
                기준일자="",
                수정주가구분=1,
                output="주식일봉차트조회",
                next=0,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("키움 일봉 조회 실패: %s", code)
            raise RuntimeError(f"키움 일봉 조회 실패: {code}") from exc

        if df is None or df.empty:
            raise RuntimeError(f"키움 데이터가 비어 있습니다: {code}")

        rename_map = {
            "일자": "date",
            "시가": "open",
            "고가": "high",
            "저가": "low",
            "현재가": "close",
            "거래량": "volume",
        }
        missing = [k for k in rename_map if k not in df.columns]
        if missing:
            raise RuntimeError(f"키움 데이터 포맷이 예상과 다릅니다. 누락 컬럼: {missing}")

        out = df.rename(columns=rename_map)[list(rename_map.values())].copy()
        out["date"] = pd.to_datetime(out["date"], format="%Y%m%d", errors="coerce")

        for col in ["open", "high", "low", "close", "volume"]:
            out[col] = pd.to_numeric(out[col].astype(str).str.replace(",", ""), errors="coerce").abs()

        out = out.dropna(subset=["date", "open", "high", "low", "close"])
        out = out.sort_values("date").tail(count).reset_index(drop=True)
        return out
