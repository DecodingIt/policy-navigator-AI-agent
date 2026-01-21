# Policy Navigator Agent 🧭

> **⚠️ Submission Note:**
> 
> **1. API Key Configuration:**
> Due to persistent platform errors when attempting to integrate the standard API keys, I was unable to use the provided credentials. To ensure the agent functions correctly for this submission, I have configured the system to use my **own individual API keys**. Please be aware of this when reviewing the configuration.
> 
> **2. Missing Audio Explanation:**
> I sincerely apologize for the delay in this submission. Additionally, due to technical constraints with my recording setup, I was unable to record the audio explanation as originally planned. To compensate, I have provided a detailed **Code Breakdown** section below that explains every part of the implementation in plain English.

---

## 📖 Project Overview
The **Policy Navigator Agent** is an Agentic RAG system built using the **aiXplain SDK**. It is designed to search, analyze, and explain complex government regulations (such as EPA or WHO guidelines).

## 🚀 Features
- **Multi-Source Ingestion:** Scrapes websites and processes CSV datasets.
- **RAG Pipeline:** Uses Vector Search to retrieve context-aware answers.
- **Agentic Tools:**
  - **SQL Tool:** For structured data analysis.
  - **Code Interpreter:** For calculating logic/math.
  - **Notification Tool:** Integrates with Slack/Notion.

---

## 📂 Code Breakdown

Here is a brief explanation of every major snippet in `main.py`:

### 1. Setup & Authentication
```python
import os
os.environ["AIXPLAIN_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"
Explanation: This sets up the environment. We import the necessary libraries and securely set the API key. This key is the "passport" that allows our code to talk to the aiXplain servers.

2. Ingestion Phase (Data Loading)
Python

rag_index = IndexFactory.create(name=index_name, ...)
rag_index.upsert(csv_file_path)
Explanation:

IndexFactory.create: Builds a "Vector Index" (a smart database for AI) where we will store our documents.

upsert: Takes our CSV data and website text and uploads it into that index, making it searchable.

3. Tool Definitions
The agent needs "tools" to do its job. We define them here:

RAG Tool:

Python

rag_tool = AgentFactory.create_model_tool(model=rag_index.id, ...)
What it does: Gives the agent a search engine. It links the agent to the data we just uploaded so it can find answers in the regulations.

SQL Tool:

Python

sql_tool = AgentFactory.create_sql_tool(..., source=csv_file_path)
What it does: Allows the agent to run strict data queries (like "How many policies are in category X?") on the CSV file.

Code Interpreter:

Python

code_tool = PythonInterpreterTool()
What it does: A calculator on steroids. If the agent needs to compute a percentage or solve a math problem found in the policy, it writes Python code here to get the exact answer.

Notification Tool:

Python

notification_tool = ModelFactory.create_utility_model(..., code=send_notification)
What it does: This is a custom function we wrote. It simulates connecting to an external app (like Slack) to send alerts based on the agent's findings.

4. Agent Creation
Python

agent = AgentFactory.create(
    name="Policy Navigator Agent",
    tools=[rag_tool, sql_tool, code_tool, notification_tool],
    llm_id="..."
)
Explanation: This is where we build the "Brain." We combine the Logic Model (LLM) with all the tools we created above. This tells the AI: "You are the Policy Navigator, and here are the tools you can use to answer questions."

5. Execution
Python

response = agent.run(query)
Explanation: We give the agent a complex command. It autonomously figures out which tools to use and in what order to solve the user's problem.

🛠️ How to Run
Install Dependencies:

Bash

pip install aixplain requests beautifulsoup4 pandas
Add Your Key: Open main.py and paste your API key in the os.environ section.

Run:

Bash

python main.py
