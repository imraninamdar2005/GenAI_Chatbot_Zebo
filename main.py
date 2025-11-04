# This is the NEW code for main.py (with "Zebo")

from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Dict

# --- Import agents ---
import database
import web_scraper

# --- Define chat models ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: List[ChatMessage]

# Load the API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY not found in .env file")

# Configure the Gemini AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# 1. Create the FastAPI "app"
app = FastAPI(
    title="GenAI Chatbot",
    description="A human-like chatbot specializing in Generative AI."
)

# --- NEW PERSONA: ZEBO ---
# 2. Define the "persona"
persona = {
    "name": "Zebo", # <-- NAME CHANGED
    "background": "Generative AI Research Analyst",
    "interests": ["AI libraries", "tools", "startups", "emerging models"],
    "style": "Friendly, curious, and conversational."
}

# 3. The main "homepage" route
@app.get("/")
def get_root():
    return {
        "message": f"Hello! I'm {persona['name']}.",
        "details": f"I'm a {persona['background']} and I love to chat about {', '.join(persona['interests'])}. How can I help you today?"
    }

# 4. The "brain" endpoint (NOW WITH MEMORY)
@app.post("/chat")
def handle_chat(request: ChatRequest):
    
    if not request.history:
        raise HTTPException(status_code=400, detail="No chat history provided.")
    
    user_prompt = request.history[-1].content
    past_conversation = request.history[:-1]
    
    context_data = None
    
    # --- AGENT ORCHESTRATION ---
    if "news" in user_prompt.lower() or "latest" in user_prompt.lower() or "blog" in user_prompt.lower():
        print("Keyword match: Activating Web-Scraper Agent...")
        context_data = web_scraper.scrape_latest_langchain_news()
    
    if not context_data:
        print("Activating Retrieval Agent (Memory)...")
        retrieved_fact = database.search_memory(user_prompt)
        if retrieved_fact:
            print(f"Found relevant fact: {retrieved_fact}")
            context_data = retrieved_fact
        else:
            print("No specific fact found in memory.")
    
    if not context_data and ("generative ai" not in user_prompt.lower() and "genai" not in user_prompt.lower()):
        return {"response": "That's an interesting question! However, I specialize in Generative AI. Could we talk about that instead?"}

    # --- Build the prompt with memory ---
    try:
        chat_transcript = ""
        for message in past_conversation:
            if message.role == "user":
                chat_transcript += f"User: {message.content}\n"
            elif message.role == "assistant":
                chat_transcript += f"Zebo: {message.content}\n" # <-- NAME CHANGED

        full_prompt = f"""
        You are Zebo, a Generative AI Research Analyst. # <-- NAME CHANGED
        Your style is friendly, curious, and conversational.
        
        Here is the conversation so far:
        {chat_transcript}
        
        A user is now asking: '{user_prompt}'
        """
        
        if context_data:
            full_prompt += f"\n\nUse this specific context to help you answer: '{context_data}'"
        
        full_prompt += "\n\nPlease provide a helpful response based on the new question and the conversation history."
        
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        return {"response": ai_response}

    except Exception as e:
        print(f"Error calling AI: {e}")
        raise HTTPException(status_code=500, detail="Error generating AI response.")

# 6. A function to run the server
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)