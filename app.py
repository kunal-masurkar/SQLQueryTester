from flask import Flask, request, jsonify, render_template
from modules.test_manager import TestManager
from modules.query_executor import QueryExecutor
from modules.security import SecurityTester
from modules.reporter import ReportGenerator
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
query_executor = QueryExecutor(Config.DATABASE_URI)
test_manager = TestManager(Config.TEST_CASES_DIR)
security_tester = SecurityTester(injection_patterns=Config.SQL_INJECTION_PATTERNS)
report_generator = ReportGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/execute', methods=['POST'])
def execute_query():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Validate query
        validation = query_executor.validate_query(query)
        if not validation['is_valid']:
            return jsonify({
                'error': 'Invalid query',
                'issues': validation['issues']
            }), 400
        
        # Execute query
        result = query_executor.execute(query)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/test/injection', methods=['POST'])
def test_injection():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        vulnerabilities = security_tester.test_sql_injection(query)
        return jsonify({
            'success': True,
            'vulnerabilities': vulnerabilities
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/tests/load', methods=['GET'])
def load_tests():
    try:
        test_cases = test_manager.load_test_cases()
        return jsonify({
            'success': True,
            'test_cases': test_cases
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/tests/run', methods=['POST'])
def run_tests():
    try:
        results = test_manager.run_tests(query_executor)
        report = report_generator.generate_report(results)
        return jsonify({
            'success': True,
            'results': results,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG) 