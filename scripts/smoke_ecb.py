"""Smoke test: check that the environment works and the ECB Data Portal API is reachable.

Run with:  uv run python scripts/smoke_ecb.py
"""

from io import StringIO

import pandas as pd
import requests

ECB_API = "https://data-api.ecb.europa.eu/service/data"

# €STR: volume-weighted trimmed mean rate, business-day frequency
ESTR_KEY = "EST/B.EU000A2X2A25.WT"


def fetch_last(series_key: str, n: int = 5) -> pd.DataFrame:
    resp = requests.get(
        f"{ECB_API}/{series_key}",
        params={"lastNObservations": n, "format": "csvdata"},
        timeout=30,
    )
    resp.raise_for_status()
    df = pd.read_csv(StringIO(resp.text))
    return df[["TIME_PERIOD", "OBS_VALUE"]].rename(
        columns={"TIME_PERIOD": "date", "OBS_VALUE": "rate_pct"}
    )


if __name__ == "__main__":
    print("€STR, last 5 fixings (%):")
    print(fetch_last(ESTR_KEY).to_string(index=False))
