# 🤖 Zebo: The Generative AI Analyst Chatbot

Zebo is a sophisticated, human-like chatbot specializing in Generative AI tools, frameworks, and research. This project fulfills the challenge requirements by implementing a layered multi-agent architecture (RAG, Web Scraping, Memory) and a custom, user-centric interface (Streamlit).

## 👤 Persona: Zebo (The Generative AI Research Analyst)

Zebo adopts a friendly, curious, and conversational tone, always seeking to clarify the user's intent. The goal is to provide precise, contextually aware answers about GenAI.

## ⚙️ Architecture and Agent System

This chatbot operates on a multi-layered system orchestrated via Python code (using concepts found in LangChain/LangGraph):

1.  **Reasoning Agent (Gemini 2.5 Flash):** The core large language model that synthesizes information, maintains the persona, and generates the final response.
2.  **Retrieval Agent (Qdrant):** Queries the embedded vector database for domain-specific facts (RAG: Retrieval-Augmented Generation) before answering a technical question (e.g., "What is RAG?").
3.  **Web-Scraper Agent (`requests`/BeautifulSoup):** Fetches real-time, external information (e.g., "What's the latest LangChain news?") when the internal memory is insufficient.
4.  **Memory Agent:** Maintains both **Short-Term Memory** (session state for conversational context) and **Long-Term Memory** (Qdrant database).
5.  **Evaluation Agent (Placeholder):** Currently integrated through prompt engineering (hallucination reduction) and will be formally expanded during the submission phase (see below).

## 🚀 Setup and Installation

### Prerequisites
* Python 3.10+
* A Google AI API Key (`GOOGLE_API_KEY`)

### Steps

1.  **Clone the Repository (or Download Files):** Ensure all files (`main.py`, `chat_ui.py`, `database.py`, etc.) are in one folder.
2.  **Install Dependencies:** Open the terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set API Key:** Create a file named `.env` in the root folder and add your key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
4.  **Run the Backend (FastAPI):** Open the first terminal window and start the API engine. (This initializes the Qdrant database/memory).
    ```bash
    python main.py
    ```
5.  **Run the Frontend (Streamlit):** Open a second terminal window and start the UI.
    ```bash
    streamlit run chat_ui.py
    ```

## 📋 Evaluation Criteria (The Final Step)

The challenge requires a **CSV file** with evaluation results from at least **50 test queries** using tools like Ragas or DeepEval.

Since we built this without a heavy evaluation framework, your immediate next step is to prepare for this testing. You need to run 50 queries and manually document the results in a spreadsheet (CSV) format.

| Query Text | Expected Answer Category | Actual Response | Context Used | Hallucination (Y/N) | Relevance (1-5) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| what is Qdrant | RAG Fact | Qdrant is a vector database... | database.py | N | 5 |
| what's the news | Scraper Fact | Latest headlines... | web_scraper.py | N | 5 |
| how are you | Irrelevant | I specialize in GenAI... | N/A | N | 5 |
| what is LangChain | RAG Fact | LangChain is a framework... | database.py | N | 5 |
| **(46 more queries...)** | | | | | |