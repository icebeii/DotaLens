def calculate_win(player_slot: int, radiant_win: bool) -> bool:
    is_radiant = player_slot < 128
    if is_radiant:
        return radiant_win
    return not radiant_win

def get_hero_name(heroes: list[dict], hero_id: int) -> str:
    for hero in heroes:
        if hero["id"] == hero_id:
            return hero["localized_name"]
    return "Unknown"

def calculate_hero_stats(matches: list[dict], heroes: list[dict]) -> list[dict]:
    stats = {}

    for match in matches:
        hero_id = match["hero_id"]

        if hero_id not in stats:
            stats[hero_id] = {
                "hero_id": hero_id,
                "hero_name": get_hero_name(heroes, hero_id),
                "games": 0,
                "wins": 0,
                "losses": 0
            }

        stats[hero_id]["games"] += 1
        if calculate_win(match["player_slot"], match["radiant_win"]):
            stats[hero_id]["wins"] += 1
        else:
            stats[hero_id]["losses"] += 1

    for hero in stats.values():
        hero["win_rate"] = round(hero["wins"] / hero["games"] * 100, 2)

    return sorted(stats.values(), key=lambda hero: hero["games"], reverse=True)

def calculate_player_stats(matches: list[dict]) -> dict:
    games = len(matches)

    if games == 0:
        return {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "avg_kills": 0,
            "avg_deaths": 0,
            "avg_assists": 0,
        }

    wins = 0
    total_kills = 0
    total_deaths = 0
    total_assists = 0

    for match in matches:
        if calculate_win(match["player_slot"], match["radiant_win"]):
            wins += 1

        total_kills += match["kills"]
        total_deaths += match["deaths"]
        total_assists += match["assists"]

    losses = games - wins

    return {
        "games": games,
        "wins": wins,
        "losses": losses,
        "win_rate": round(wins / games * 100, 2),
        "avg_kills": round(total_kills / games, 2),
        "avg_deaths": round(total_deaths / games, 2),
        "avg_assists": round(total_assists / games, 2),
    }