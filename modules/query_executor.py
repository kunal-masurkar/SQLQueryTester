from sqlalchemy import create_engine, text
from typing import Any, Dict, List
import pandas as pd
import os

class QueryExecutor:
    def __init__(self, database_uri: str):
        # For SQLite, ensure the database file exists
        if database_uri.startswith('sqlite'):
            db_path = database_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                # Create an empty file
                with open(db_path, 'w') as f:
                    pass
        
        self.engine = create_engine(database_uri)
        self.connection = self.engine.connect()

    def execute(self, query: str) -> Any:
        """
        Execute a SQL query and return the results.
        
        Args:
            query (str): The SQL query to execute
            
        Returns:
            Any: Query results in a format suitable for comparison
        """
        try:
            # Execute the query
            result = self.connection.execute(text(query))
            
            # If it's a SELECT query, return the results
            if query.strip().upper().startswith('SELECT'):
                # Convert to pandas DataFrame for easier manipulation
                df = pd.DataFrame(result.fetchall())
                if not df.empty:
                    df.columns = result.keys()
                return df.to_dict('records')
            
            # For non-SELECT queries, return affected row count
            return {'affected_rows': result.rowcount}
            
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate a SQL query without executing it.
        
        Args:
            query (str): The SQL query to validate
            
        Returns:
            Dict[str, Any]: Validation results including query type and potential issues
        """
        validation = {
            'is_valid': True,
            'query_type': None,
            'issues': []
        }
        
        try:
            # Basic query type detection
            query_upper = query.strip().upper()
            if query_upper.startswith('SELECT'):
                validation['query_type'] = 'SELECT'
            elif query_upper.startswith('INSERT'):
                validation['query_type'] = 'INSERT'
            elif query_upper.startswith('UPDATE'):
                validation['query_type'] = 'UPDATE'
            elif query_upper.startswith('DELETE'):
                validation['query_type'] = 'DELETE'
            else:
                validation['issues'].append('Unknown query type')
            
            # Check for common issues
            if 'DROP' in query_upper or 'TRUNCATE' in query_upper:
                validation['issues'].append('Query contains potentially dangerous operations')
            
            validation['is_valid'] = len(validation['issues']) == 0
            
        except Exception as e:
            validation['is_valid'] = False
            validation['issues'].append(str(e))
        
        return validation

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose() 