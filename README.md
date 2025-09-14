
# SQL Validator Agent

An AI-powered agent designed to analyze and validate SQL queries for syntax correctness, logical consistency, and adherence to best practices. It provides detailed feedback and suggestions for query optimization.

## 🚀 Features

- **Comprehensive SQL Analysis**: Evaluates SQL queries for:
  - Syntax correctness
  - Logical consistency
  - Performance optimization
  - Best practices adherence

- **Detailed Feedback**: Returns structured feedback including:
  - List of identified issues
  - Suggested improvements
  - Estimated query complexity
  - Corrected SQL query (if applicable)

- **Customizable Prompts**: Allows users to define specific analysis prompts tailored to their needs.

## 📂 Project Structure

```
SQL-validator-agent/
├── config/            # Configuration files for the agent
├── input/             # Sample SQL queries for testing
├── tools/             # Utility scripts and helper functions
├── .gitignore         # Git ignore rules
├── main.py            # Main script to run the agent
└── requirements.txt   # Python dependencies
```

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Abhisek-Rout/SQL-validator-agent.git
   cd SQL-validator-agent
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Usage

To analyze a SQL query, run the following command:

```bash
python main.py --sql "SELECT * FROM users WHERE age > 30"
```

The agent will output a JSON object containing:

- `issues`: List of identified problems (syntax, logical, performance-related)
- `suggestions`: List of recommended improvements
- `complexity`: Estimated query complexity ("Low", "Medium", "High")
- `new_sql`: Corrected SQL query incorporating all improvements (empty string if no changes)

## 🔧 Configuration

The agent's behavior can be customized by modifying the configuration files in the `config/` directory. You can adjust settings such as:

- Prompt templates
- Analysis parameters
- Output formatting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or feedback, please open an issue in the [GitHub repository](https://github.com/Abhisek-Rout/SQL-validator-agent) or contact the maintainer directly.
