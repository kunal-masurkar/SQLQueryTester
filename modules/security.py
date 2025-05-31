from typing import List, Dict, Any
import re

class SecurityTester:
    def __init__(self, injection_patterns: List[str] = None):
        self.injection_patterns = injection_patterns or [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "1' OR '1'='1",
            "1; DROP TABLE users; --"
        ]
        self.common_vulnerabilities = [
            r"'.*OR.*'1'='1",
            r"'.*UNION.*SELECT",
            r"'.*DROP.*TABLE",
            r"'.*DELETE.*FROM",
            r"'.*UPDATE.*SET",
            r"'.*INSERT.*INTO",
            r"'.*EXEC.*",
            r"'.*EXECUTE.*",
            r"'.*WAITFOR.*DELAY",
            r"'.*SLEEP.*",
        ]

    def test_sql_injection(self, query: str) -> List[Dict[str, Any]]:
        """
        Test a SQL query for potential injection vulnerabilities.
        
        Args:
            query (str): The SQL query to test
            
        Returns:
            List[Dict[str, Any]]: List of found vulnerabilities
        """
        vulnerabilities = []
        
        # Check for common SQL injection patterns
        for pattern in self.injection_patterns:
            if pattern in query:
                vulnerabilities.append({
                    'type': 'SQL_INJECTION',
                    'pattern': pattern,
                    'description': f'Query contains potential SQL injection pattern: {pattern}'
                })
        
        # Check for unescaped quotes
        if query.count("'") % 2 != 0:
            vulnerabilities.append({
                'type': 'UNESCAPED_QUOTES',
                'description': 'Query contains unescaped quotes'
            })
        
        # Check for dangerous operations
        dangerous_operations = ['DROP', 'TRUNCATE', 'DELETE FROM', 'UPDATE']
        for operation in dangerous_operations:
            if operation in query.upper():
                vulnerabilities.append({
                    'type': 'DANGEROUS_OPERATION',
                    'operation': operation,
                    'description': f'Query contains dangerous operation: {operation}'
                })
        
        return vulnerabilities

    def test_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Test a SQL query for potential security vulnerabilities.
        
        Args:
            query (str): The SQL query to test
            
        Returns:
            List[Dict[str, Any]]: List of found vulnerabilities
        """
        vulnerabilities = []
        
        # Test for SQL injection patterns
        for pattern in self.injection_patterns:
            if pattern in query:
                vulnerabilities.append({
                    'type': 'SQL_INJECTION',
                    'pattern': pattern,
                    'severity': 'HIGH',
                    'description': f'Query contains potential SQL injection pattern: {pattern}'
                })
        
        # Test for common vulnerabilities using regex
        for pattern in self.common_vulnerabilities:
            if re.search(pattern, query, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'SQL_INJECTION',
                    'pattern': pattern,
                    'severity': 'HIGH',
                    'description': f'Query matches common SQL injection pattern: {pattern}'
                })
        
        # Test for parameterized query usage
        if not self._is_parameterized(query):
            vulnerabilities.append({
                'type': 'PARAMETERIZATION',
                'severity': 'MEDIUM',
                'description': 'Query does not use parameterized statements'
            })
        
        # Test for sensitive data exposure
        if self._contains_sensitive_data(query):
            vulnerabilities.append({
                'type': 'SENSITIVE_DATA',
                'severity': 'HIGH',
                'description': 'Query may expose sensitive data'
            })
        
        return vulnerabilities

    def _is_parameterized(self, query: str) -> bool:
        """
        Check if the query uses parameterized statements.
        
        Args:
            query (str): The SQL query to check
            
        Returns:
            bool: True if the query uses parameterized statements
        """
        # Look for common parameterization patterns
        param_patterns = [
            r':\w+',  # Named parameters
            r'\?',    # Positional parameters
            r'%s',    # Python-style parameters
            r'@\w+',  # SQL Server parameters
        ]
        
        return any(re.search(pattern, query) for pattern in param_patterns)

    def _contains_sensitive_data(self, query: str) -> bool:
        """
        Check if the query might expose sensitive data.
        
        Args:
            query (str): The SQL query to check
            
        Returns:
            bool: True if the query might expose sensitive data
        """
        sensitive_patterns = [
            r'password',
            r'credit_card',
            r'ssn',
            r'social_security',
            r'secret',
            r'api_key',
            r'token',
        ]
        
        return any(re.search(pattern, query, re.IGNORECASE) for pattern in sensitive_patterns)

    def get_security_report(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a security report from found vulnerabilities.
        
        Args:
            vulnerabilities (List[Dict[str, Any]]): List of found vulnerabilities
            
        Returns:
            Dict[str, Any]: Security report
        """
        severity_counts = {
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for vuln in vulnerabilities:
            severity_counts[vuln['severity']] += 1
        
        return {
            'total_vulnerabilities': len(vulnerabilities),
            'severity_breakdown': severity_counts,
            'vulnerabilities': vulnerabilities,
            'is_secure': len(vulnerabilities) == 0
        } 