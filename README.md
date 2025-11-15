# 🎓 EduBridge: Automated Study Assistant Agent

### Capstone Project for the 5-Day AI Agents Intensive Course with Google

| Detail | Value |
| :--- | :--- |
| **Track** | Agents for Good |
| **Agent Name** | EduBridge |
| **Developer** | Mohammed Faizal. M |
| **Roles** | Placement Cell Contributor, HR Intern, Microsoft Student Ambassador |
| **Purpose** | To provide free, ethical educational and career guidance to students and freshers. |

---

## 1. The Pitch (Problem, Solution, Value)

### 1.1. Problem Statement

Students and freshers often spend excessive time and cognitive load in the initial phases of learning: searching for information, synthesizing articles, and then manually creating study aids (like flashcards or quizzes). This process is fragmented and often results in shallow, inefficient learning.

### 1.2. Solution: EduBridge Agent

The **EduBridge** agent is a specialized, multi-agent system designed to streamline this process. It takes a single topic query and executes a reliable, **sequential workflow**—acting as an automated, always-on AI tutor that delivers structured study materials in one go.

### 1.3. Value Proposition

* **Ethical Guidance:** Behavior is constrained by the developer's purpose, ensuring ethical and high-quality educational outputs.
* **Efficiency:** Instantly transforms a topic into a comprehensive study guide, saving hours of manual work.
* **Structured Learning:** Outputs are formatted into **Summary, Flashcards, and Quizzes** for immediate revision.

---

## 2. Technical Architecture & Key Concepts

The agent is built on the Google Agent Development Kit (ADK) using a sequential team structure.

### 2.1. Workflow Diagram



**Workflow Chain:** **ResearchAgent** (Find Data) ➡️ **ExplanationAgent** (Synthesize) ➡️ **ConsolidatorAgent** (Format & Final Output)

### 2.2. Key Concepts Demonstrated (70 Points Category)

| Feature | Key Concept | Implementation in `edubridge_agent.py` |
| :--- | :--- | :--- |
| **Multi-Agent System** | **Sequential Agents** | The `sequential.SequentialAgent` chains three specialized LLMAgents. |
| **Tools** | **Built-in Tools (Google Search)** | The `ResearchAgent` uses `builtin.GoogleSearchTool()` for real-time information retrieval. |
| **Sessions & Memory** | **Sessions & State Management** | The `InMemorySessionService` is used to maintain conversational history for follow-up questions. |
| **Observability** | **Logging, Tracing** | Python's `logging` module is initialized with a unique `RUN_ID` to trace the agent's internal decisions and execution path. |
| **Context Engineering** | **Context Engineering** | The `DEVELOPER_PROFILE['purpose']` is injected into the `ConsolidatorAgent`'s system prompt to guide ethical output. |

---

## 3. Setup, Execution, and Deployment

### 3.1. Local Setup

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_URL]
    cd EduBridge-Capstone-Agent
    ```
2.  **Install Dependencies:** The `requirements.txt` file includes necessary fixes for compatibility.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set Environment Variable:**
    ```bash
    export GEMINI_API_KEY="YOUR_API_KEY"
    ```
4.  **Run the Agent:**
    ```bash
    python edubridge_agent.py
    ```

### 3.2. Agent Deployment (Bonus: 5 Points)

The agent is ready for cloud deployment using the provided **`Dockerfile`**.

* **Platform:** Google Cloud Run (recommended due to generous Free Tier).
* **Steps:** Containerize the application (`docker build -t edubridge .`) and deploy the image to Cloud Run. The service will then host a stable, scalable endpoint for the agent.
