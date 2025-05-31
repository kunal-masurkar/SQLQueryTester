# SQLQueryTester

A hybrid SQL query testing tool that allows you to write, execute, and validate SQL queries against a database. This tool is particularly useful for testing SQL queries, learning SQL, and validating database operations.

## Features

- Execute SQL queries against a database
- Validate query syntax and structure
- Run test cases with expected outputs
- Support for various SQL operations (SELECT, INSERT, UPDATE, DELETE)
- YAML-based test case management
- Detailed test results and error reporting

## Project Structure

```
SQLQueryTester/
├── modules/
│   ├── __init__.py
│   ├── query_executor.py    # Handles database connections and query execution
│   └── test_manager.py      # Manages test cases and test execution
├── test_cases/
│   └── sample_queries.yaml  # Sample test cases
├── schema.sql              # Database schema and sample data
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.7 or higher
- SQLite (included with Python)
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kunal-masurkar/SQLQueryTester
cd SQLQueryTester
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. Initialize the database:
```bash
sqlite3 database.db < schema.sql
```

2. Configure the database connection:
   - The default configuration uses SQLite
   - Database file will be created automatically if it doesn't exist

## Usage

### Running Test Cases

1. Place your test cases in YAML format in the `test_cases` directory
2. Each test case should include:
   - name: Test case name
   - query: SQL query to execute
   - expected_output: Expected result

Example test case:
```yaml
test_cases:
  - name: "Basic SELECT Query"
    query: "SELECT * FROM employees"
    expected_output:
      - {"id": 1, "name": "John Doe", "department": "IT", "salary": 75000}
```

### Sample Queries

The project includes several sample queries demonstrating different SQL operations:

1. Basic SELECT queries
2. Queries with WHERE clauses
3. JOIN operations
4. Aggregate functions
5. Subqueries
6. Complex queries with multiple clauses

## Database Schema

The project uses two main tables:

### Departments Table
```sql
CREATE TABLE departments (
    department_code VARCHAR(10) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);
```

### Employees Table
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(10) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (department) REFERENCES departments(department_code)
);
```

## Development

### Adding New Features

1. Create new test cases in the `test_cases` directory
2. Modify the schema in `schema.sql` if needed
3. Update the query executor or test manager as required

### Running Tests

To run all test cases:
```python
from modules.test_manager import TestManager
from modules.query_executor import QueryExecutor

# Initialize components
query_executor = QueryExecutor('sqlite:///database.db')
test_manager = TestManager('test_cases')

# Run tests
results = test_manager.run_tests(query_executor)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Kunal Masurkar <br>
 [GitHub](https://github.com/kunal-masurkar) <br>  [LinkedIn](https://linkedin.com/in/kunal-masurkar-8494a123a)

## Support

For support, please open an issue in the repository or contact the maintainers. 
