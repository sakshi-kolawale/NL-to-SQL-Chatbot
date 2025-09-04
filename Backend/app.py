
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from database import DatabaseManager
from nl_to_sql import NLToSQLConverter
from config import Config

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
CORS(app)
app.config.from_object(Config)

# Global instances
db_manager = DatabaseManager()
sql_converter = NLToSQLConverter()

@app.route('/api/connect', methods=['POST'])
def connect_database():
    """Connect to MySQL database"""
    try:
        data = request.get_json()
        connection_string = data.get('connection_string')
        
        if not connection_string:
            return jsonify({
                'success': False,
                'message': 'Connection string is required'
            }), 400
        
        success = db_manager.connect(connection_string)
        
        if success:
            schema = db_manager.get_schema()
            if schema:
                return jsonify({
                    'success': True,
                    'message': 'Connected to MySQL database successfully',
                    'schema': schema
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Connected but failed to retrieve schema'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to connect to MySQL database'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Connection error: {str(e)}'
        }), 500

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process natural language query"""
    try:
        data = request.get_json()
        nl_query = data.get('query', '').strip()
        
        if not nl_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Test connection
        if not db_manager.test_connection():
            return jsonify({'error': 'Database connection lost. Please reconnect.'}), 400
        
        # Get current schema
        schema = db_manager.get_schema()
        if not schema:
            return jsonify({'error': 'No database schema available'}), 400
        
        # Generate SQL
        sql_query, error = sql_converter.generate_sql(nl_query, schema)
        if error:
            return jsonify({'error': error}), 400
        
        if not sql_query:
            return jsonify({'error': 'Failed to generate SQL query'}), 400
        
        # Execute query
        results, exec_error = db_manager.execute_query(sql_query)
        if exec_error:
            return jsonify({
                'error': f'SQL execution error: {exec_error}',
                'generated_sql': sql_query
            }), 400
        
        return jsonify({
            'success': True,
            'sql_query': sql_query,
            'results': results or [],
            'count': len(results) if results else 0
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get database schema"""
    try:
        if not db_manager.test_connection():
            return jsonify({'error': 'Database connection lost'}), 400
            
        schema = db_manager.get_schema()
        if schema:
            return jsonify({'schema': schema})
        else:
            return jsonify({'error': 'Failed to retrieve schema'}), 500
    except Exception as e:
        return jsonify({'error': f'Schema error: {str(e)}'}), 500

@app.route('/api/execute-sql', methods=['POST'])
def execute_raw_sql():
    """Execute raw SQL query"""
    try:
        data = request.get_json()
        sql_query = data.get('sql_query', '').strip()
        
        if not sql_query:
            return jsonify({'error': 'SQL query is required'}), 400
        
        if not db_manager.test_connection():
            return jsonify({'error': 'Database connection lost'}), 400
        
        results, error = db_manager.execute_query(sql_query)
        if error:
            return jsonify({'error': f'SQL execution error: {error}'}), 400
        
        return jsonify({
            'success': True,
            'results': results or [],
            'count': len(results) if results else 0
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/disconnect', methods=['POST'])
def disconnect_database():
    """Disconnect from database"""
    try:
        db_manager.close()
        return jsonify({
            'success': True,
            'message': 'Disconnected from database'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Disconnect error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database_connected': db_manager.test_connection()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Database URL: {Config.DATABASE_URL}")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)

