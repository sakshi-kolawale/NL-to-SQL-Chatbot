import google.generativeai as genai
from config import Config
import re

class NLToSQLConverter:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        # Use a valid model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_sql(self, natural_language_query, schema_info):
        """Convert natural language to MySQL query"""
        
        if not schema_info:
            return None, "No schema information available"
        
        schema_text = self._format_schema(schema_info)
        
        prompt = f"""
You are an expert MySQL query generator. Given a database schema and a natural language question, generate a precise MySQL query.

Database Schema:
{schema_text}

Natural Language Query: {natural_language_query}

Instructions:
1. Generate ONLY the SQL query, no explanations or comments
2. Use proper MySQL syntax
3. Handle JOINs, aggregations, and filtering appropriately
4. Use LIMIT clause when asking for "top N" or "first N" results
5. Be case-insensitive for column matching
6. Use backticks for table/column names if needed
7. Return only executable MySQL query
8. Do not include semicolon at the end

Generate the MySQL query:
        """
        
        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            sql_query = self._clean_sql_response(sql_query)
            
            if not sql_query:
                return None, "Failed to generate valid SQL query"
                
            return sql_query, None
            
        except Exception as e:
            return None, f"Error generating SQL: {str(e)}"
    
    def _format_schema(self, schema_info):
        schema_text = ""
        for table_name, columns in schema_info.items():
            schema_text += f"\n=== Table: `{table_name}` ===\n"
            for col in columns:
                pk_indicator = " (PRIMARY KEY)" if col['primary_key'] else ""
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default_val = f" DEFAULT {col['default']}" if col['default'] else ""
                extra = f" {col['extra']}" if col['extra'] else ""
                schema_text += f"  {col['column']}: {col['type']} {nullable}{pk_indicator}{default_val}{extra}\n"
        return schema_text
    
    def _clean_sql_response(self, response):
        response = re.sub(r'```sql\s*', '', response, flags=re.IGNORECASE)
        response = re.sub(r'```', '', response)
        response = re.sub(r'^(sql query:|query:|mysql query:)', '', response, flags=re.IGNORECASE)
        
        sql_lines = []
        for line in response.split('\n'):
            line = line.strip()
            if line and not line.startswith('--') and not line.startswith('#'):
                sql_lines.append(line)
        
        sql_query = ' '.join(sql_lines).strip()
        sql_query = sql_query.rstrip(';')
        return sql_query if sql_query else None


# import google.generativeai as genai
# from config import Config
# import re

# class NLToSQLConverter:
#     def __init__(self):
#         genai.configure(api_key=Config.GOOGLE_API_KEY)
#         self.model = genai.GenerativeModel('gemini-pro')
        
#     def generate_sql(self, natural_language_query, schema_info):
#         """Convert natural language to MySQL query"""
        
#         if not schema_info:
#             return None, "No schema information available"
        
#         # Format schema information
#         schema_text = self._format_schema(schema_info)
        
#         prompt = f"""
# You are an expert MySQL query generator. Given a database schema and a natural language question, generate a precise MySQL query.

# Database Schema:
# {schema_text}

# Natural Language Query: {natural_language_query}

# Instructions:
# 1. Generate ONLY the SQL query, no explanations or comments
# 2. Use proper MySQL syntax
# 3. Handle JOINs, aggregations, and filtering appropriately
# 4. Use LIMIT clause when asking for "top N" or "first N" results
# 5. Be case-insensitive for column matching
# 6. Use backticks for table/column names if needed
# 7. Return only executable MySQL query
# 8. Do not include semicolon at the end

# Generate the MySQL query:
#         """
        
#         try:
#             response = self.model.generate_content(prompt)
#             sql_query = response.text.strip()
            
#             # Clean the response to get only SQL
#             sql_query = self._clean_sql_response(sql_query)
            
#             if not sql_query:
#                 return None, "Failed to generate valid SQL query"
                
#             return sql_query, None
            
#         except Exception as e:
#             return None, f"Error generating SQL: {str(e)}"
    
