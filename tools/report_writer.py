import os
import json
from datetime import datetime

REPORTS_DIR = "reports"

def save_report(filename: str, sql_text: str, checker_result, evaluator_result, verbose: bool = False):
    """
    Save a SQL validation report in Markdown format.

    - filename: path to the SQL file
    - sql_text: content of the SQL file
    - checker_result: dict or Markdown-formatted JSON string
    - evaluator_result: dict or Markdown-formatted JSON string
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    report_path = os.path.join(REPORTS_DIR, f"sql_report_{base_name}.md")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(report_path, "w", encoding="utf-8") as f:
        # Header
        f.write(f"# SQL Validation Report\n\n")
        f.write(f"**File:** `{filename}`  \n")
        f.write(f"**Timestamp:** {timestamp}\n\n")

        # SQL Content
        f.write("## SQL Content\n")
        f.write("```sql\n")
        if len(sql_text) > 500:
            f.write(sql_text[:500] + "...\n")
        else:
            f.write(sql_text + "\n")
        f.write("```\n\n")

        # SQL Checker Result
        f.write("## SQL Checker Result\n")
        if isinstance(checker_result, str) and checker_result.strip().startswith("```"):
            # Already Markdown-formatted
            f.write(checker_result.strip() + "\n\n")
        else:
            f.write("```json\n")
            f.write(json.dumps(checker_result, indent=2))
            f.write("\n```\n\n")

        # Evaluator Result
        f.write("## Evaluator Result\n")
        if isinstance(evaluator_result, str) and evaluator_result.strip().startswith("```"):
            f.write(evaluator_result.strip() + "\n")
        else:
            f.write("```json\n")
            f.write(json.dumps(evaluator_result, indent=2))
            f.write("\n```\n")

    if verbose:
        print(f"Report saved: {report_path}")

    return {"report_md": report_path}
