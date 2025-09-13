from crewai import Agent
from utils.file_loader import write_report, write_corrected_sql

class ReportGeneratorAgent(Agent):
    def __init__(self, reports_dir: str):
        super().__init__(
            role="Report Generator",
            goal="Generate a final SQL review report",
            backstory="Summarizes SQL validation results into a structured report."
        )
        self.reports_dir = reports_dir

    def execute(self, review_results: dict):
        """
        Expects review_results in the format:
        {
            "filename.sql": {
                "checker_result": {...},
                "verifier_result": {...},
                "corrected_sql": "..."
            },
            ...
        }
        """
        report_files = []

        for filename, results in review_results.items():
            # Build report content
            report_content = f"File: {filename}\n\n"
            report_content += f"Checker Result: {results.get('checker_result')}\n"
            report_content += f"Verifier Result: {results.get('verifier_result')}\n"

            # Write report using file_loader.py
            report_path = write_report(filename, report_content)
            report_files.append(report_path)

            # Write corrected SQL if available
            corrected_sql = results.get("corrected_sql")
            if corrected_sql:
                write_corrected_sql(filename, corrected_sql)

        return report_files
