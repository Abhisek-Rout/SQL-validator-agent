import argparse
import os
import yaml
from crewai import Agent, Task, Crew
from tools.file_loader import load_sql_file
from tools.report_writer import save_report

CONFIG_DIR = "config"
INPUT_DIR = "input"


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def create_agent(agent_config):
    """Factory to create an Agent from YAML config."""
    return Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        llm=agent_config["model"],  # model comes from agents.yaml
    )


def create_task(task_config, agent, input_data):
    """Factory to create a Task from YAML config."""
    return Task(
        description=task_config["description"],
        expected_output=task_config["expected_output"],
        agent=agent,
        input=input_data,
    )


import re

def clean_sql(sql: str) -> str:
    """Remove SQL comments before passing to LLM."""
    # Remove -- single line comments
    sql = re.sub(r'--.*', '', sql)
    # Remove /* ... */ block comments
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    return sql.strip()


def main():
    parser = argparse.ArgumentParser(description="SQL Validation Agentic AI")
    parser.add_argument("filename", help="SQL filename inside input/ directory")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    sql_path = os.path.join(INPUT_DIR, args.filename)
    sql_text_raw = load_sql_file(sql_path, verbose=args.verbose)
    sql_text = clean_sql(sql_text_raw)

    # Load configs
    agents_config = load_yaml(os.path.join(CONFIG_DIR, "agents.yaml"))["agents"]
    tasks_config = load_yaml(os.path.join(CONFIG_DIR, "tasks.yaml"))["tasks"]

    if args.verbose:
        print("Agents and tasks configuration loaded")

    # Create agents
    sql_checker_agent = create_agent(agents_config["sql_checker"])
    evaluator_agent = create_agent(agents_config["evaluator"])

    # Create SQL Checker task (substitute {sql} with actual query text)
    check_task_desc = tasks_config["check_sql"]["description"].format(sql=sql_text)
    check_task = create_task(
        {
            "description": check_task_desc,
            "expected_output": tasks_config["check_sql"]["expected_output"],
        },
        sql_checker_agent,
        sql_text,
    )

    # Create Evaluator task (input = checker result later)
    eval_task = create_task(
        tasks_config["evaluate_sql"],
        evaluator_agent,
        input_data="",  # placeholder, updated after checker runs
    )

    # Build Crew
    crew = Crew(
        agents=[sql_checker_agent, evaluator_agent],
        tasks=[check_task, eval_task],
        verbose=args.verbose,
    )

    # Run Crew
    results = crew.kickoff()

    # Extract results
    checker_result = results.tasks_output[0].raw
    evaluator_result = results.tasks_output[1].raw

    if args.verbose:
        print("\n=== SQLCheckerAgent result ===")
        print(checker_result)
        print("\n=== EvaluatorAgent result ===")
        print(evaluator_result)

    # Save report
    report_paths = save_report(
        sql_path, sql_text, checker_result, evaluator_result, verbose=args.verbose
    )

    print("\nProcess complete!")
    print(f"Report MD: {report_paths['report_md']}")


if __name__ == "__main__":
    main()
