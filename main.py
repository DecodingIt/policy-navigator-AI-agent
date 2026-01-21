import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

from aixplain.factories import AgentFactory, IndexFactory, ModelFactory, ToolFactory
from aixplain.modules.model.record import Record
from aixplain.enums import Function, Supplier
from aixplain.modules.agent.tool.python_interpreter_tool import PythonInterpreterTool

# 1. SETUP & AUTHENTICATION

os.environ["AIXPLAIN_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"

print("--- Setting up Policy Navigator Agent ---")

# 2. INGESTION PHASE (Core Functionality: Ingest Data)

index_name = "Government_Regulations_Index"

print(f"Creating/Retrieving Index: {index_name}...")

rag_index = IndexFactory.create(
    name=index_name,
    description="Index containing government regulations (EPA, WHO) and compliance datasets."
)

csv_file_path = "compliance_data.csv"

df = pd.DataFrame({
    'policy_id': [101, 102],
    'text': [
        "The standard for PM2.5 emissions has been lowered to 9.0 µg/m3 annually.",
        "Healthcare providers must report Level 3 incidents within 24 hours."
    ],
    'category': ["Environment", "Health"]
})
df.to_csv(csv_file_path, index=False)

print("Ingesting Dataset (CSV)...")

rag_index.upsert(csv_file_path)

def scrape_and_index_url(url, source_tag):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        text_content = " ".join([p.get_text() for p in soup.find_all('p')])

        record = Record(
            id=url,
            value=text_content[:5000],  # Limit text size for demo
            attributes={"source": source_tag, "url": url}
        )
        rag_index.upsert([record])
        print(f"Successfully indexed content from {source_tag}")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# 3. DEFINE TOOLS (Technical Components)

rag_tool = AgentFactory.create_model_tool(
    model=rag_index.id,
    description="Use this tool to search for specific government regulations, compliance policies, and scraped web data."
)


sql_tool = AgentFactory.create_sql_tool(
    name="Compliance Data Analyzer",
    description="Useful for counting policies, filtering data by category, or finding specific policy IDs from the CSV.",
    source=csv_file_path,
    source_type="csv"
)



code_tool = PythonInterpreterTool()

def send_notification(message: str, platform: str = "Slack") -> str:

    print(f"\n[INTEGRATION] Sending to {platform}: {message}\n")
    return f"Notification successfully sent to {platform}."


notification_tool = ModelFactory.create_utility_model(
    name="Notification Sender",
    description="Send summaries, alerts, or updates to external apps like Slack or Notion.",
    code=send_notification
)

# 4. CREATE THE AGENT

print("Constructing Policy Navigator Agent...")

agent = AgentFactory.create(
    name="Policy Navigator Agent",
    description="An AI agent that analyzes government regulations and compliance policies. It can search documentation, analyze data, and notify users.",
    tools=[
        rag_tool,
        sql_tool,
        code_tool,
        notification_tool
    ],
    llm_id="6646261c6eb563165658bbb1"  # Example ID for GPT-4o or similar high-reasoning model
)

print(f"Agent Created! ID: {agent.id}")


# 5. RUN THE AGENT
query = """
Check the regulations regarding PM2.5 emissions. 
If the limit is below 10.0, use Python to calculate the percentage reduction needed from a current level of 12.0. 
Finally, send a Slack notification with the required reduction.
"""

print(f"\nProcessing Query: {query}")
response = agent.run(query)

print("\n--- Agent Response ---")
print(response.data["output"])