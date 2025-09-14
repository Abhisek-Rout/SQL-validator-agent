import os

def load_sql_file(file_path: str, verbose: bool = False) -> str:
    """Load SQL file from disk and return content."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SQL file not found: {file_path}")

    with open(file_path, "r") as f:
        sql_content = f.read()

    if verbose:
        print(f"Loaded SQL file: {file_path}")
        print(f"File size: {len(sql_content)} characters")

    return sql_content