#     def _format_schema(self, schema_info):
#         """Format schema information for the prompt"""
#         schema_text = ""
#         for table_name, columns in schema_info.items():
#             schema_text += f"\n=== Table: `{table_name}` ===\n"
#             for col in columns:
#                 pk_indicator = " (PRIMARY KEY)" if col['primary_key'] else ""
#                 nullable = "NULL" if col['nullable'] else "NOT NULL"
#                 default_val = f" DEFAULT {col['default']}" if col['default'] else ""
#                 extra = f" {col['extra']}" if col['extra'] else ""
                
#                 schema_text += f"  {col['column']}: {col['type']} {nullable}{pk_indicator}{default_val}{extra}\n"
        
#         return schema_text
    
#     def _clean_sql_response(self, response):
#         """Clean the AI response to extract only SQL"""
#         # Remove markdown code blocks
#         response = re.sub(r'```sql\s*', '', response, flags=re.IGNORECASE)
#         response = re.sub(r'```', '', response)
        
#         # Remove common prefixes
#         response = re.sub(r'^(sql query:|query:|mysql query:)', '', response, flags=re.IGNORECASE)
        
#         # Remove comments and extra whitespace
#         lines = response.split('\n')
#         sql_lines = []
        
#         for line in lines:
#             line = line.strip()
#             # Skip empty lines and comments
#             if line and not line.startswith('--') and not line.startswith('#'):
#                 sql_lines.append(line)
        
#         # Join lines and clean up
#         sql_query = ' '.join(sql_lines).strip()
        
#         # Remove trailing semicolon if present
#         sql_query = sql_query.rstrip(';')
        
#         return sql_query if sql_query else None


# import google.generativeai as genai
# from config import Config
# import json

# class NLToSQLConverter:
#     def __init__(self):
#         genai.configure(api_key=Config.GOOGLE_API_KEY)
#         self.model = genai.GenerativeModel('gemini-pro')
        
#     def generate_sql(self, natural_language_query, schema_info):
#         """Convert natural language to SQL query"""
        
#         # Format schema information
#         schema_text = self._format_schema(schema_info)
        
#         prompt = f"""
#         You are an expert SQL query generator. Given a database schema and a natural language question, 
#         generate a precise SQL query.

#         Database Schema:
#         {schema_text}

#         Natural Language Query: {natural_language_query}

#         Instructions:
#         1. Generate ONLY the SQL query, no explanations
#         2. Use proper SQL syntax for the given schema
#         3. Handle aggregations, joins, and filtering appropriately
#         4. Use LIMIT clause when asking for "top N" results
#         5. Be case-insensitive for column matching
#         6. Return only executable SQL

#         SQL Query:
#         """
        
#         try:
#             response = self.model.generate_content(prompt)
#             sql_query = response.text.strip()
            
#             # Clean the response to get only SQL
#             sql_query = self._clean_sql_response(sql_query)
            
#             return sql_query, None
#         except Exception as e:
#             return None, f"Error generating SQL: {str(e)}"
    
#     def _format_schema(self, schema_info):
#         """Format schema information for the prompt"""
#         schema_text = ""
#         for table_name, columns in schema_info.items():
#             schema_text += f"\nTable: {table_name}\n"
#             for col in columns:
#                 pk_indicator = " (PRIMARY KEY)" if col['primary_key'] else ""
#                 nullable = "NULL" if col['nullable'] else "NOT NULL"
#                 schema_text += f"  - {col['column']}: {col['type']} {nullable}{pk_indicator}\n"
#         return schema_text
    
#     def _clean_sql_response(self, response):
#         """Clean the AI response to extract only SQL"""
#         # Remove common prefixes/suffixes
#         response = response.replace('```sql', '').replace('```', '')
#         response = response.replace('SQL Query:', '').strip()
        
#         # Take only the first statement if multiple
#         lines = response.split('\n')
#         sql_lines = []
#         for line in lines:
#             line = line.strip()
#             if line and not line.startswith('--') and not line.startswith('#'):
#                 sql_lines.append(line)
        
#         return ' '.join(sql_lines)