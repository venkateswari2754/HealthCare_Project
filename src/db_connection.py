"""
================================================================================
                    DATABASE CONNECTION MODULE
================================================================================

MODULE: Database Configuration and Connection Management
VERSION: 1.0
AUTHOR: Venkateswari
DATE: November 2025

DESCRIPTION:
    This module handles all database connections to MySQL using mysql-connector.
    Credentials are securely managed through environment variables (.env file).
    Provides helper functions for common database operations with proper error
    handling and connection management.

KEY FEATURES:
    ✓ Secure credential management using environment variables
    ✓ Connection pooling and error handling
    ✓ Helper functions for common database operations
    ✓ Context managers for safe connection handling
    ✓ Transaction management with rollback support
    ✓ Parameterized queries to prevent SQL injection

DEPENDENCIES:
    • mysql-connector-python: MySQL database connector
    • python-dotenv: Environment variable management
    • sqlalchemy: SQL toolkit (optional for advanced use)

CONFIGURATION:
    Add the following to your .env file:
    
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=your_password
    DB_NAME=healthcare_db
    DB_PORT=3306

USAGE EXAMPLES:

    1. Simple Connection:
        >>> from db_connection import get_db_connection
        >>> db = get_db_connection()
        >>> cursor = db.cursor()
        >>> cursor.execute("SELECT * FROM hospitals")
        >>> cursor.close()
        >>> db.close()

    2. Using Context Manager (Recommended):
        >>> from db_connection import get_db_cursor
        >>> with get_db_cursor() as cursor:
        ...     cursor.execute("SELECT * FROM hospitals WHERE state = %s", ("CA",))
        ...     results = cursor.fetchall()

    3. Test Connection:
        >>> from db_connection import test_connection
        >>> if test_connection():
        ...     print("Database is ready to use!")

================================================================================
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

# ✅ Database Configuration (Retrieved from environment variables)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "healthcare_db"),
    "port": int(os.getenv("DB_PORT", 3306))
}


def get_db_connection():
    """
    Create and return a database connection.
    
    This function establishes a connection to MySQL using credentials
    from environment variables. It verifies the connection is active
    before returning it.
    
    Returns:
        mysql.connector.MySQLConnection: Active database connection
        
    Raises:
        mysql.connector.Error: If connection fails
        
    Example:
        >>> db = get_db_connection()
        >>> cursor = db.cursor()
        >>> cursor.execute("SELECT * FROM hospitals")
        >>> results = cursor.fetchall()
        >>> cursor.close()
        >>> db.close()
    """
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        if db.is_connected():
            print(f"✅ Successfully connected to MySQL database: {DB_CONFIG['database']}")
            return db
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        raise


def close_db_connection(db):
    """
    Safely close a database connection.
    
    Checks if connection is active before closing to avoid errors.
    
    Args:
        db (mysql.connector.MySQLConnection): Database connection to close
        
    Example:
        >>> db = get_db_connection()
        >>> # ... perform operations ...
        >>> close_db_connection(db)
        ✅ Database connection closed successfully.
    """
    if db and db.is_connected():
        db.close()
        print("✅ Database connection closed successfully.")


@contextmanager
def get_db_cursor():
    """
    Context manager for database cursor operations.
    Automatically handles connection and cursor cleanup.
    Ensures transactions are committed or rolled back properly.
    
    Yields:
        mysql.connector.MySQLCursor: Database cursor (returns dicts)
        
    Raises:
        mysql.connector.Error: If database operations fail
        
    Example:
        >>> with get_db_cursor() as cursor:
        ...     cursor.execute("SELECT * FROM hospitals")
        ...     results = cursor.fetchall()
        ...     for row in results:
        ...         print(row)
        
        >>> # Insert example
        >>> with get_db_cursor() as cursor:
        ...     query = "INSERT INTO hospitals (name, state) VALUES (%s, %s)"
        ...     cursor.execute(query, ("City Hospital", "CA"))
    """
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)  # Return results as dictionaries
        yield cursor
        db.commit()
        print("✅ Database transaction committed successfully.")
    except Error as e:
        if db:
            db.rollback()
            print("⚠️ Database transaction rolled back due to error.")
        print(f"❌ Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()


def test_connection():
    """
    Test the database connection.
    
    Useful for verifying credentials and connectivity at startup.
    Attempts to connect, verify, and immediately disconnect.
    
    Returns:
        bool: True if connection is successful, False otherwise
        
    Example:
        >>> if test_connection():
        ...     print("Database is ready to use!")
        ... else:
        ...     print("Failed to connect to database")
    """
    try:
        db = get_db_connection()
        if db.is_connected():
            print("✅ Database connection test PASSED!")
            db.close()
            return True
    except Error as e:
        print(f"❌ Database connection test FAILED: {e}")
        return False


def execute_query(query, params=None):
    """
    Execute a SELECT query and return results.
    
    Uses parameterized queries to prevent SQL injection.
    Handles connection lifecycle automatically.
    
    Args:
        query (str): SQL SELECT query with %s placeholders for parameters
        params (tuple, optional): Query parameters for parameterized queries
        
    Returns:
        list: List of query results as dictionaries
        
    Raises:
        mysql.connector.Error: If query execution fails
        
    Example:
        >>> results = execute_query(
        ...     "SELECT * FROM hospitals WHERE state = %s",
        ...     ("CA",)
        ... )
        >>> for hospital in results:
        ...     print(hospital['hospital_name'])
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    except Error as e:
        print(f"❌ Query execution failed: {e}")
        raise


