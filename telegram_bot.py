from __future__ import annotations

import logging
import os
from typing import List

from scanner import ScanResult, StockScanner

logger = logging.getLogger(__name__)


def _format_message(results: List[ScanResult], csv_path: str) -> str:
    if not results:
        return f"[스캔 완료] 조건을 만족한 종목이 없습니다.\nCSV: {csv_path}"

    lines = [f"[스캔 완료] 조건 충족 종목 {len(results)}개", f"CSV: {csv_path}", ""]
    for r in results:
        lines.append(
            (
                f"- [{r.market}] {r.symbol} ({r.name}) | {r.date}\n"
                f"  close={r.close:.2f}, low={r.low:.2f}, high={r.high:.2f}\n"
                f"  ma120={r.ma120:.2f}, ma200={r.ma200:.2f}\n"
                f"  c1={r.cond_close_le_120}, c2={r.cond_close_le_200}, "
                f"c3={r.cond_touch_120}, c4={r.cond_touch_200}"
            )
        )
    return "\n".join(lines)


async def run_bot() -> None:
    """Run Telegram bot. Required env vars:

    - TELEGRAM_BOT_TOKEN: bot token
    - TELEGRAM_CHAT_ID: chat id for push target
    - STOCKS_CSV (optional): default stocks.csv
    """
    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes
    except ImportError as exc:
        raise RuntimeError(
            "python-telegram-bot가 설치되어 있지 않습니다. `pip install python-telegram-bot` 후 다시 시도하세요."
        ) from exc

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    stocks_csv = os.getenv("STOCKS_CSV", "stocks.csv")

    if not token or not chat_id:
        raise RuntimeError("TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 환경변수를 설정하세요.")

    scanner = StockScanner(stocks_csv=stocks_csv)

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("안녕하세요. /scan 명령으로 종목 스캔을 실행하세요.")

    async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("스캔을 시작합니다. 잠시만 기다려주세요...")
        try:
            results, csv_path = scanner.run_scan()
            message = _format_message(results, csv_path)
            await context.bot.send_message(chat_id=chat_id, text=message)
            await update.message.reply_text(f"스캔 완료. 결과 파일: {csv_path}")
        except Exception as exc:  # noqa: BLE001
            logger.exception("/scan 처리 오류: %s", exc)
            await update.message.reply_text(f"스캔 중 오류가 발생했습니다: {exc}")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan))

    logger.info("텔레그램 봇 시작")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()
