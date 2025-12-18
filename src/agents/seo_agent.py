import pandas as pd
from seo_schema import normalize_seo_schema
from seo_executor import execute_plan
from seo_planner import generate_plan

def run_seo_agent(user_query: str, df: pd.DataFrame):
    normalized = normalize_seo_schema(df)

    plan = generate_plan(user_query)

    result = execute_plan(normalized, plan)

    return result
