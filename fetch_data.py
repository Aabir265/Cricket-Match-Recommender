"""
Download and prepare India's men's international cricket matches
from Cricsheet for the India Cricket Match Recommendation System.

Filters:
    - Team: India
    - Gender: male
    - International matches only
    - Date: 2000-01-01 onwards
    - Formats: Test, ODI, T20I

Output:
    data/matches.csv

Source:
    https://cricsheet.org/
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from datetime import date
from urllib.request import Request, urlopen

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

CRICSHEET_URL = "https://cricsheet.org/downloads/all_json.zip"

START_DATE = date(2000, 1, 1)

OUTPUT_DIR = Path("data")
RAW_DIR = OUTPUT_DIR / "raw"
OUTPUT_FILE = OUTPUT_DIR / "matches.csv"

# Keep the downloaded archive so we don't download it every run.
ARCHIVE_FILE = RAW_DIR / "all_json.zip"


# ============================================================
# DOWNLOAD
# ============================================================

def download_cricsheet() -> None:
    """Download Cricsheet's complete JSON archive."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if ARCHIVE_FILE.exists():
        print(f"✓ Archive already exists: {ARCHIVE_FILE}")
        return

    print("Downloading Cricsheet JSON data...")
    print(f"URL: {CRICSHEET_URL}")

    request = Request(
        CRICSHEET_URL,
        headers={
            "User-Agent": "India-Cricket-Recommender/1.0"
        },
    )

    with urlopen(request, timeout=60) as response:
        data = response.read()

    ARCHIVE_FILE.write_bytes(data)

    size_mb = len(data) / (1024 * 1024)

    print(f"✓ Download complete: {size_mb:.1f} MB")


# ============================================================
# HELPERS
# ============================================================

def get_match_format(info: dict) -> str:
    """
    Convert Cricsheet's match_type into a cleaner format name.
    """

    match_type = str(info.get("match_type", "")).lower()

    if match_type == "test":
        return "Test"

    if match_type == "odi":
        return "ODI"

    if match_type == "t20":
        return "T20I"

    return match_type.upper()


def get_opponent(info: dict) -> str | None:
    """Return India's opponent."""

    teams = info.get("teams", [])

    for team in teams:
        if team != "India":
            return team

    return None


def get_match_date(info: dict) -> str | None:
    """Return the first match date as YYYY-MM-DD."""

    dates = info.get("dates", [])

    if not dates:
        return None

    return str(dates[0])


def get_result(info: dict) -> tuple[str | None, str | None, int | None]:
    """
    Extract India's result.

    Returns:
        result
        winner
        margin

    Examples:
        ("Won", "India", 6)
        ("Lost", "Australia", 5)
        ("Draw", None, None)
        ("Tied", None, None)
    """

    outcome = info.get("outcome", {})

    winner = outcome.get("winner")

    if winner == "India":
        result = "Won"
    elif winner:
        result = "Lost"
    elif "result" in outcome:
        result = str(outcome["result"]).title()
    else:
        result = None

    margin_data = outcome.get("by", {})

    margin = None

    if isinstance(margin_data, dict):

        if "runs" in margin_data:
            margin = int(margin_data["runs"])

        elif "wickets" in margin_data:
            margin = int(margin_data["wickets"])

    return result, winner, margin


def get_margin_type(info: dict) -> str | None:
    """Determine whether the margin was by runs or wickets."""

    outcome = info.get("outcome", {})
    by = outcome.get("by", {})

    if "runs" in by:
        return "runs"

    if "wickets" in by:
        return "wickets"

    return None


def get_event(info: dict) -> tuple[str | None, str | None]:
    """Extract tournament/event information."""

    event = info.get("event", {})

    if not isinstance(event, dict):
        return None, None

    return (
        event.get("name"),
        event.get("stage"),
    )


def get_player_of_match(info: dict) -> str | None:
    """Return player(s) of the match."""

    players = info.get("player_of_match", [])

    if not players:
        return None

    return ", ".join(players)


def get_india_players(info: dict) -> str:
    """Return India's playing XI."""

    players = info.get("players", {})

    india_players = players.get("India", [])

    return ", ".join(india_players)


def get_venue(info: dict) -> str | None:
    return info.get("venue")


def get_city(info: dict) -> str | None:
    return info.get("city")


