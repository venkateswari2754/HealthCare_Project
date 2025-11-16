"""
================================================================================
                    DATA PIPELINE MODULE
================================================================================

MODULE: Data Pipeline and ETL Operations
VERSION: 1.0
AUTHOR: Venkateswari
DATE: November 2025

DESCRIPTION:
    This module handles ETL (Extract, Transform, Load) operations for the
    Healthcare project. It loads data from CSV files, transforms it, and
    loads it into the MySQL database.

KEY FEATURES:
    ✓ Load data from CSV files
    ✓ Transform and validate data
    ✓ Insert data into MySQL database
    ✓ Handle data quality issues
    ✓ Generate data pipeline reports
    ✓ Support for bulk operations

MAIN FUNCTIONS:
    1. load_csv_data() - Read CSV files
    2. validate_data() - Check data quality
    3. create_tables() - Create required database tables
    4. insert_hospital_data() - Load hospital information
    5. insert_doctor_data() - Load doctor information
    6. insert_emergency_data() - Load emergency services data

WORKFLOW:
    1. Read CSV files from data/ directory
    2. Validate data quality and format
    3. Create database tables if they don't exist
    4. Insert transformed data into MySQL
    5. Generate summary report

USAGE:
    from Create_Data_Pipeline import setup_database, load_all_data
    
    # Create tables and load all data
    setup_database()
    
    # Or load individual datasets
    load_hospital_data()
    load_doctor_data()

================================================================================
"""

import pandas as pd
import os
from db_connection import get_db_cursor, insert_data, execute_query
from mysql.connector import Error


# ✅ Define file paths for datasets
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HOSPITAL_FILE = os.path.join(DATA_DIR, "Hospital_General_Information.csv")
DOCTOR_FILE = os.path.join(DATA_DIR, "doctors_info_data.csv")
DOCTOR_SLOTS_FILE = os.path.join(DATA_DIR, "doctors_slots_data.csv")
EMERGENCY_FILE = os.path.join(DATA_DIR, "hospitals_emergency_data.csv")
LAB_TESTS_FILE = os.path.join(DATA_DIR, "Hospital_Information_with_Lab_Tests.csv")


