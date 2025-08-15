import aiohttp
from ..news_hooks import fetch_newsapi
from ..config import ODDSAPI_KEY, API_BASKETBALL_KEY

async def get_team_form(team_id):
    url=f"https://api-basketball.p.rapidapi.com/games"
    headers={"X-RapidAPI-Key":API_BASKETBALL_KEY,"X-RapidAPI-Host":"api-basketball.p.rapidapi.com"}
    params={"team":team_id,"season":"2025-2026","last":5}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as r:
            js=await r.json()
            scores=[g["scores"]["home"]["points"]-g["scores"]["away"]["points"] for g in js.get("response",[])]
            return sum(scores)/len(scores) if scores else 50

async def get_player_impact(team_id):
    return 5  # Placeholder: integrate API-Basketball injuries if needed

async def scan():
    picks=[]
    async with aiohttp.ClientSession() as session:
        url=f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
        params={"apiKey":ODDSAPI_KEY,"regions":"us","markets":"h2h","oddsFormat":"decimal"}
        async with session.get(url,params=params) as r:
            data=await r.json()
            for match in data:
                home=match["home_team"]
                away=match["away_team"]
                odds_list=match["bookmakers"][0]["markets"][0]["outcomes"]
                best_odds=max([o["price"] for o in odds_list])
                pick_type=max(odds_list,key=lambda x:x["price"])["name"]

                form_home=await get_team_form(match["home_team_id"])
                form_away=await get_team_form(match["away_team_id"])
                player_home=await get_player_impact(match["home_team_id"])
                player_away=await get_player_impact(match["away_team_id"])
                news_signals=await fetch_newsapi(home,away)

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
                    "reasons":["Odds data",f"Form:{round(form_home,1)}-{round(form_away,1)}",f"Player impact:{player_impact}"]+news_signals
                })
    return picks