def insert_data(table, data):
    """
    Insert data into a table.
    
    Automatically constructs INSERT query from dictionary.
    Uses parameterized queries for security.
    
    Args:
        table (str): Target table name
        data (dict): Dictionary with column names as keys and values to insert
        
    Returns:
        int: ID of the inserted row (lastrowid)
        
    Raises:
        mysql.connector.Error: If insert fails
        
    Example:
        >>> data = {
        ...     "hospital_name": "City Hospital",
        ...     "state": "CA",
        ...     "beds": 300
        ... }
        >>> hospital_id = insert_data("hospitals", data)
        >>> print(f"Inserted hospital with ID: {hospital_id}")
    """
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with get_db_cursor() as cursor:
            cursor.execute(query, tuple(data.values()))
            print(f"✅ Data inserted into {table} successfully")
            return cursor.lastrowid
    except Error as e:
        print(f"❌ Insert failed: {e}")
        raise


def update_data(table, data, where_clause, where_params):
    """
    Update data in a table.
    
    Args:
        table (str): Target table name
        data (dict): Dictionary with column names and new values
        where_clause (str): WHERE clause with %s placeholders
        where_params (tuple): Parameters for WHERE clause
        
    Returns:
        int: Number of rows affected
        
    Example:
        >>> update_data(
        ...     "hospitals",
        ...     {"beds": 350},
        ...     "hospital_id = %s",
        ...     (1,)
        ... )
    """
    try:
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        with get_db_cursor() as cursor:
            cursor.execute(query, tuple(data.values()) + where_params)
            print(f"✅ Data updated in {table} successfully")
            return cursor.rowcount
    except Error as e:
        print(f"❌ Update failed: {e}")
        raise


def delete_data(table, where_clause, where_params):
    """
    Delete data from a table.
    
    Args:
        table (str): Target table name
        where_clause (str): WHERE clause with %s placeholders
        where_params (tuple): Parameters for WHERE clause
        
    Returns:
        int: Number of rows deleted
        
    Example:
        >>> deleted_count = delete_data(
        ...     "hospitals",
        ...     "hospital_id = %s",
        ...     (1,)
        ... )
    """
    try:
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        with get_db_cursor() as cursor:
            cursor.execute(query, where_params)
            print(f"✅ Data deleted from {table} successfully")
            return cursor.rowcount
    except Error as e:
        print(f"❌ Delete failed: {e}")
        raise


if __name__ == "__main__":
    # Test database connection when run as standalone script
    print("\n" + "="*70)
    print("          DATABASE CONNECTION TEST")
    print("="*70)
    print("\nTesting database connection with current configuration...")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"User: {DB_CONFIG['user']}")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Port: {DB_CONFIG['port']}")
    print("-"*70)
    test_connection()
    print("="*70 + "\n")