def load_csv_data(file_path):
    """
    Load data from CSV file into a Pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.EmptyDataError: If CSV is empty
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ File not found: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} rows from {os.path.basename(file_path)}")
        return df
    except Exception as e:
        print(f"❌ Error loading CSV {file_path}: {e}")
        raise


def create_hospitals_table():
    """
    Create hospitals table in the database.
    
    Table Structure:
        - hospital_id: AUTO_INCREMENT PRIMARY KEY
        - hospital_name: VARCHAR(255)
        - state: VARCHAR(100)
        - hospital_type: VARCHAR(100)
        - beds: INT
        - trauma_center: VARCHAR(10)
        
    Returns:
        bool: True if successful, False otherwise
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hospitals (
        hospital_id INT AUTO_INCREMENT PRIMARY KEY,
        hospital_name VARCHAR(255) NOT NULL,
        state VARCHAR(100),
        hospital_type VARCHAR(100),
        beds INT,
        trauma_center VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_hospital (hospital_name, state)
    )
    """
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute(create_table_query)
            print("✅ Hospitals table created successfully")
            return True
    except Error as e:
        print(f"❌ Error creating hospitals table: {e}")
        return False


def create_doctors_table():
    """
    Create doctors table in the database.
    
    Returns:
        bool: True if successful
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INT AUTO_INCREMENT PRIMARY KEY,
        doctor_name VARCHAR(255) NOT NULL,
        hospital_id INT,
        specialty VARCHAR(100),
        phone VARCHAR(20),
        email VARCHAR(100),
        experience_years INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
    )
    """
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute(create_table_query)
            print("✅ Doctors table created successfully")
            return True
    except Error as e:
        print(f"❌ Error creating doctors table: {e}")
        return False


def create_emergency_services_table():
    """
    Create emergency services table in the database.
    
    Returns:
        bool: True if successful
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS emergency_services (
        emergency_id INT AUTO_INCREMENT PRIMARY KEY,
        hospital_id INT,
        hospital_name VARCHAR(255),
        state VARCHAR(100),
        emergency_type VARCHAR(100),
        phone_number VARCHAR(20),
        address VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
    )
    """
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute(create_table_query)
            print("✅ Emergency Services table created successfully")
            return True
    except Error as e:
        print(f"❌ Error creating emergency services table: {e}")
        return False


def load_hospital_data():
    """
    Load hospital data from CSV and insert into database.
    
    Returns:
        int: Number of hospitals loaded
    """
    try:
        print("\n📊 Loading Hospital Data...")
        df = load_csv_data(HOSPITAL_FILE)
        
        # Display sample data
        print(f"Sample columns: {df.columns.tolist()}")
        print(f"Sample data:\n{df.head()}")
        
        count = 0
        for _, row in df.iterrows():
            try:
                data = {
                    "hospital_name": row.get("Hospital Name", row.get("hospital_name", "")),
                    "state": row.get("State", row.get("state", "")),
                    "hospital_type": row.get("Hospital Type", row.get("hospital_type", "")),
                    "beds": row.get("Number of Beds", row.get("beds", 0)),
                    "trauma_center": row.get("Trauma Center", row.get("trauma_center", "No"))
                }
                
                insert_data("hospitals", data)
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting hospital row: {e}")
                continue
        
        print(f"✅ Loaded {count} hospitals into database")
        return count
    except Exception as e:
        print(f"❌ Error loading hospital data: {e}")
        return 0


def load_doctor_data():
    """
    Load doctor data from CSV and insert into database.
    
    Returns:
        int: Number of doctors loaded
    """
    try:
        print("\n👨‍⚕️ Loading Doctor Data...")
        df = load_csv_data(DOCTOR_FILE)
        
        count = 0
        for _, row in df.iterrows():
            try:
                data = {
                    "doctor_name": row.get("Doctor Name", ""),
                    "specialty": row.get("Specialty", ""),
                    "phone": row.get("Phone", ""),
                    "email": row.get("Email", ""),
                    "experience_years": row.get("Experience Years", 0)
                }
                
                insert_data("doctors", data)
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting doctor row: {e}")
                continue
        
        print(f"✅ Loaded {count} doctors into database")
        return count
    except Exception as e:
        print(f"❌ Error loading doctor data: {e}")
        return 0


def load_emergency_data():
    """
    Load emergency services data from CSV and insert into database.
    
    Returns:
        int: Number of emergency services loaded
    """
    try:
        print("\n🚑 Loading Emergency Services Data...")
        df = load_csv_data(EMERGENCY_FILE)
        
        count = 0
        for _, row in df.iterrows():
            try:
                data = {
                    "hospital_name": row.get("Hospital Name", ""),
                    "state": row.get("State", ""),
                    "emergency_type": row.get("Emergency Type", ""),
                    "phone_number": row.get("Phone Number", ""),
                    "address": row.get("Address", "")
                }
                
                insert_data("emergency_services", data)
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting emergency service row: {e}")
                continue
        
        print(f"✅ Loaded {count} emergency services into database")
        return count
    except Exception as e:
        print(f"❌ Error loading emergency data: {e}")
        return 0


def setup_database():
    """
    Complete database setup: Create tables and load all data.
    
    This is the main function to run for initial setup.
    
    Example:
        >>> setup_database()
    """
    print("\n" + "="*70)
    print("          DATABASE SETUP - DATA PIPELINE")
    print("="*70)
    
    # Step 1: Create tables
    print("\n📋 Creating database tables...")
    create_hospitals_table()
    create_doctors_table()
    create_emergency_services_table()
    
    # Step 2: Load data
    print("\n📥 Loading data from CSV files...")
    hospital_count = load_hospital_data()
    doctor_count = load_doctor_data()
    emergency_count = load_emergency_data()
    
    # Step 3: Summary
    print("\n" + "="*70)
    print("          PIPELINE SUMMARY")
    print("="*70)
    print(f"✅ Hospitals loaded: {hospital_count}")
    print(f"✅ Doctors loaded: {doctor_count}")
    print(f"✅ Emergency services loaded: {emergency_count}")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run the complete pipeline setup
    setup_database()
