from .csv_extractor import extract_monzo_csv

def route_extractor(file):
    """Auto-detect file type and return the extractor name ('csv', 'pdf', 'image')."""
    ext = file.name.split('.')[-1].lower()
    if ext == 'csv':
        return 'csv'
    elif ext == 'pdf':
        return 'pdf'
    elif ext in ['png', 'jpg', 'jpeg']:
        return 'image'
    else:
        return 'unknown'

def extract_csv(file):
    """Extract and map Monzo CSV to Budget schema."""
    return extract_monzo_csv(file)

def extract_pdf(file):
    """Stub for PDF extraction."""
    return f"Extracted PDF: {file.name}"

def extract_image(file):
    """Stub for image extraction."""
    return f"Extracted Image: {file.name}" 