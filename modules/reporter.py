import os
import json
import yaml
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

class ReportGenerator:
    def __init__(self, report_dir: str = 'reports'):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)

    def generate_report(self, test_results: List[Dict[str, Any]], format: str = 'json') -> Dict[str, Any]:
        """
        Generate a test report from test results.
        
        Args:
            test_results (List[Dict[str, Any]]): List of test results
            format (str): Output format ('json', 'yaml', or 'html')
            
        Returns:
            Dict[str, Any]: Generated report
        """
        # Calculate summary statistics
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results if r['status'] == 'PASS')
        failed_tests = sum(1 for r in test_results if r['status'] == 'FAIL')
        error_tests = sum(1 for r in test_results if r['status'] == 'ERROR')
        
        # Calculate average execution time
        execution_times = [r['execution_time'] for r in test_results if r['status'] != 'ERROR']
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'error_tests': error_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                'average_execution_time': avg_execution_time
            },
            'test_results': test_results
        }
        
        # Save report to file
        self._save_report(report, format)
        
        return report

    def _save_report(self, report: Dict[str, Any], format: str):
        """
        Save the report to a file in the specified format.
        
        Args:
            report (Dict[str, Any]): The report to save
            format (str): Output format
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f'report_{timestamp}.json'
            filepath = os.path.join(self.report_dir, filename)
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
                
        elif format == 'yaml':
            filename = f'report_{timestamp}.yaml'
            filepath = os.path.join(self.report_dir, filename)
            with open(filepath, 'w') as f:
                yaml.dump(report, f, default_flow_style=False)
                
        elif format == 'html':
            filename = f'report_{timestamp}.html'
            filepath = os.path.join(self.report_dir, filename)
            self._generate_html_report(report, filepath)
            
        else:
            raise ValueError(f"Unsupported report format: {format}")

    def _generate_html_report(self, report: Dict[str, Any], filepath: str):
        """
        Generate an HTML report.
        
        Args:
            report (Dict[str, Any]): The report data
            filepath (str): Path to save the HTML file
        """
        # Convert test results to DataFrame for easier HTML generation
        df = pd.DataFrame(report['test_results'])
        
        # Generate HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SQL Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .test-results {{ margin-top: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .pass {{ color: green; }}
                .fail {{ color: red; }}
                .error {{ color: orange; }}
            </style>
        </head>
        <body>
            <h1>SQL Test Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Tests: {report['summary']['total_tests']}</p>
                <p>Passed: {report['summary']['passed_tests']}</p>
                <p>Failed: {report['summary']['failed_tests']}</p>
                <p>Errors: {report['summary']['error_tests']}</p>
                <p>Success Rate: {report['summary']['success_rate']:.2f}%</p>
                <p>Average Execution Time: {report['summary']['average_execution_time']:.2f}s</p>
            </div>
            <div class="test-results">
                <h2>Test Results</h2>
                {df.to_html(classes='test-results-table', index=False)}
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w') as f:
            f.write(html) 