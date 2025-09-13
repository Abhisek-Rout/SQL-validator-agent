import sys
from crewai import Crew, Process
from agents.sql_checker import SQLCheckerAgent
from agents.report_generator import ReportGeneratorAgent
from agents.sql_report_validator import SQLVerifierAgent
from utils.file_loader import get_sql_file, read_sql_file, write_report, write_corrected_sql

def main():
    if len(sys.argv) < 2:
        print("Usage: python crew.py <sql_filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        filepath = get_sql_file(filename)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # Read SQL content
    sql_content = read_sql_file(filepath)

    # Initialize agents
    checker_agent = SQLCheckerAgent()
    verifier_agent = SQLVerifierAgent()
    reporter_agent = ReportGeneratorAgent()

    # Wrap in CrewAI Crew
    crew = Crew(
        agents=[checker_agent, verifier_agent, reporter_agent],
        process=Process.sequential,
        verbose=True
    )

    # Step 1: Run SQL Checker
    check_result = checker_agent.execute({filename: sql_content})

    # Step 2: Run SQL Verifier on checker output
    verify_result = verifier_agent.execute(check_result)

    # Step 3: Generate final report including verification
    report_content = f"""
File: {filename}

Checker Result: {check_result.get(filename)}
Verifier Result: {verify_result.get(filename)}
"""
    write_report(filename, report_content)

    # Step 4: Write corrected SQL (only if verifier passes)
    corrected_sql = check_result.get(filename, {}).get("corrected_sql", sql_content)
    if verify_result.get(filename, {}).get("verifier_pass", False):
        write_corrected_sql(filename, corrected_sql)
        print(f"Corrected SQL written for '{filename}'")
    else:
        print(f"Corrected SQL not written because verification failed for '{filename}'")

    print(f"Completed processing '{filename}'")
    print(f"Reports saved in './reports/'")

if __name__ == "__main__":
    main()