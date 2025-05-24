"""
Google Sheets API integration for AI Financial Reviewer.
"""

# Placeholder imports
# import gspread, etc.

def append_rows(sheet_id, tab_id, rows):
    """Append rows below the header in the specified sheet/tab."""
    pass

def lock_header_row(sheet_id, tab_id):
    """Lock the header row to prevent editing."""
    pass

def fill_down_formulas(sheet_id, tagging_tab_id, start_row, end_row):
    """Propagate formulas in the tagging sheet from start_row to end_row."""
    pass

def validate_formula_propagation(sheet_id, tagging_tab_id):
    """Validate that formula columns are filled for all rows; retry if needed."""
    pass 