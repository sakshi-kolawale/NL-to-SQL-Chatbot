
import pymysql
from urllib.parse import urlparse
import pandas as pd
from config import Config

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.db_config = None
        
    def connect(self, connection_string=None):
        """Connect to MySQL database"""
        conn_str = connection_string or Config.DATABASE_URL
        
        try:
            parsed = urlparse(conn_str)
            
            self.db_config = {
                'host': parsed.hostname or 'localhost',
                'user': parsed.username,
                'password': parsed.password,
                'database': parsed.path[1:] if parsed.path else '',
                'port': parsed.port or 3306,
                'charset': 'utf8mb4',
                'autocommit': True
            }
            
            self.connection = pymysql.connect(**self.db_config)
            return True
            
        except Exception as e:
            print(f"MySQL connection error: {e}")
            return False
    
    def get_schema(self):
        """Get MySQL database schema information"""
        if not self.connection:
            return None
            
        schema_info = {}
        cursor = self.connection.cursor()
        
        try:
            # Get all tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            for table_tuple in tables:
                table_name = table_tuple[0]
                
                # Get column information
                cursor.execute(f"DESCRIBE {table_name};")
                columns = cursor.fetchall()
                
                schema_info[table_name] = []
                for col in columns:
                    schema_info[table_name].append({
                        'column': col[0],
                        'type': col[1],
                        'nullable': col[2] == 'YES',
                        'primary_key': col[3] == 'PRI',
                        'default': col[4],
                        'extra': col[5]
                    })
                    
        except Exception as e:
            print(f"Schema fetch error: {e}")
            return None
            
        finally:
            cursor.close()
            
        return schema_info
    
    def execute_query(self, query):
        """Execute SQL query and return results"""
        if not self.connection:
            return None, "No database connection"
            
        try:
            # Use pandas to execute query and get results
            df = pd.read_sql_query(query, self.connection)
            
            # Convert datetime objects to strings for JSON serialization
            for col in df.select_dtypes(include=['datetime64', 'datetime']).columns:
                df[col] = df[col].astype(str)
            
            return df.to_dict('records'), None
            
        except Exception as e:
            error_msg = str(e)
            print(f"Query execution error: {error_msg}")
            return None, error_msg
    
    def test_connection(self):
        """Test if connection is still alive"""
        if not self.connection:
            return False
        try:
            self.connection.ping(reconnect=True)
            return True
        except:
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
