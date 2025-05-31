-- Create departments table
CREATE TABLE departments (
    department_code VARCHAR(10) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

-- Create employees table
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(10) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (department) REFERENCES departments(department_code)
);

-- Insert sample data into departments
INSERT INTO departments (department_code, department_name) VALUES
    ('IT', 'Information Technology'),
    ('HR', 'Human Resources'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing');

-- Insert sample data into employees
INSERT INTO employees (name, department, salary) VALUES
    ('John Doe', 'IT', 75000),
    ('Jane Smith', 'HR', 65000),
    ('Bob Johnson', 'Finance', 80000),
    ('Alice Brown', 'Marketing', 70000),
    ('Charlie Wilson', 'IT', 80000),
    ('Diana Miller', 'Finance', 70000); 