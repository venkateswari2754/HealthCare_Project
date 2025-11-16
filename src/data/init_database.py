"""
================================================================================
                    DATABASE INITIALIZATION SCRIPT
================================================================================

MODULE: Database Initialization and Setup
VERSION: 1.0
AUTHOR: Venkateswari
DATE: November 2025

DESCRIPTION:
    This script initializes the MySQL database for the Healthcare project.
    It creates the database if it doesn't exist and runs the data pipeline.

WORKFLOW:
    1. Connect to MySQL server (without specifying database)
    2. Create the healthcare database if it doesn't exist
    3. Run the data pipeline to create tables and load data

USAGE:
    python init_database.py

================================================================================
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "healthcare_db")
DB_PORT = int(os.getenv("DB_PORT", 3306))


def create_database():
    """
    Create the healthcare database if it doesn't exist.
    
    Returns:
        bool: True if database created or already exists, False otherwise
    """
    try:
        # Connect to MySQL without specifying a database
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        cursor = db.cursor()
        
        # Create database if it doesn't exist
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        cursor.execute(create_db_query)
        print(f"✅ Database '{DB_NAME}' created or already exists")
        
        cursor.close()
        db.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False


def main():
    """
    Main initialization function.
    """
    print("\n" + "="*70)
    print("          DATABASE INITIALIZATION")
    print("="*70)
    
    print(f"\nMySQL Connection Details:")
    print(f"  Host: {DB_HOST}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}")
    print(f"  Port: {DB_PORT}")
    print("-"*70)
    
    # Step 1: Create database
    print("\n📦 Step 1: Creating database...")
    if not create_database():
        print("❌ Failed to create database. Exiting.")
        sys.exit(1)
    
    # Step 2: Run data pipeline
    print("\n📋 Step 2: Running data pipeline...")
    try:
        # Import after database is created
        from data_pipeline import setup_database
        setup_database()
        print("\n✅ Data pipeline completed successfully!")
    except Exception as e:
        print(f"❌ Error running data pipeline: {e}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("          INITIALIZATION COMPLETE ✅")
    print("="*70)
    print("\nYour healthcare database is now ready to use!")
    print(f"Database: {DB_NAME}")
    print(f"Tables: hospitals, doctors, emergency_services")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
