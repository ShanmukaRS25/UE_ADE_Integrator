
#  README.md

# LLM Tooling for Structured 3D Editor Workflows (Unreal Engine)

An open-source framework that enables natural-language–driven automation inside Unreal Engine by converting LLM outputs into structured, deterministic editor actions.

This project demonstrates how Large Language Models (LLMs) can safely assist complex visual editor workflows using a schema-constrained, tool-based execution model.

## 🚀 Overview

Modern LLMs are powerful, but directly allowing them to manipulate complex, stateful systems (like 3D editors) can be unsafe and non-deterministic.

This project solves that problem by introducing:

* A **Python-based command server** that validates and structures LLM outputs
* A **C++ Unreal Engine Editor Plugin** that executes only approved actions
* A **schema-first tool architecture** to prevent hallucinated or unsafe operations

Instead of allowing an LLM to “freely generate code,” the system:

1. Accepts natural language input
2. Converts it into structured tool commands
3. Validates against a strict schema
4. Executes deterministic editor operations

## 🏗 System Architecture

```
User (Natural Language)
        ↓
LLM (Cursor / Claude / API)
        ↓
MCP Tool Call
        ↓
Python Command Server (Validation Layer)
        ↓
HTTP / JSON
        ↓
Unreal Engine Editor Plugin (C++)
        ↓
Structured Asset Creation & Wiring
```

### Core Principle

> Separate AI reasoning from execution.

The LLM suggests actions.
The engine executes only validated, deterministic commands.

## ✨ Features

* Natural language → structured editor actions
* Schema-validated LLM output
* Deterministic execution layer
* Automated asset generation (AI controllers, state machines, behavior graphs)
* Open-source, extensible tool architecture
* Editor-only plugin (no runtime risk)

## 📦 Repository Structure

```
/mcp-server
    server.py
    /tools
    /schemas
    requirements.txt

/unreal-plugin
    /Source
    MCP_AI_Plugin.uplugin

/docs
    architecture.md
    contribution-guide.md


# 🛠 Installation & Setup

## 1️⃣ Prerequisites

### Required Software

* Unreal Engine 5.6 (C++ project)
* Visual Studio 2022 (Game Development with C++)
* Python 3.11+
* pip

Optional:

* Cursor AI / Claude Desktop
* OpenAI / Anthropic API key

## 2️⃣ Unreal Engine Setup

### Step 1: Create Project

1. Open Unreal Engine 5.6
2. Select **Games → Third Person Template**
3. Choose **C++**
4. Name project: `UE_MCP_AI_Tools`

### Step 2: Install Plugin

1. Copy `unreal-plugin/MCP_AI_Plugin` into:

YourProject/Plugins/

2. Open Unreal Editor
3. Enable the plugin under:

   Edit → Plugins
   ```
4. Restart Editor


### Step 3: Enable Required UE Modules

Ensure the following are enabled:

* AI Module
* Gameplay Tasks
* Editor Scripting Utilities
* HTTP Server
* JSON / JSON Utilities


## 3️⃣ Python MCP Server Setup

Navigate to:

```
cd mcp-server
```

Create virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate   # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn server:app --reload
```

Server runs at:

```
http://localhost:8000
```


## 🔐 Security & Validation

The system enforces:

* Strict JSON schema validation
* Predefined tool whitelist
* Deterministic command mapping
* No arbitrary code execution

The Unreal plugin executes only recognized actions such as:

* CREATE_AI_CONTROLLER
* CREATE_BLACKBOARD
* CREATE_BEHAVIOR_TREE
* ADD_BT_NODE
* CONNECT_BT_NODES

# 🧠 Example Workflow

## User Prompt

```
Create a basic enemy AI that patrols between points and chases the player when detected.
```


## LLM Output (Structured Tool Call)

```json
{
  "action": "CREATE_BEHAVIOR_TREE",
  "name": "BT_Enemy"
}
```


## Unreal Engine Result

The system automatically:

* Creates AI Controller class
* Creates Blackboard with required keys
* Creates Behavior Tree
* Wires root sequence
* Adds patrol & chase tasks

All without manual UI configuration.


# 🎯 Final Result

After execution:

* AI assets appear in Content Browser
* Behavior Tree is fully structured
* Blackboard keys are configured
* AI controller references tree
* Ready for in-editor testing

Time saved compared to manual setup: significant for rapid prototyping.

# 🧪 Testing

* Schema validation tests
* API contract tests
* Editor command logging
* Asset creation verification

To run server tests:

```bash
pytest
```

# 🔄 Contribution Guide

Contributors can:

* Add new MCP tools
* Extend Unreal command handlers
* Improve validation schemas
* Add new automation workflows

Each tool requires:

1. Schema definition
2. Python validation logic
3. Unreal execution handler

# 📚 Design Principles

* Tool-based LLM interaction
* Deterministic execution
* Human-in-the-loop automation
* Clear separation of reasoning and action
* Extensibility over complexity

# ⚠️ Limitations

* Editor-only (not runtime)
* Requires Unreal C++ project
* Limited to predefined tool actions
* Not a general-purpose code generator

# 🔮 Roadmap

* Extended asset graph automation
* Perception system setup
* Batch workflow generation
* Multi-engine abstraction layer
* CLI interface for CI pipelines


# 📄 License

MIT License


# 🤝 Why This Project Exists

This project explores how LLMs can assist complex software systems safely.
Unreal Engine is used as a representative large, stateful editor environment.
The architecture is transferable to CAD, robotics simulation, digital twin systems, and other 3D platforms.


If you'd like next, I can:

* Make this README more startup-product style
* Make it more research-focused
* Add diagrams (Mermaid architecture graph)
* Create a GitHub project description summary (short version)
* Help you write a contribution guide

Just tell me the direction.
