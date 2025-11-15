# --- 1. SETUP AND DEPENDENCY FIXES ---

# 🚨 CRITICAL FIX for Pydantic/ADK conflicts in Kaggle:
# Force install stable Pydantic versions before installing the main libraries.
!pip install "pydantic<2.0" "pydantic-core<2.0" --quiet
# Install the core Google libraries
!pip install google-adk google-genai --quiet

# --- IMPORTS & OBSERVABILITY ---
import os
import logging, uuid
# If the error "No module named 'google.adk.agent_team'" persists, 
# it means the kernel restart is necessary, but the imports should work here.
from google import adk
from google.adk.agent_team import sequential
from google.adk.llm_agent import LlmAgent, LlmAgentConfig
from google.adk.tools import builtin
from google.adk.session import InMemorySessionService
from google.genai import types

# Initialize Observability (Required Feature)
RUN_ID = str(uuid.uuid4())[:8]
logging.basicConfig(level=logging.INFO, format=f"%(asctime)s | RUN_ID={RUN_ID} | %(levelname)s | %(message)s")
print(f"✅ Observability initialized with RUN_ID: {RUN_ID}")

# --- DEVELOPER PROFILE (Context Engineering) ---
DEVELOPER_PROFILE = {
    "agent_name": "EduBridge",
    "developer_name": "Mohammed Faizal. M",
    "purpose": "Provide free, ethical educational and career guidance to students and freshers."
}

# --- API KEY CONFIGURATION ---
try:
    API_KEY = os.environ.get("GEMINI_API_KEY") 
    if not API_KEY:
        logging.warning("GEMINI_API_KEY environment variable not found. Please set it as a Kaggle Secret.")
except Exception as e:
    logging.error(f"Error during API Key setup: {e}")

# --- 2. AGENT DEFINITIONS (Multi-Agent System) ---

# 2.1. ResearchAgent: Uses Google Search (Built-in Tool)
research_config = LlmAgentConfig(
    model_name='gemini-2.5-flash',
    system_instruction="You are a meticulous Research Agent. Your sole task is to use the Google Search tool to find and return **only the most relevant raw text snippets** for the student's study topic.",
    tools=[builtin.GoogleSearchTool()], 
    temperature=0.0,
)
research_agent = LlmAgent(name="ResearchAgent", config=research_config)
logging.info("ResearchAgent initialized.")


# 2.2. ExplanationAgent: Synthesizes the raw data.
explanation_config = LlmAgentConfig(
    model_name='gemini-2.5-flash',
    system_instruction="You are a Tutor Agent. Synthesize the raw research findings into a clear, concise educational explanation suitable for a high school student.",
    temperature=0.3,
)
explanation_agent = LlmAgent(name="ExplanationAgent", config=explanation_config)
logging.info("ExplanationAgent initialized.")


# 2.3. ConsolidatorAgent: Formats the final output based on the Developer Profile's purpose.
developer_purpose = DEVELOPER_PROFILE['purpose']
consolidator_system_instruction = f"""
You are the Study Material Consolidator Agent for the 'EduBridge' project. 
The project's guiding principle is to: "{developer_purpose}".
Your final task is to reformat the provided explanation into a structured study guide that is ethical and effective. The guide **must** include: 
1. A final, concise summary. 
2. At least two key terms/definitions (Flashcards format). 
3. One simple quiz question related to the topic, with the answer hidden at the end.
"""

consolidator_config = LlmAgentConfig(
    model_name='gemini-2.5-flash',
    system_instruction=consolidator_system_instruction,
    temperature=0.5,
)
consolidator_agent = LlmAgent(name="ConsolidatorAgent", config=consolidator_config)
logging.info("ConsolidatorAgent initialized with ethical context.")


# --- 3. SEQUENTIAL AGENT ORCHESTRATION ---
edubridge_agent = sequential.SequentialAgent(
    name="EduBridge_Assistant",
    agents=[
        research_agent,
        explanation_agent,
        consolidator_agent
    ],
)
print("\n✅ EduBridge Sequential Agent System Initialized and Ready for Testing.")
# --- 4. SESSIONS & MEMORY SETUP (State Management) ---
session_service = InMemorySessionService()
session_id = "capstone_student_session"

def run_edubridge_agent(user_prompt: str):
    """Executes the agent workflow and manages session state."""
    
    # Get/Create Session (maintains history for follow-up questions)
    session = session_service.get_session(session_id)
    
    # Observability: Log the start
    logging.info(f"RUNNING TASK: Student Query -> '{user_prompt[:50]}...'")
    
    try:
        # Execute the Sequential Agent (Agent 1 -> Agent 2 -> Agent 3)
        response = edubridge_agent.run(
            user_prompt, 
            session=session 
        )
        
        # Update Session History
        session.history.append(types.Content(role='user', parts=[types.Part.from_text(user_prompt)]))
        session.history.append(types.Content(role='model', parts=[types.Part.from_text(response.output)]))
        
        logging.info(f"TASK SUCCESS: Study material generated. History length: {len(session.history)} turns.")
        return response.output
    
    except Exception as e:
        logging.error(f"TASK FAILED: {e}")
        return f"❌ Agent Error: An issue occurred during the study generation workflow: {e}"


# --- 5. LIVE INTERACTIVE TEST (Your "Web UI" Equivalent) ---
print("\n" + "="*20 + " EDU BRIDGE LIVE TEST INTERFACE " + "="*20)
print("Demonstrating Sequential Workflow, Google Search, and Observability.")
print("-" * 60)

# Example interaction 1: Full research and generation
test_input_1 = "Explain the recent advancements in sustainable energy storage."
print(f"**INPUT 1:** STUDENT > {test_input_1}")
agent_output_1 = run_edubridge_agent(test_input_1)
    
print("\n" + "--- 🎓 EDU BRIDGE OUTPUT 1 ---")
print(agent_output_1)
print("-" * 60)

# Example interaction 2: Follow-up question (Testing Session/Memory)
test_input_2 = "Give me one more flashcard about a key term from the last topic."
print(f"\n**INPUT 2:** STUDENT > {test_input_2}")
agent_output_2 = run_edubridge_agent(test_input_2)

print("\n" + "--- 🎓 EDU BRIDGE OUTPUT 2 (Testing Memory) ---")
print(agent_output_2)
print("-" * 60)
