# **Healthsense AI**

> AI-Driven Multi-Agent Healthcare System

## **Introduction & Motivation**

The integration of Generative AI (GenAI) and Large Language Models (LLMs) has significantly transformed the healthcare sector by enabling advanced natural language processing, improving access to medical information, and streamlining patient interactions. AI-powered solutions can assist in diagnosing conditions, providing health recommendations, and offering 24/7 support to patients.

Despite the abundance of medical knowledge, accessing personalized and reliable health information remains a challenge. Many existing healthcare systems provide generic responses and lack contextual awareness. HealthSense AI is designed to bridge this gap by leveraging LLMs and the LangChain framework to offer intelligent, context-aware health information assistance.


## **Problem Statement**

*Develop an intelligent healthcare platform that streamlines medical service discovery and booking by analyzing hospital data, reviews, and healthcare metrics.*

*The system will extract and compare key parameters to help users make informed healthcare decisions.
The solution will feature a comprehensive comparison engine for hospitals and diagnostic centers, an automated slot booking system, and detailed information about medical tests and procedures. The platform will incorporate a user-friendly chat interface to hospital comparisons, explore healthcare metrics, and facilitate seamless appointment scheduling.*

## **Core Objectives**

- **Implement Natural Language Processing (NLP)** – Accurately interpret and process medical terminology.
- **Develop Context-Aware Responses** – Maintain dialogue history for better interaction continuity.
- **Enable Multi-Source Integration** – Pull data from reliable medical knowledge bases.
- **Provide Real-Time Doctor and Hospital Recommendations** – Offer users relevant medical support.
- **Ensure Compliance and Ethical AI** Usage – Maintain HIPAA and GDPR compliance.
## **Key Milestones for 8 Weeks**

1. **Week 1: Project Initialization and Fundamentals**

 - Project overview and architecture discussion
 - Setting up development environment (Python, VS Code, Git)
 - Introduction to Large Language Models; Understanding LLM capabilities and limitations
 - Langchain framework overview including Key components: Chains, Agents, Tools, Memory
2. **Week 2: Database Setup and Synthetic Data**

 - SQL fundamentals review; CREATE TABLE/DATABASE, SELECT
 - Design and implement healthcare database schema in MySQL
 - Create synthetic data generator for realistic healthcare scenarios
 - Develop data insertion pipeline
 - Set up database connections with proper error handling

 3. **Week 3: Hospital Comparison Agent**
 - Setting up development environment
 - Installing necessary libraries
 - Pandas DataFrame operations; Data manipulation and analysis
 - Data preparation for hospital comparison
 - Integration with OpenAI and GPT using Langchain
 - Build CSV-based agent for hospital comparison with custom tools
 - Focus on data validation and error handling

 4. **Week 4: Doctor Information Agent**
 - Data preparation for doctor’s available slots
 - Understand concept of toolkit in context of Langchain
 - Develop SQL toolkit with custom query builders and validation
 - Explore verbose when using toolkits
 - Prompt engineering for data handling

 5. **Week 5:  Emergency and Diagnostics Agents**
  - Create synthetic data generator
  - Data preparation for emergency information and diagnostic information datasets
  - Prompt engineering for data handling
  - Implement the 2 agents - Emergency service and Diagnostic Info

  6. **Week 6: Crew AI Implementation**
  - Understand crew-ai - agent, task, role, tools, backstory, goal
  - Implement single task and single agent flow
  - Understand Crew AI for sequential and parallel agent operations
  - Build routing agent for healthsense.ai

  7. **Week 7: Deployment and API Development**
  - Structure code following clean architecture principles
  - Creating Flask/FastAPI backend
  - Developing frontend interface
  - Create Docker deployment configuration
  - Set up CI/CD pipeline
  - Deploying the application

  8. **Week 8: Final Presentation and Interview Readiness**
 - Creating technical documentation
 - Writing user guides
 - Implementing logging
 - Performance testing
 - Final deployment checks

## **Milestones of Week 2**


---

**Step 1: Setting Up the Environment for your Project**
1. Install Prerequisites:
Python 3.9+ – Required for FastAPI, Streamlit, and OpenAI integration.
VS Code – For coding and debugging.
MongoDB – As the NoSQL database.

2. Install Required Extensions in VS Code:
Python (by Microsoft) – For Python support and debugging.
Pylance – For intelligent code completion.
MongoDB for VS Code – To manage MongoDB directly from VS Code.

#3. Create Project Structure:
#Open VS Code and create the following structure:

healthsense_main/
├── data/
│   ├── Hospital_General_Information.csv
│   ├── Hospital_Information_with_Lab_Tests.csv
│   ├── hospitals_emergency_data.csv
│   ├── crewai_storage.db
├── src/
│   ├── data/
│   ├── DiagnosticInfoAgent.py
│   ├── DoctorInfoAgent.py
│   ├── EmergencyServicesAgent.py
│   ├── HospitalComparisonAgent.py
│   ├── app.py
│   ├── constants.py
│   ├── main.py
│   ├── appointments.db
│   ├── emergency.db
├── static/
│   ├── index.html
├── .gitattributes
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt

# Create virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
env\Scripts\activate
# On Mac/Linux
source env/bin/activate

"""**Step 5: Install Dependencies:**"""

#5. Install Dependencies:
#Create requirements.txt with the following content:

pandas
httpx
crewai
langchain
langchain-core
langchain-community
langchain-openai
langchain-experimental
litellm
fastapi
uvicorn
fastapi
uvicorn
sqlite-utils

#Then install all dependencies:

pip install -r requirements.txt

"""## **Dataset Overview**



---



Besides, make sure you have understood the datasets before moving forward.

Here's a brief description about all the 4 datasets:

### **Hospital General Information Dataset**

*   Contains hospital names, locations, specialties, capacity, and contact details.
*   Used for hospital comparisons and providing relevant hospital recommendations.

*Source: Public healthcare directories and government datasets.*



### **Hospital Information with Lab Tests Dataset**

* Includes details about available lab tests, diagnostic packages, and pricing.
* Used for diagnostic services recommendations and health test comparisons.

*Source: Aggregated medical lab datasets and public health data.*



### **Hospitals Emergency Data Dataset**
* Contains hospital emergency department details, ambulance availability, and response times.
* Used for emergency assistance and directing users to the nearest available emergency services.

*Source: Public emergency response data and hospital records.*



### **Doctor Availability Dataset**

* Contains doctor schedules, specializations, consultation availability, and hospital affiliations.
* Used for doctor appointment recommendations and scheduling.

*Source: Medical institutions and clinic appointment systems.*

These datasets enable HealthSense AI to deliver accurate, data-driven healthcare recommendations.

## **Dataset Exploration[Optional]**

#### **1. Setup Development Environment**
"""
# Install necessary packages
!pip install pandas numpy matplotlib seaborn
