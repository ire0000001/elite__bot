import aiohttp
from ..news_hooks import fetch_newsapi
from ..config import ODDSAPI_KEY, API_FOOTBALL_KEY

async def get_team_form(team):
    return 80  # Placeholder: integrate API-Football for real form

async def get_player_impact(team):
    return 5  # Placeholder: integrate API-Football injuries

async def scan():
    picks=[]
    async with aiohttp.ClientSession() as session:
        url=f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds"
        params={"apiKey":ODDSAPI_KEY,"regions":"uk","markets":"h2h","oddsFormat":"decimal"}
        async with session.get(url,params=params) as r:
            data=await r.json()
            for match in data:
                home=match["home_team"]
                away=match["away_team"]
                odds_list=match["bookmakers"][0]["markets"][0]["outcomes"]
                best_odds=max([o["price"] for o in odds_list])
                pick_type=max(odds_list,key=lambda x:x["price"])["name"]

                news_signals=await fetch_newsapi(home,away)
                form_home=await get_team_form(home)
                form_away=await get_team_form(away)
                player_home=await get_player_impact(home)
                player_away=await get_player_impact(away)

                odds_score=50+(best_odds-1.5)*20
                form_score=form_home-form_away+50
                player_impact=player_home-player_away
                news_boost=len(news_signals)*2

                confidence=min(100,odds_score*0.4+form_score*0.3+player_impact*0.2+news_boost*0.1)

                picks.append({
                    "home":home,
                    "away":away,
                    "league":match["sport_title"],
                    "pick_type":pick_type,
                    "best_odds":best_odds,
                    "confidence_score":round(confidence),
                    "reasons":["Odds data",f"Form:{form_home}-{form_away}",f"Player impact:{player_impact}"]+news_signals
                })
    return picks

