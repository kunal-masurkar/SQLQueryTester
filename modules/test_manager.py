import os
import yaml
import json
from datetime import datetime
from typing import List, Dict, Any
from .query_executor import QueryExecutor

class TestManager:
    def __init__(self, test_cases_dir: str):
        self.test_cases_dir = test_cases_dir
        if not os.path.exists(test_cases_dir):
            os.makedirs(test_cases_dir)

    def load_test_cases(self) -> List[Dict[str, Any]]:
        """
        Load all test cases from YAML files in the test cases directory.
        
        Returns:
            List[Dict[str, Any]]: List of test cases
        """
        test_cases = []
        for filename in os.listdir(self.test_cases_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(self.test_cases_dir, filename)
                with open(file_path, 'r') as f:
                    test_cases.extend(yaml.safe_load(f)['test_cases'])
        return test_cases

    def run_tests(self, query_executor: QueryExecutor) -> List[Dict[str, Any]]:
        """
        Run all test cases using the provided query executor.
        
        Args:
            query_executor (QueryExecutor): The query executor to use
            
        Returns:
            List[Dict[str, Any]]: Test results
        """
        test_cases = self.load_test_cases()
        results = []
        
        for test_case in test_cases:
            result = {
                'name': test_case['name'],
                'query': test_case['query'],
                'status': 'PENDING',
                'error': None,
                'execution_time': 0
            }
            
            try:
                # Execute the query
                actual_output = query_executor.execute(test_case['query'])
                
                # Compare with expected output using robust comparison
                if self._compare_outputs(actual_output, test_case['expected_output']):
                    result['status'] = 'PASS'
                else:
                    result['status'] = 'FAIL'
                    result['error'] = f'Expected {test_case["expected_output"]}, got {actual_output}'
                
            except Exception as e:
                result['status'] = 'ERROR'
                result['error'] = str(e)
            
            results.append(result)
        
        return results

    def save_test_case(self, test_case: Dict[str, Any]) -> str:
        """Save a new test case to a YAML file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'test_case_{timestamp}.yaml'
        file_path = os.path.join(self.test_cases_dir, filename)
        
        with open(file_path, 'w') as f:
            yaml.dump([test_case], f, default_flow_style=False)
        
        return filename

    def _execute_test_case(self, test_case: Dict[str, Any]) -> Any:
        """Execute a single test case and return the result."""
        # This method should be implemented to actually execute the query
        # For now, we'll return a mock result
        return {'mock': 'result'}

    def _compare_outputs(self, actual: Any, expected: Any) -> bool:
        """Compare actual and expected outputs."""
        if actual is None or expected is None:
            return actual == expected
        
        # Convert both to JSON-serializable format for comparison
        actual_json = json.dumps(actual, sort_keys=True)
        expected_json = json.dumps(expected, sort_keys=True)
        
        return actual_json == expected_json 