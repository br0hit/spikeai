import pandas as pd

ALLOWED_OPS = {"filter", "group_by", "aggregate"}
ALLOWED_FIELDS = {
    "url",
    "protocol",
    "title_length",
    "meta_description",
    "indexability",
    "meta_missing",
    "meta_duplicate",
}

ALLOWED_CONDITIONS = {"eq", "neq", "gt", "lt"}

def validate_plan(plan: dict):
    if plan.get("dataset") != "seo":
        raise ValueError("Invalid dataset")

    for op in plan.get("operations", []):
        if op["op"] not in ALLOWED_OPS:
            raise ValueError(f"Invalid op: {op['op']}")
        if "field" in op and op["field"] not in ALLOWED_FIELDS:
            raise ValueError(f"Invalid field: {op['field']}")

def apply_filter(df: pd.DataFrame, op: dict) -> pd.DataFrame:
    f, c, v = op["field"], op["condition"], op["value"]

    if c == "eq":
        return df[df[f] == v]
    if c == "neq":
        return df[df[f] != v]
    if c == "gt":
        return df[df[f] > v]
    if c == "lt":
        return df[df[f] < v]

    raise ValueError(f"Unsupported condition {c}")

def execute_plan(df: pd.DataFrame, plan: dict):
    validate_plan(plan)

    working = df.copy()
    result = None

    for op in plan["operations"]:
        if op["op"] == "filter":
            working = apply_filter(working, op)

        elif op["op"] == "group_by":
            result = (
                working
                .groupby(op["field"])
                .size()
                .reset_index(name="count")
            )

        elif op["op"] == "aggregate":
            if op["type"] == "count":
                result = len(working)

            elif op["type"] == "percentage":
                total = len(working)
                match = (working[op["field"]] == op["value"]).sum()
                result = (match / total) * 100 if total else 0

    if plan.get("select"):
        return working[plan["select"]].dropna().to_dict(orient="records")

    return result
