import os
from dotenv import load_dotenv

load_dotenv()

SQL_INPUT_DIR = os.getenv("SQL_INPUT_DIR", "./sql_files")
REPORTS_DIR = os.getenv("REPORTS_DIR", "./reports")


def get_sql_file(filename: str) -> str:
    """
    Get absolute path for a given SQL file in the input directory.
    Raises FileNotFoundError if not found.
    """
    filepath = os.path.join(SQL_INPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found: {filepath}")
    return filepath


def read_sql_file(filepath: str) -> str:
    """Read SQL file content"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_report(filename: str, content: str):
    """Write error or validation report"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    base_name = os.path.splitext(filename)[0]
    report_path = os.path.join(REPORTS_DIR, f"{base_name}_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    return report_path


def write_corrected_sql(filename: str, content: str):
    """Write corrected SQL file"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    base_name = os.path.splitext(filename)[0]
    corrected_path = os.path.join(REPORTS_DIR, f"{base_name}_corrected.sql")
    with open(corrected_path, "w", encoding="utf-8") as f:
        f.write(content)
    return corrected_path