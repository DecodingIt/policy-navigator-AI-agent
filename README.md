# ⚖️ GovRegs Agent: Agentic RAG System

**A compliance and regulatory AI assistant built with Python and the aiXplain SDK.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![aiXplain](https://img.shields.io/badge/Platform-aiXplain-orange) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

## 📖 Overview
**GovRegs Agent** is an **Agentic RAG (Retrieval-Augmented Generation)** system designed to help users navigate complex government regulations. Unlike standard chatbots, this agent doesn't just guess; it dynamically chooses between multiple tools to provide accurate, cited answers.

It is capable of:
1. **Retrieving Facts:** querying a private Vector Index for specific policy details (e.g., *Executive Order 14067*).
2. **Checking Status:** searching the live web to see if a law is active or repealed.
3. **Calculating:** handling dates and fines using a calculator tool.

## 🏗️ Architecture
The system uses an **Agentic Workflow** where a central "Brain" (LLM) orchestrates specialized tools:

1. **Data Ingestion:** Raw text/PDFs → Embedding Model → **Vector Index**.
2. **Tooling:**
    * `Gov_Compliance_Index`: For document retrieval.
    * `Web_Search`: For real-time "status" checks.
    * `Calculator`: For numerical compliance estimations.
3. **User Interface:** A Streamlit chat interface exposed via LocalTunnel.

## 🚀 Features
* **Hybrid Search:** Combines semantic document search with general web knowledge.
* **Hallucination Guardrails:** Agent instructions prioritize the private index over general training data.
* **Dynamic Indexing:** Automatically creates unique vector stores for uploaded compliance documents.
* **Citation Awareness:** Provides sources for its answers.

## 🛠️ Prerequisites
* Python 3.8+
* An [aiXplain API Key](https://platform.aixplain.com/)

## 📦 Installation

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/gov-regs-agent.git](https://github.com/yourusername/gov-regs-agent.git)
cd gov-regs-agent
