"""
================================================================================
                    HOSPITAL COMPARISON AI AGENT
================================================================================

PROJECT: Healthcare AI Assistant - Hospital Comparison Module
AUTHOR: Venkateswari
DATE: November 2025
VERSION: 1.0

DESCRIPTION:
    This module implements an intelligent Hospital Comparison Agent powered by
    LangChain and OpenAI's GPT-4. The agent analyzes hospital data and provides
    personalized hospital recommendations based on user queries and preferences.

KEY FEATURES:
    ✓ AI-Powered Hospital Analysis: Uses GPT-4 to intelligently compare hospitals
    ✓ Pandas DataFrame Integration: Efficiently processes hospital datasets
    ✓ Condition-Specific Recommendations: Tailored advice based on medical needs
    ✓ Multi-Factor Evaluation: Considers expertise, location, facilities, cost, and reviews
    ✓ Natural Language Interface: Users can ask questions in plain English
    ✓ Secure API Key Management: Uses environment variables for credentials

MAIN COMPONENTS:
    1. Data Loading: Reads hospital information from CSV files
    2. LLM Configuration: Initializes GPT-4 model with optimized parameters
    3. Agent Creation: Sets up LangChain pandas agent for data analysis
    4. Query Processing: Handles user questions and generates recommendations

WORKFLOW:
    1. Load hospital dataset into Pandas DataFrame
    2. Initialize ChatOpenAI model with API credentials
    3. Create a specialized agent with healthcare-specific system prompts
    4. Process user queries about hospitals
    5. Return personalized recommendations with detailed analysis

USE CASES:
    • "Which hospital has good medical imaging?"
    • "I have an emergency, please provide phone number of the hospital nearby San Mateo"
    • "Which hospitals have good acute care facilities?"
    • Custom queries about hospital features, specialties, and services

SECURITY CONSIDERATIONS:
    ⚠️  API keys are stored in environment variables (.env file)
    ⚠️  Never hardcode sensitive information in source code
    ⚠️  Use allow_dangerous_code=True carefully (enables code execution)
    ⚠️  Ensure proper sandboxing for production deployments

DEPENDENCIES:
    • pandas: Data manipulation and analysis
    • langchain: AI agent framework
    • langchain_experimental: Pandas DataFrame agent tools
    • langchain_openai: OpenAI integration
    • python-dotenv: Environment variable management
    • httpx: HTTP client for API requests

================================================================================
"""

# Importing necessary libraries for data processing, AI model integration, and agent creation

# Pandas library for handling and processing structured data (CSV, DataFrames)
import pandas as pd

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Importing LangChain's agent toolkit for interacting with Pandas DataFrames
from langchain_experimental.agents import create_pandas_dataframe_agent

# Importing OpenAI's ChatGPT integration for LangChain
from langchain_openai import ChatOpenAI

# Importing predefined agent types from LangChain for different AI-driven workflows
from langchain_classic.agents.agent_types import AgentType

# A high-performance HTTP client for making API requests
import httpx

# Standard Python module for interacting with the operating system (e.g., setting API keys)
import os

# Importing LangChain's components for prompt engineering and structured conversation handling
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

# ✅ Specify the LLM model name (Ensure compatibility with your use case)
LLM_MODEL_NAME = "gpt-4o-2024-08-06"  # Example: Use "gpt-4-turbo" or "gpt-3.5-turbo" if needed.
# ✅ Set your OpenAI API key as an environment variable for authentication

# 🔴 IMPORTANT SECURITY WARNING:
# - Never share this key publicly.
# - Avoid hardcoding in scripts; use environment variables instead.
# - For production deployments, consider using a vault or key management system.

# ✅ Recommended: Setting API Key as an environment variable
API_KEY = os.getenv("OPENAI_API_KEY")  # Retrieve API key from environment variable
if API_KEY:
    os.environ["OPENAI_API_KEY"] = API_KEY  # Safer approach for handling API keys

# ✅ Verifying API Key Setup
if os.getenv("OPENAI_API_KEY"):
    print("✅ OpenAI API Key successfully set as an environment variable.")
else:
    print("❌ Error: API Key not found! Please check your configuration.")
    
# Define the path to the hospital dataset (Ensure the file is in the correct directory)
DATA_PATH = r"D:\Projects\Capstone_Projects\HealthCare\Viswa_Class\GenAIProjects\HealthCare_Project\data\Hospital_General_Information.csv"

# Load the CSV file into a Pandas DataFrame
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    print("❌ Error: File not found! Check the file path.")

# Display the first 5 rows of the dataset to verify successful loading
print(df.head())

# Get a summary of the dataset
print(df.info())

# Display basic statistics of numerical columns
print(df.describe())

# ✅ Initialize the ChatOpenAI model with the given API key and settings
llm = ChatOpenAI(
    openai_api_key=API_KEY,   # 🔑 API key for authentication with OpenAI
    temperature=0,            # 🎯 Set temperature to 0 for deterministic responses (no randomness)
    model=LLM_MODEL_NAME,     # 🚀 Use the specified LLM model (e.g., GPT-4 or other)
    max_tokens=500,           # 📏 Limit the response to 500 tokens to control output length
    http_client=httpx.Client(verify=False)  # ⚡ Use HTTP client with SSL verification disabled (for certain environments)
)

## 💡 **System Message for Healthcare Assistant**


# ✅ Define system message with role-specific instructions for the AI assistant
system_message = SystemMessagePromptTemplate.from_template(
"""
You are a highly skilled healthcare assistant with expertise in comparing hospitals.
Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
You will evaluate hospitals considering factors such as medical specialties, patient reviews, location, cost, accessibility, facilities,
and the availability of treatment for specific conditions.

When comparing hospitals, follow these guidelines:

- Condition-Specific Comparison: Focus on the hospitals' expertise in treating the user's specific health condition
(e.g., heart disease, cancer, etc.).
- Hospital Features: Include details about the hospital's reputation, technology, facilities, specialized care, and any awards or
recognitions.
- Location and Accessibility: Consider the proximity to the user’s location and the convenience of travel.
- Cost and Insurance: Compare the cost of treatment and insurance coverage options offered by the hospitals.
- Patient Feedback: Analyze reviews and ratings to gauge patient satisfaction and outcomes.
- Personalized Recommendation: Provide a clear, personalized suggestion based on the user’s priorities, whether they are medical
expertise, convenience, or cost.


Use "Hospital Type" column to look for good facilities of each hospital.
CAREFULLY look at each column name to understand what to output.
"""
)

prompt = ChatPromptTemplate.from_messages([system_message])

# ✅ Create a Pandas DataFrame Agent for hospital data analysis
agent = create_pandas_dataframe_agent(
    llm,                            # 🔥 The ChatOpenAI model
    df,                             # 📊 The hospital dataset (Pandas DataFrame)
    prompt=prompt,                  # 📜 Custom prompt template for hospital comparison
    verbose=False,                   # 🛑 Disable detailed execution logs
    allow_dangerous_code=True,       # ⚠️ Enable execution of LLM-generated Python code (Use with caution!)
    agent_type=AgentType.OPENAI_FUNCTIONS  # 🤖 Specify OpenAI's function-based agent type
)

print(agent.invoke("Which hospital has good medical imaging")['output'])
print(agent.invoke("I have an emergency, please provide phone number of the hospital nearby san mateo")['output'])
print(agent.invoke("Which hospitals have good acute care facilities")['output'])
