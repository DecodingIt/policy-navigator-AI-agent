#=================================================================================
#First Block
!pip install aixplain pandas streamlit --upgrade -q

import os
os.environ["AIXPLAIN_API_KEY"] = "f42fae9e414932e1991b589cf28c95317e240a0bd7d52d4aa0c87ab400231c88"
import time
from aixplain.factories import AgentFactory, ModelFactory, IndexFactory, ToolFactory
from aixplain.enums import Function, Language

print("Environment setup complete")
#=================================================================================
#2ND BLOCK
import time
from aixplain.enums import Function


print("Searching for a valid embedding model")
embedding_models = ModelFactory.list(
    function=Function.TEXT_EMBEDDING,
    page_size=5
)
embed_model = embedding_models['results'][0]
print(f"Using Model: {embed_model.name}")


unique_id = int(time.time())
index_name = f"Gov_Compliance_Index_{unique_id}"
print(f"Creating Unique Index: {index_name}...")


index = IndexFactory.create(
    name=index_name,
    description="Index containing government privacy acts.",
    embedding_model=embed_model.id
)


policy_text = """
EXECUTIVE ORDER 14067 SUMMARY:
This order ensures the responsible development of digital assets.
Section 4(b): The Secretary of the Treasury shall report on the future of money and payment systems.
Compliance Note: Small businesses dealing in crypto-assets must register with FinCEN by Q4 2025.
Section 230 Status: Remains active but subject to new transparency reporting requirements as of May 2025.
"""

with open("policy_document.txt", "w") as f:
    f.write(policy_text)

print("Uploading document")
index.upsert("policy_document.txt")

print(f"Indexing complete. Index ID: {index.id}")
#=================================================================================
#3RD BLOCK

rag_tool = index

search_tool = ModelFactory.get("6931bdf462eb386b7158def3")

calc_tool = ModelFactory.get("60ddefa08d38c51c5885e75e")

print("Tools configured.")

system_prompt = """
You are a 'Government Compliance & Regulatory Agent'.
1. ALWAYS check the 'Gov_Compliance_Index' first for specific policy details.
2. If the user asks about the STATUS of a law and it's not in the index, use the Search Tool.
3. Provide clear, structured answers with citations.
"""


agent = AgentFactory.create(
    name="GoverAgent",
    description="Agent for querying government regulations.",
    instructions=system_prompt,
    tools=[
        rag_tool,
        search_tool,
        calc_tool
    ],
    llm_id="6922e85e0d7b9d771e28cc5b" #Gemini 3.0
)

print(f"Agent Created! ID: {agent.id}")
#=================================================================================
#4TH BLOCK

query = "What are the compliance requirements for small businesses regarding crypto?"

print(f"User: {query}")
print("Agent is thinking")

try:
    response = agent.run(query)
    print(f"\nAgent: {response['data']['output']}")
except Exception as e:
    print(f"Error: {e}")
#=================================================================================
