# src/services/seo_data.py

import pandas as pd
import io
import requests

class SEODataService:
    # ✅ Correct Sheet ID from hackathon doc
    SHEET_ID = "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE"
    GID = "1438203274"

    def fetch_live_data(self) -> pd.DataFrame:
        """
        Fetch Screaming Frog SEO data live from Google Sheets.
        """
        try:
            url = (
                f"https://docs.google.com/spreadsheets/d/"
                f"{self.SHEET_ID}/gviz/tq?tqx=out:csv&gid={self.GID}"
            )

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            df = pd.read_csv(io.StringIO(response.text))

            # Basic hygiene (schema-safe)
            df = df.dropna(how="all").dropna(axis=1, how="all")

            print(f"✅ Loaded SEO data: {df.shape[0]} rows, {df.shape[1]} columns")
            return df

        except Exception as e:
            print(f"❌ Error fetching SEO data: {e}")
            return pd.DataFrame()

    def get_schema_info(self, df: pd.DataFrame) -> str:
        if df.empty:
            return "No data available."

        lines = []
        for col in df.columns:
            sample = df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A"
            lines.append(f"- {col} (dtype={df[col].dtype}, sample={sample})")

        return "\n".join(lines)