def is_india_men_international(info: dict) -> bool:
    """
    Check whether the match is one we want.

    Conditions:
        - India participated
        - male
        - international
        - date >= 2000
        - Test / ODI / T20I
    """

    teams = info.get("teams", [])

    if "India" not in teams:
        return False

    # Gender filter
    if info.get("gender") != "male":
        return False

    # Team type filter
    team_type = info.get("team_type")

    if team_type and team_type != "international":
        return False

    # Date filter
    dates = info.get("dates", [])

    if not dates:
        return False

    try:
        match_date = date.fromisoformat(str(dates[0]))
    except ValueError:
        return False

    if match_date < START_DATE:
        return False

    # Format filter
    match_type = str(info.get("match_type", "")).lower()

    if match_type not in {"test", "odi", "t20"}:
        return False

    return True


# ============================================================
# PARSE MATCHES
# ============================================================

def parse_matches() -> list[dict]:
    """Read the Cricsheet archive and extract India's matches."""

    print("\nReading Cricsheet matches...")

    matches = []

    with zipfile.ZipFile(ARCHIVE_FILE, "r") as archive:

        json_files = [
            name
            for name in archive.namelist()
            if name.endswith(".json")
        ]

        print(f"Found {len(json_files):,} JSON match files.")

        for index, filename in enumerate(json_files, start=1):

            try:
                raw = archive.read(filename)
                match = json.loads(raw)
                info = match.get("info", {})

            except (json.JSONDecodeError, KeyError, zipfile.BadZipFile) as exc:
                print(f"Skipping {filename}: {exc}")
                continue

            if not is_india_men_international(info):
                continue

            match_date = get_match_date(info)

            result, winner, margin = get_result(info)

            event_name, event_stage = get_event(info)

            opponent = get_opponent(info)

            row = {
                "match_id": Path(filename).stem,

                "date": match_date,

                "year": int(match_date[:4])
                if match_date
                else None,

                "format": get_match_format(info),

                "team": "India",

                "opponent": opponent,

                "competition": event_name,

                "stage": event_stage,

                "venue": get_venue(info),

                "city": get_city(info),

                "result": result,

                "winner": winner,

                "margin": margin,

                "margin_type": get_margin_type(info),

                "player_of_match": get_player_of_match(info),

                "india_players": get_india_players(info),
            }

            matches.append(row)

            # Progress indicator
            if index % 1000 == 0:
                print(
                    f"Processed {index:,}/{len(json_files):,} files..."
                )

    return matches


# ============================================================
# CLEAN DATA
# ============================================================

def clean_dataframe(matches: list[dict]) -> pd.DataFrame:

    df = pd.DataFrame(matches)

    if df.empty:
        raise RuntimeError(
            "No India matches were found. "
            "Check the Cricsheet data or filters."
        )

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Sort chronologically
    df = df.sort_values("date")

    # Remove accidental duplicates
    df = df.drop_duplicates(
        subset=["match_id"]
    )

    # Convert back to ISO format
    df["date"] = df["date"].dt.strftime(
        "%Y-%m-%d"
    )

    # Reset index
    df = df.reset_index(drop=True)

    return df


# ============================================================
# SAVE
# ============================================================

def save_dataframe(df: pd.DataFrame) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print(
        f"\n✓ Saved {len(df):,} matches to:"
    )

    print(
        f"  {OUTPUT_FILE}"
    )


# ============================================================
# SUMMARY
# ============================================================

def print_summary(df: pd.DataFrame) -> None:

    print("\n" + "=" * 60)
    print("INDIA CRICKET DATASET")
    print("=" * 60)

    print(f"\nTotal matches: {len(df):,}")

    print("\nMatches by format:")

    print(
        df["format"]
        .value_counts()
        .to_string()
    )

    print("\nMatches by result:")

    print(
        df["result"]
        .value_counts(dropna=False)
        .to_string()
    )

    print("\nMatches by opponent:")

    print(
        df["opponent"]
        .value_counts()
        .head(15)
        .to_string()
    )

    print("\nMatches by year:")

    print(
        df["year"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nDate range:")

    print(
        f"{df['date'].min()} → {df['date'].max()}"
    )

    print("\n" + "=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("INDIA CRICKET DATA PREPARATION")
    print("=" * 60)

    download_cricsheet()

    matches = parse_matches()

    print(
        f"\n✓ Found {len(matches):,} India men's "
        f"international matches since 2000."
    )

    df = clean_dataframe(matches)

    save_dataframe(df)

    print_summary(df)

    print("\nDone! 🎉")


if __name__ == "__main__":
    main()