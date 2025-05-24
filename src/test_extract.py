import types
from src.extract import route_extractor, extract_csv, extract_pdf, extract_image
import pandas as pd
from io import StringIO

def make_file(name, type_):
    return types.SimpleNamespace(name=name, type=type_)

def test_route_extractor_csv():
    file = make_file("test.csv", "text/csv")
    assert route_extractor(file) == "csv"

def test_route_extractor_pdf():
    file = make_file("test.pdf", "application/pdf")
    assert route_extractor(file) == "pdf"

def test_route_extractor_png():
    file = make_file("test.png", "image/png")
    assert route_extractor(file) == "image"

def test_route_extractor_jpg():
    file = make_file("test.jpg", "image/jpeg")
    assert route_extractor(file) == "image"

def test_route_extractor_unknown():
    file = make_file("test.txt", "text/plain")
    assert route_extractor(file) == "unknown"

def test_extract_csv_valid():
    csv = StringIO(
        'Transaction ID,Date,Time,Type,Name,Emoji,Category,Amount,Currency,Local Amount,Local Currency,Notes & #tags,Address,Receipt,Description,Category Split,Money Out,Money In\n'
        'tx1,2024-01-01,12:00,card,Shop,🛒,Groceries,-10,GBP,-10,GBP,Note,,No,Desc,,10,0\n'
    )
    file = make_file("test.csv", "text/csv")
    file.file = csv
    df = extract_csv(file.file)
    assert isinstance(df, pd.DataFrame)
    assert "Tag" in df.columns
    assert len(df) == 1

def test_extract_csv_missing_column():
    csv = StringIO(
        'Transaction ID,Date,Time,Type,Name,Emoji,Category,Amount,Currency,Local Amount,Local Currency,Notes & #tags,Address,Receipt,Description,Category Split,Money Out\n'
        'tx1,2024-01-01,12:00,card,Shop,🛒,Groceries,-10,GBP,-10,GBP,Note,,No,Desc,,10\n'
    )
    file = make_file("test.csv", "text/csv")
    file.file = csv
    result = extract_csv(file.file)
    assert isinstance(result, dict)
    assert "error" in result
    assert "Missing columns" in result["error"]

def test_extract_pdf():
    file = make_file("test.pdf", "application/pdf")
    assert extract_pdf(file) == "Extracted PDF: test.pdf"

def test_extract_image():
    file = make_file("test.png", "image/png")
    assert extract_image(file) == "Extracted Image: test.png" 