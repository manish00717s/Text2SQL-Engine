"""
SQL Generation module using LangChain and OpenAI/Azure OpenAI.
Implements RAG approach for Text-to-SQL conversion.
"""

import os
import re
from typing import Tuple, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()


class SQLGenerator:
    """Generates SQL queries from natural language using LLM with RAG."""
    
    def __init__(self, schema_info: str, model_name: str = None):
        """
        Initialize SQL generator with database schema context.
        
        Args:
            schema_info: Database schema information for RAG context
            model_name: OpenAI model to use (defaults to env variable or gpt-4-turbo-preview)
        """
        self.schema_info = schema_info
        
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file.")
        
        # Get model name from env or use default
        if model_name is None:
            model_name = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        # Check if using Azure OpenAI
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        
        # Initialize LLM (Azure or OpenAI)
        if azure_endpoint and azure_deployment:
            # Using Azure OpenAI
            self.llm = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                azure_deployment=azure_deployment,
                api_key=api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                temperature=0
            )
        else:
            # Using standard OpenAI
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0,  # Deterministic output for SQL generation
                api_key=api_key
            )
        
        # Create prompt template with schema injection (RAG approach)
        self.prompt_template = PromptTemplate(
            input_variables=["schema", "question"],
            template="""You are an expert SQL analyst working with a SQLite database.

{schema}

IMPORTANT INSTRUCTIONS:
1. Write ONLY the SQL query - no explanations or markdown formatting
2. Use proper SQLite syntax
3. Ensure the query is executable and safe (read-only SELECT statements)
4. Use appropriate JOINs when multiple tables are involved
5. Use aggregate functions (COUNT, SUM, AVG, etc.) when needed
6. Apply proper filtering, grouping, and ordering
7. Limit results when asking for "top" items
8. Do NOT include ```sql or ``` markers

USER QUESTION: {question}

SQL QUERY:"""
        )
        
        # Create the chain using LCEL (LangChain Expression Language)
        self.chain = self.prompt_template | self.llm
    
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question.
        
        Args:
            question: Natural language question
            
        Returns:
            Generated SQL query string
        """
        try:
            # Generate SQL using the chain (LCEL)
            response = self.chain.invoke({
                "schema": self.schema_info,
                "question": question
            })
            
            # Extract content from AIMessage
            if hasattr(response, 'content'):
                sql_text = response.content
            else:
                sql_text = str(response)
            
            # Clean up the response
            sql_query = self._clean_sql_output(sql_text)
            
            return sql_query
            
        except Exception as e:
            raise Exception(f"Error generating SQL: {str(e)}")
    
    def _clean_sql_output(self, output: str) -> str:
        """
        Clean and format SQL output from LLM.
        
        Args:
            output: Raw output from LLM
            
        Returns:
            Cleaned SQL query
        """
        # Remove markdown code blocks if present
        output = re.sub(r'```sql\s*', '', output)
        output = re.sub(r'```\s*', '', output)
        
        # Remove extra whitespace and newlines
        output = ' '.join(output.split())
        
        # Ensure query ends with semicolon
        output = output.strip()
        if not output.endswith(';'):
            output += ';'
        
        return output
    
    def generate_summary(self, question: str, query: str, result_count: int) -> str:
        """
        Generate natural language summary of query results.
        
        Args:
            question: Original user question
            query: Generated SQL query
            result_count: Number of rows returned
            
        Returns:
            Natural language summary
        """
        summary_prompt = f"""Given the user's question and the query results, provide a brief natural language summary.

USER QUESTION: {question}

SQL QUERY: {query}

NUMBER OF RESULTS: {result_count}

Provide a 1-2 sentence summary explaining what the data shows. Be concise and business-focused.

SUMMARY:"""
        
        try:
            response = self.llm.invoke(summary_prompt)
            if hasattr(response, 'content'):
                return response.content.strip()
            return str(response).strip()
        except Exception as e:
            return f"Query returned {result_count} result(s)."


class QueryValidator:
    """Validates SQL queries for safety and correctness."""
    
    @staticmethod
    def is_safe_query(query: str) -> Tuple[bool, Optional[str]]:
        """
        Check if query is safe to execute (read-only).
        
        Args:
            query: SQL query to validate
            
        Returns:
            Tuple of (is_safe, error_message)
        """
        query_upper = query.upper().strip()
        
        # List of dangerous keywords
        dangerous_keywords = [
            'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER',
            'CREATE', 'TRUNCATE', 'REPLACE', 'MERGE'
        ]
        
        # Check for dangerous operations
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Query contains forbidden operation: {keyword}"
        
        # Must be a SELECT statement
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        return True, None
    
    @staticmethod
    def validate_syntax(query: str) -> Tuple[bool, Optional[str]]:
        """
        Basic syntax validation.
        
        Args:
            query: SQL query to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or len(query.strip()) == 0:
            return False, "Query is empty"
        
        # Check for basic SQL structure
        if 'SELECT' not in query.upper():
            return False, "Query must contain SELECT statement"
        
        # Check for balanced parentheses
        if query.count('(') != query.count(')'):
            return False, "Unbalanced parentheses in query"
        
        return True, None


if __name__ == "__main__":
    # Test SQL generator
    from database import DatabaseManager
    
    print("Testing SQL Generator...\n")
    
    # Get schema info
    db = DatabaseManager()
    schema = db.get_schema_info()
    
    # Initialize generator
    try:
        generator = SQLGenerator(schema)
        
        # Test questions
        test_questions = [
            "Show me the top 3 customers who spent the most money",
            "What are the total sales by region?",
            "Which products are low in stock (less than 50 units)?",
            "Show me all electronics products with their prices"
        ]
        
        for question in test_questions:
            print(f"Q: {question}")
            sql = generator.generate_sql(question)
            print(f"SQL: {sql}\n")
            
            # Validate
            is_safe, error = QueryValidator.is_safe_query(sql)
            print(f"Safe: {is_safe}")
            if error:
                print(f"Error: {error}")
            print("-" * 60 + "\n")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Created .env file with OPENAI_API_KEY")
        print("2. Installed all requirements: pip install -r requirements.txt")
    
    db.close()
