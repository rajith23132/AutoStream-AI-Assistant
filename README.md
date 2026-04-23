# AutoStream-AI-Assistant

A conversational AI agent that answers product queries, detects high-intent users, and captures leads using a structured workflow powered by Gemini + LangChain.

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd autostream-agent
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set your API key

**Windows:**

```bash
set GOOGLE_API_KEY=your_api_key
```

**Mac/Linux:**

```bash
export GOOGLE_API_KEY="your_api_key"
```

---

### 5. Run the app

```bash
python -m streamlit run app.py
```

Open: http://localhost:8501

---

## Architecture Explanation

This project uses a modular agent design built with LangChain and a Gemini LLM. While LangGraph could be used for more complex workflows, I chose a lightweight LangChain-based approach because the task involves a linear but stateful interaction (query → intent detection → lead capture).

State is managed using a combination of:

* `st.session_state` (for UI-level persistence)
* A structured `state` dictionary inside the agent

The state tracks whether the agent is currently in a lead collection phase (`collecting = True/False`) and stores user details (name, email, platform). This allows the agent to maintain context across 5–6 turns and ensures that once a user shows high intent, the system transitions from a retrieval-based response (RAG) to a deterministic lead capture flow.

Intent detection is handled using rule-based logic (keyword matching), prioritizing high-intent signals before informational queries. This prevents the model from continuing to answer questions when it should instead initiate conversion.

For knowledge retrieval, a simple JSON-based RAG approach is used, where context is injected into the LLM prompt.

---

## WhatsApp Deployment (Webhook Integration)

To integrate this agent with WhatsApp, I would use the WhatsApp Business API (via Meta or a provider like Twilio).

### Flow:

1. **Webhook Setup**

   * Deploy a backend (FastAPI/Flask)
   * Expose an endpoint (e.g., `/webhook`)
   * Register it with WhatsApp API

2. **Incoming Messages**

   * WhatsApp sends user messages to the webhook
   * Extract user ID (phone number) and message text

3. **State Management**

   * Store conversation state per user (Redis / DB)
   * Retrieve state before calling `agent_step()`

4. **Agent Processing**

   * Pass message + state to the agent
   * Get response and updated state

5. **Send Response**

   * Call WhatsApp API to send reply back to user

6. **Persistence**

   * Save updated state for future turns

### Key Considerations:

* Use Redis for scalable session memory
* Handle rate limits and retries
* Secure webhook with verification tokens

---

## Features

* Intent detection (greeting, pricing, high-intent)
* Context-aware responses (RAG)
* Multi-turn memory (5–6 turns)
* Lead capture workflow
* Mock tool execution
* Streamlit chat UI

---

## Sample Flow

User: *"I want to try the Pro plan"* ->
Agent: *"Awesome! Can I have your name?"* ->
→ Collects email
→ Collects platform
→ Calls `mock_lead_capture()`

---

## 🛠 Tech Stack

* Python
* LangChain
* Gemini API
* Streamlit

---

## 📄 License

For assignment/demo purposes.
