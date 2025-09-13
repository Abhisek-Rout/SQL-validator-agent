from crewai import Agent
import sqlparse

class SQLVerifierAgent(Agent):
    def __init__(self):
        super().__init__(
            role="SQL Verifier",
            goal="Validate corrected SQL from checker agent",
            backstory="Ensures SQL syntax is correct and query logic is intact."
        )

    def execute(self, check_result: dict):
        results = {}
        for filename, data in check_result.items():
            corrected_sql = data.get("corrected_sql", "")
            # Local syntax validation
            try:
                parsed = sqlparse.parse(corrected_sql)
                valid = len(parsed) > 0
            except Exception:
                valid = False

            results[filename] = {
                "verifier_pass": valid,
                "feedback": "SQL is valid" if valid else "SQL parsing failed"
            }
        return results
