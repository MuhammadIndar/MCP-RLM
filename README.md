

# 🧠 MCP-RLM: Recursive Language Model Agent

**Infinite Context Reasoning for Large Language Models**

## 📖 What is MCP-RLM?

**MCP-RLM** is an *open-source* implementation of the **Recursive Language Models (RLMs)** architecture introduced by researchers at MIT CSAIL (Zhang et al., 2025).

Typically, LLMs have a "Context Window" limit. If you force a document containing millions of words into it, the model will suffer from *context rot* (forgetting the middle part) or become extremely slow and expensive.

**MCP-RLM changes how LLMs process data:**
Instead of "reading" the entire document at once, MCP-RLM treats the document as an **External Environment** (like a database or file) that can be accessed programmatically. The agent uses Python code to break down, scan, and perform *sub-queries* recursively to itself to answer complex questions from massive data.

---

## ✨ Key Features

* **♾️ Infinite Context Scaling**: Capable of processing documents far larger than the model's token limit (theoretically up to 10 Million+ tokens).
* **📉 Cost-Effective**: Uses small models (Worker) for heavy scanning, and large models (Planner) only for orchestration. Cheaper than loading the entire context into a large model.
* **🎯 High Accuracy on Reasoning**: Reduces hallucinations on complex *needle-in-a-haystack* tasks because each section is examined in isolation.
* **🔌 Provider Agnostic**: Flexible configuration! Use **Claude** as the brain (Root) and **Ollama/Local LLM** as the worker (Sub) for privacy and cost savings.

---

## ⚙️ How It Works & Architecture

This implementation uses the **MCP (Model Context Protocol)** to connect your IDE/Chatbot (such as Cursor, Claude Desktop) with the "RLM Engine" behind the scenes.
![RLM](./assets/RLM.png)

### Core Concept: Root vs. Sub Agent

The system divides tasks into two AI model roles for cost efficiency and accuracy:

1. **🧠 Root Agent (The Planner)**
* **Role**: Project Manager.
* **Task**: Does not read the document directly. It views metadata (file length), plans strategies, and writes Python code to execute those strategies.
* **Model**: Smart model (e.g., `Claude-3.5-Sonnet`, `GPT-4o`).


2. **👷 Sub Agent (The Worker)**
* **Role**: Field Worker.
* **Task**: Called hundreds of times by the Python code to read small data *chunks* and extract specific information.
* **Model**: Fast & cheap model (e.g., `GPT-4o-mini`, `Llama-3`, `Haiku`).



---

## 🚀 Installation & Usage

### Prerequisites

* Python 3.10+
* `pip`

### Installation Steps

1. **Clone Repository**
```bash
git clone https://github.com/username/MCP-RLM.git
cd MCP-RLM

```


2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate   # For Windows

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


**What is being installed?**
* `mcp`: The core SDK for the MCP protocol.
* `openai` & `anthropic`: Client libraries to connect to LLM providers.
* `python-dotenv`: To load API Keys from the `.env` file.
* `tiktoken`: To count tokens to ensure they fit model limits.


```


```


4. **Environment Configuration**
Copy `.env.EXAMPLE` to `.env` and fill in your API Keys.
```bash
cp .env.EXAMPLE .env

```



### Model Configuration

You can control the agent's behavior via `config.yaml`.

```yaml
# config.yaml
agents:
  root:
    provider: "anthropic"
    model: "claude-3-5-sonnet" # Excellent at coding
  sub:
    provider: "openai"         # Or use "ollama" for local
    model: "gpt-4o-mini"       # Fast & Cheap for hundreds of loops

```

### Running the Server

Run the MCP server:

```bash
python server.py

```

The server will run and be ready to connect with MCP clients (like Claude Desktop or Cursor).

---

## Client Configuration

To use it, you need to connect this MCP server to applications like Claude Desktop or Cursor.

### 1. Claude Desktop

Open the Claude Desktop configuration file:

* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "rlm-researcher": {
      "command": "/path/to/MCP-RLM/venv/bin/python",
      "args": ["/path/to/MCP-RLM/server.py"]
    }
  }
}

```

> **Note:** Replace `/path/to/MCP-RLM/` with the absolute path to your project folder.

### 2. Cursor IDE

1. Open **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Fill in the following form:
* **Name**: `RLM-Researcher` (or any other name)
* **Type**: `stdio`
* **Command**: `/path/to/MCP-RLM/venv/bin/python /path/to/MCP-RLM/server.py`


4. Click **Save**.

If successful, the status indicator will turn green.

### 3. Antigravity IDE

You can use the UI or edit the configuration file manually.

**Method 1: Via UI**

1. Click the `...` menu in the agent panel.
2. Select **Manage MCP Servers**.
3. Add a new server with the same configuration as above.

**Method 2: Manual Config**
Edit the file `~/.gemini/antigravity/mcp_config.json`:

```json
{
  "mcpServers": {
    "rlm-researcher": {
      "command": "/path/to/MCP-RLM/venv/bin/python",
      "args": ["/path/to/MCP-RLM/server.py"],
      "enabled": true
    }
  }
}

```

---

## 📚 References & Credits

This project is an experimental implementation based on the following research paper:

> **Recursive Language Models**
> *Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL) 2025*

This paper proposes RLM as a general inference strategy that treats long prompts as an external environment, enabling programmatic problem decomposition.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

---
