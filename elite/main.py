import asyncio
from scanners.soccer_scanner import scan as soccer_scan
from scanners.basketball_scanner import scan as basketball_scan
from alerts.telegram import send_telegram
from config import CONFIDENCE_ALERT_MIN, POLL_SECONDS

async def run():
    while True:
        soccer_picks = await soccer_scan()
        basketball_picks = await basketball_scan()
        for pick in soccer_picks + basketball_picks:
            if pick["confidence_score"] >= CONFIDENCE_ALERT_MIN:
                msg=f"🟢 {pick['league']} - {pick['home']} vs {pick['away']}\nPick: {pick['pick_type']}\nOdds: {pick['best_odds']}\nConfidence: {pick['confidence_score']}\nReasons: {', '.join(pick['reasons'])}"
                send_telegram(msg)
        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    asyncio.run(run())
