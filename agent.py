import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


# SET API KEY (for local dev)
# ---------------------------
os.environ["GOOGLE_API_KEY"] = "Your API Key"

# Load Knowledge Base
# ---------------------------
with open("knowledge.json", "r") as f:
    knowledge = json.load(f)

# Gemini LLM
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Mock Tool
# ---------------------------
def mock_lead_capture(name, email, platform):
    return f"Lead captured successfully: {name}, {email}, {platform}"

# Intent Detection
# ---------------------------
def detect_intent(user_input):
    text = user_input.lower()

    # HIGH INTENT 
    if any(phrase in text for phrase in [
        "i want", "i’d like", "i would like",
        "sign me up", "get started",
        "try", "subscribe", "buy"
    ]):
        return "high_intent"

    if any(w in text for w in ["hi", "hello", "hey"]):
        return "greeting"

    if any(w in text for w in ["price", "cost", "plan", "pricing"]):
        return "pricing"

    return "general"

# RAG
# ---------------------------
def get_rag_response(user_input, history):

    context = json.dumps(knowledge, indent=2)

    prompt = PromptTemplate(
        input_variables=["context", "question", "history"],
        template="""
You are a SaaS assistant.

Conversation:
{history}

Answer ONLY from this context:
{context}

Question:
{question}
"""
    )

    chain = prompt | llm

    res = chain.invoke({
        "context": context,
        "question": user_input,
        "history": history
    })

    return res.content

# AGENT STEP
# ---------------------------
def agent_step(user_input, state, history):

    # ---------------------------
    # Lead Capture Flow
    # ---------------------------
    if state["collecting"]:

        if not state["lead"]["name"]:
            state["lead"]["name"] = user_input
            return "Got it! What's your email?", state

        elif not state["lead"]["email"]:
            state["lead"]["email"] = user_input
            return "Great! Which platform do you create content on?", state

        elif not state["lead"]["platform"]:
            state["lead"]["platform"] = user_input

            msg = mock_lead_capture(
                state["lead"]["name"],
                state["lead"]["email"],
                state["lead"]["platform"]
            )

            # reset
            state["collecting"] = False
            state["lead"] = {"name": None, "email": None, "platform": None}

            return msg + "\nThanks! We'll reach out soon!! ", state

    
    # Intent Detection
    # ---------------------------
    intent = detect_intent(user_input)

    
    # Handle Intents
    # ---------------------------
    if intent == "high_intent":
        state["collecting"] = True
        return "Awesome! Can I have your name?", state

    elif intent == "greeting":
        return "Hey! How can I help you today?", state

    elif intent == "pricing":
        return get_rag_response(user_input, history), state

    else:
        return get_rag_response(user_input, history), state
