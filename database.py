"""
Database initialization and management module.
Creates and populates a sample SQLite database with business data.
"""

import sqlite3
import pandas as pd
from typing import List, Tuple, Optional
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database operations and schema."""
    
    def __init__(self, db_path: str = "business_data.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        
    def connect(self) -> sqlite3.Connection:
        """Establish database connection."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.connection
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Create tables and populate with sample data."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Drop existing tables if they exist
        cursor.execute("DROP TABLE IF EXISTS Orders")
        cursor.execute("DROP TABLE IF EXISTS Products")
        cursor.execute("DROP TABLE IF EXISTS Customers")
        
        # Create Customers table
        cursor.execute("""
            CREATE TABLE Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                region TEXT NOT NULL,
                registration_date DATE NOT NULL
            )
        """)
        
        # Create Products table
        cursor.execute("""
            CREATE TABLE Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock_quantity INTEGER NOT NULL
            )
        """)
        
        # Create Orders table
        cursor.execute("""
            CREATE TABLE Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                order_date DATE NOT NULL,
                total_amount REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            )
        """)
        
        # Insert sample customers
        customers_data = [
            ("Alice Johnson", "alice.j@email.com", "North", "2023-01-15"),
            ("Bob Smith", "bob.smith@email.com", "South", "2023-02-20"),
            ("Carol Williams", "carol.w@email.com", "East", "2023-03-10"),
            ("David Brown", "david.b@email.com", "West", "2023-04-05"),
            ("Emma Davis", "emma.d@email.com", "North", "2023-05-12"),
            ("Frank Miller", "frank.m@email.com", "South", "2023-06-18"),
            ("Grace Wilson", "grace.w@email.com", "East", "2023-07-22"),
            ("Henry Moore", "henry.m@email.com", "West", "2023-08-30"),
        ]
        
        cursor.executemany(
            "INSERT INTO Customers (name, email, region, registration_date) VALUES (?, ?, ?, ?)",
            customers_data
        )
        
        # Insert sample products
        products_data = [
            ("Laptop", "Electronics", 899.99, 50),
            ("Smartphone", "Electronics", 599.99, 100),
            ("Desk Chair", "Furniture", 199.99, 75),
            ("Standing Desk", "Furniture", 399.99, 30),
            ("Wireless Mouse", "Electronics", 29.99, 200),
            ("Keyboard", "Electronics", 79.99, 150),
            ("Monitor", "Electronics", 299.99, 60),
            ("Bookshelf", "Furniture", 149.99, 40),
            ("Office Lamp", "Furniture", 49.99, 120),
            ("Webcam", "Electronics", 89.99, 80),
        ]
        
        cursor.executemany(
            "INSERT INTO Products (product_name, category, price, stock_quantity) VALUES (?, ?, ?, ?)",
            products_data
        )
        
        # Insert sample orders
        orders_data = [
            (1, 1, 2, "2023-09-01", 1799.98),
            (1, 2, 1, "2023-09-02", 599.99),
            (2, 3, 1, "2023-09-03", 199.99),
            (2, 4, 1, "2023-09-04", 399.99),
            (3, 1, 1, "2023-09-05", 899.99),
            (3, 5, 3, "2023-09-05", 89.97),
            (4, 7, 2, "2023-09-06", 599.98),
            (5, 2, 2, "2023-09-07", 1199.98),
            (5, 6, 1, "2023-09-08", 79.99),
            (6, 8, 1, "2023-09-09", 149.99),
            (7, 1, 3, "2023-09-10", 2699.97),
            (7, 10, 2, "2023-09-11", 179.98),
            (8, 3, 2, "2023-09-12", 399.98),
            (1, 9, 4, "2023-09-13", 199.96),
            (2, 7, 1, "2023-09-14", 299.99),
            (3, 4, 1, "2023-09-15", 399.99),
            (4, 1, 1, "2023-09-16", 899.99),
            (5, 3, 3, "2023-09-17", 599.97),
            (6, 5, 5, "2023-09-18", 149.95),
            (7, 6, 2, "2023-09-19", 159.98),
        ]
        
        cursor.executemany(
            "INSERT INTO Orders (customer_id, product_id, quantity, order_date, total_amount) VALUES (?, ?, ?, ?, ?)",
            orders_data
        )
        
        conn.commit()
        print("✅ Database initialized successfully with sample data!")
    
    def get_schema_info(self) -> str:
        """
        Retrieve database schema information for RAG context.
        
        Returns:
            Formatted string containing table schemas
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema_info = "DATABASE SCHEMA:\n\n"
        
        for table in tables:
            table_name = table[0]
            schema_info += f"Table: {table_name}\n"
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema_info += "Columns:\n"
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = " (PRIMARY KEY)" if col[5] else ""
                is_notnull = " NOT NULL" if col[3] else ""
                schema_info += f"  - {col_name}: {col_type}{is_pk}{is_notnull}\n"
            
            # Get foreign key information
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fks = cursor.fetchall()
            
            if fks:
                schema_info += "Foreign Keys:\n"
                for fk in fks:
                    schema_info += f"  - {fk[3]} -> {fk[2]}({fk[4]})\n"
            
            schema_info += "\n"
        
        return schema_info
    
    def execute_query(self, query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Execute SQL query safely and return results.
        
        Args:
            query: SQL query string
            
        Returns:
            Tuple of (DataFrame with results, error message if any)
        """
        try:
            conn = self.connect()
            
            # Execute query and fetch results
            df = pd.read_sql_query(query, conn)
            
            return df, None
            
        except Exception as e:
            error_msg = f"Query execution error: {str(e)}"
            return None, error_msg
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """
        Get sample rows from a table.
        
        Args:
            table_name: Name of the table
            limit: Number of rows to return
            
        Returns:
            DataFrame with sample data
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        df, error = self.execute_query(query)
        
        if error:
            return pd.DataFrame()
        
        return df


def initialize_db():
    """Helper function to initialize database."""
    db = DatabaseManager()
    db.initialize_database()
    db.close()
    return db


if __name__ == "__main__":
    # Initialize database when run directly
    initialize_db()
    print("\n✅ Database setup complete!")
    
    # Display schema info
    db = DatabaseManager()
    print("\n" + "="*60)
    print(db.get_schema_info())
    print("="*60)
    
    # Show sample data
    print("\n📊 SAMPLE DATA:\n")
    print("Customers:")
    print(db.get_sample_data("Customers"))
    print("\nProducts:")
    print(db.get_sample_data("Products"))
    print("\nOrders:")
    print(db.get_sample_data("Orders"))
    
    db.close()
