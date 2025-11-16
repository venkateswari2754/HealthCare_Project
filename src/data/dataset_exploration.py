

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
# Load dataset files
doctors_info = pd.read_csv('D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\doctors_info_data.csv') # Change the path as per your Colab File
doctors_slots = pd.read_csv('D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\doctors_slots_data.csv') # Change the path as per your Colab File
hospital_general = pd.read_csv('D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\Hospital_General_Information.csv') # Change the path as per your Colab File
hospital_lab_tests = pd.read_csv('D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\Hospital_Information_with_Lab_Tests.csv') # Change the path as per your Colab File
hospitals_emergency = pd.read_csv('D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\hospitals_emergency_data.csv') # Change the path as per your Colab File

# Store datasets in a dictionary
datasets = {
    "Doctors Info": doctors_info,
    "Doctors Slots": doctors_slots,
    "Hospital General Information": hospital_general,
    "Hospital Lab Tests": hospital_lab_tests,
    "Hospitals Emergency Data": hospitals_emergency
}
# Display first few rows of each dataset
for name, df in datasets.items():
    print(f"--- {name} ---")
    print(df.head())
    print("\n")
    
    # Checking missing values in each dataset
for name, df in datasets.items():
    print(f"Missing values in {name}:")
    print(df.isnull().sum())
    print("\n")
    
    # Checking basic statistics for numerical columns
for name, df in datasets.items():
    print(f"Statistics for {name}:")
    print(df.describe())
    print("\n")
    
    # Fill missing values with mean for numerical columns
for name, df in datasets.items():
    df.fillna(df.mean(), inplace=True)
    print(f"Filled missing values for {name}")

# # Save cleaned datasets for further processing
# for name, df in datasets.items():
#     df.to_csv(f"D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\{name.replace(' ', '_').lower()}_cleaned.csv", index=False)