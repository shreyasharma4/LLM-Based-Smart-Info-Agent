# Smart Info Agent (Azure OpenAI + LangGraph + Tools)

A conversational AI agent powered by **Azure OpenAI** and **LangGraph**, capable of understanding natural queries and fetching **real-time data** using external APIs.

This project blends **LLM reasoning** with **tool-based actions** — letting the model decide *when* to call APIs (for weather, crypto data, etc.) and respond naturally, like a human assistant.

---

## Features

 **Natural Conversations** – The agent responds like a human, no rule-based replies.  
 **Real-Time Weather Data** – Fetches live weather info for any city via `wttr.in`.  
 **Live Cryptocurrency Prices** – Gets and compares crypto prices using the CoinGecko API.  
 **Historical Crypto Trends** – Tracks how prices have changed over time.  
 **Multi-Tool Reasoning** – Uses LangGraph to let the LLM decide which tool to call automatically.  
 **Extendable** – You can add more tools easily (e.g., stock info, news, finance, etc.).

---

## Tech Stack

- **Python 3.10+**
- **LangGraph** – For multi-step reasoning and state management  
- **LangChain** – For tool and agent abstractions  
- **Azure OpenAI API** – For LLM-based reasoning (`o3-mini` deployment)  
- **Streamlit** – For an optional interactive web UI  
- **Requests** – For calling live APIs (weather, crypto)

---

## Project Structure
LLM_based_smart_info_agent/
│
├── app/
│ ├── graph_builder.py   # Builds the LangGraph-based reasoning + tool graph
│ ├── llm_client.py   # Connects to Azure OpenAI API
│ ├── tools.py   # Defines all API tools (weather, crypto, etc.)
│ ├── run_local.py   # CLI entry point for testing
│ └── init.py
│
├── ui_app.py   # Streamlit-based web UI (optional)
├── requirements.txt   # Dependencies
└── README.md   # This file


## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your_repo_url>
   cd LLM_based_smart_info_agent

2. **Create and activate virtual environment**
python -m venv venv
venv\Scripts\activate

3. **Install dependencies**
pip install -r requirements.txt

4. **Set up your Azure OpenAI credentials**
Create a .env file or export environment variables:
AZURE_OPENAI_API_KEY=<your_api_key>
AZURE_OPENAI_ENDPOINT=https://mifinchatbotbotdemo.openai.azure.com/
AZURE_OPENAI_REGION=southindia


## Run the Agent (Terminal Mode)
python -m app.run_local


## Run with UI (Streamlit)
streamlit run ui_app.py