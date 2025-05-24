import pandas as pd

BUDGET_SCHEMA = [
    "Transaction ID", "Date", "Time", "Type", "Name", "Emoji", "Category", "Amount", "Currency",
    "Local Amount", "Local Currency", "Notes & #tags", "Address", "Receipt", "Description", "Category Split",
    "Money Out", "Money In", "Tag"  # Tag is the extra column
]

MONZO_COLUMNS = [
    "Transaction ID", "Date", "Time", "Type", "Name", "Emoji", "Category", "Amount", "Currency",
    "Local Amount", "Local Currency", "Notes & #tags", "Address", "Receipt", "Description", "Category Split",
    "Money Out", "Money In"
]

def extract_monzo_csv(file):
    """
    Parse a Monzo CSV file-like object, map to Budget schema, return DataFrame.
    On error, return dict: {"error": ..., "line": ...}
    """
    try:
        df = pd.read_csv(file)
        # Check columns
        if not all(col in df.columns for col in MONZO_COLUMNS):
            missing = [col for col in MONZO_COLUMNS if col not in df.columns]
            return {"error": f"Missing columns: {missing}", "line": 0}
        # Add Tag column (empty)
        df["Tag"] = ""
        # Reorder columns to match schema
        df = df[[*MONZO_COLUMNS, "Tag"]]
        return df
    except Exception as e:
        # Try to get line number from error
        line = getattr(e, 'lineno', None) or 0
        return {"error": str(e), "line": line} 