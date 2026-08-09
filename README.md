# AI Code Agent

An Agentic AI coding assistant built with **Python, Google Gemini, LangGraph, LangChain, Docker, and Human-in-the-Loop approval**.

The agent can inspect a Python project, search and read source files, execute code inside an isolated Docker sandbox, analyze execution errors, propose file modifications, request human approval, apply approved changes, and re-run the code to verify the fix.

---

## Overview

The goal of this project is to demonstrate how an AI coding agent can move beyond simple LLM conversation and perform a controlled software-engineering workflow.

Instead of allowing the LLM to directly modify or execute code on the host machine, the system uses:

* **LangGraph** for agent workflow and state management
* **Google Gemini** for reasoning and tool selection
* **LangChain** for tool integration
* **Docker** for isolated Python execution
* **Human-in-the-Loop** for approving file modifications
* **Workspace restrictions** for safer file operations

---

## Architecture

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │ Gemini LLM  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  LangGraph  │
                    │    Agent    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         File Tools    Search Tools   Sandbox
              │            │            │
              │            │            ▼
              │            │          Docker
              │            │            │
              │            │            ▼
              │            │      stdout/stderr
              │            │       + exit code
              │            │            │
              └────────────┴────────────┘
                           │
                           ▼
                    Error Diagnosis
                           │
                           ▼
                     Edit Proposal
                           │
                           ▼
                  ┌─────────────────┐
                  │ Human Approval  │
                  └────────┬────────┘
                           │
                    ┌──────┴──────┐
                    │             │
                   YES            NO
                    │             │
                    ▼             ▼
               Apply Edit      Reject Edit
                    │
                    ▼
              Docker Re-run
                    │
                    ▼
               Verification
                    │
                    ▼
                  SUCCESS
```

---

## Core Workflow

A typical debugging task follows this workflow:

```text
User Request
     ↓
Agent understands the task
     ↓
Agent selects appropriate tools
     ↓
Agent inspects source files
     ↓
Agent executes the program
     ↓
Docker returns execution result
     ↓
Agent analyzes traceback/error
     ↓
Agent proposes a minimal edit
     ↓
Human reviews the proposed edit
     ↓
Human approves or rejects
     ↓
Approved edit is applied
     ↓
Program is executed again
     ↓
Agent verifies the result
```

---

## Features

### 1. LLM Tool Calling

Gemini determines which tool should be used based on the user's request.

Available capabilities include:

* Directory listing
* File reading
* File searching
* File discovery
* Python execution
* Docker sandbox execution
* File editing

---

### 2. LangGraph Agent Workflow

LangGraph manages the agent's state and execution flow.

The graph contains:

* Agent node
* Tool node
* Approval node
* Edit application node
* Conditional routing
* Checkpointing
* Human interrupts

This allows the agent to perform multi-step tasks instead of a single LLM request.

---

### 3. Docker Sandbox

Python code is executed inside a Docker container instead of directly on the host environment.

The sandbox uses:

* `python:3.11-slim`
* Network disabled
* Memory limit
* CPU limit
* Process limit
* Read-only workspace mount
* Execution timeout

Example:

```text
Agent
  ↓
Docker Sandbox
  ↓
Python execution
  ↓
STDOUT
STDERR
EXIT CODE
```

This execution result is returned to the agent for diagnosis.

---

### 4. Human-in-the-Loop File Editing

The agent does not silently modify source code.

When an edit is proposed:

```text
AI proposes modification
        ↓
Edit preview
        ↓
Human approval
        ↓
     ┌──┴──┐
    YES    NO
     │      │
     ▼      ▼
   Apply   Reject
```

This prevents an LLM-generated modification from being applied without user confirmation.

---

### 5. Workspace Protection

File modification is restricted to the configured workspace.

Attempts to modify files outside the allowed workspace are rejected.

The editor also requires the target text to occur exactly once before applying a modification.

This prevents ambiguous replacements.

---

### 6. Error Diagnosis and Repair

The agent can use execution results to diagnose errors.

Example:

```python
result = calculate_total(10, 20)

print(total)
```

Docker returns:

```text
NameError: name 'total' is not defined
EXIT CODE: 1
```

The agent can inspect the source and identify that `result` exists while `total` does not.

It can then propose:

```python
print(result)
```

After human approval, the modification is applied and the program is executed again.

Successful verification:

```text
STDOUT:
200

EXIT CODE: 0
```

---

## Available Tools

| Tool                 | Purpose                        |
| -------------------- | ------------------------------ |
| `list_directory`     | List files/directories         |
| `read_file`          | Read source files              |
| `search_files`       | Search text across files       |
| `find_file`          | Find files by name             |
| `edit_file`          | Generate/preview an exact edit |
| `apply_file_edit`    | Apply an approved edit         |
| `run_python`         | Python execution utility       |
| `run_python_sandbox` | Execute Python inside Docker   |

---

## Project Structure

```text
AI_Code_Agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── graph.py
│   ├── llm.py
│   ├── main.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── editor.py
│       ├── executor.py
│       ├── filesystem.py
│       ├── sandbox.py
│       └── search.py
│
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_approval.py
│   ├── test_editor.py
│   ├── test_executor.py
│   ├── test_graph.py
│   ├── test_llm.py
│   ├── test_sandbox.py
│   └── test_tools.py
│
├── workspace/
│   └── sample_project/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `.env` is for local development and must never be committed to Git.

---

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI_Code_Agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Docker Desktop

Docker Desktop must be installed and the Docker Engine must be running.

Verify:

```bash
docker --version
```

Then:

```bash
docker run --rm python:3.11-slim python --version
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

The application loads the API key using `python-dotenv`.

**Never commit `.env` to GitHub.**

---

## Running the Project

Run the main agent/test workflow:

```bash
python -m tests.test_graph
```

Provide a coding/debugging request such as:

```text
Fix the bug in workspace/sample_project/bug.py.
Run the file to identify the error.
Inspect the relevant source code.
Propose the smallest safe fix.
```

If a file modification is required, the graph pauses for human approval.

---

## Running Tests

Run the individual tool tests:

```bash
python -m tests.test_tools
```

Test Docker sandbox execution:

```bash
python -m tests.test_sandbox
```

Test the complete LangGraph workflow:

```bash
python -m tests.test_graph
```

Test the human approval workflow:

```bash
python -m tests.test_approval
```

---

## Example Agent Task

Suppose the project contains:

```python
result = calculate_total(10, 20)

print(total)
```

The agent can:

1. Locate the file.
2. Read the source.
3. Execute the program.
4. Receive the traceback.
5. Identify the undefined variable.
6. Propose a correction.
7. Pause for human approval.
8. Apply the approved edit.
9. Execute the program again.
10. Verify the successful result.

The final execution can return:

```text
STDOUT:
200

EXIT CODE: 0
```

---

## Technology Stack

### AI / Agent

* Python
* Google Gemini
* LangChain
* LangGraph

### Execution / Infrastructure

* Docker
* Docker Desktop
* Python 3.11

### Safety

* Workspace path validation
* Human-in-the-loop approval
* Exact text replacement
* Docker isolation
* Execution timeout
* Resource limits

---

## Why This Project?

A normal LLM chatbot produces text.

This project demonstrates an agent that can:

```text
Understand
   ↓
Inspect
   ↓
Execute
   ↓
Diagnose
   ↓
Propose
   ↓
Ask Permission
   ↓
Modify
   ↓
Verify
```

The important concept is that the LLM is not trusted to perform every operation directly.

The agent uses deterministic Python tools for actions and uses the LLM primarily for reasoning, tool selection, diagnosis, and explanation.

---

## Future Improvements

Possible future improvements include:

* Git-aware code changes
* Diff generation and visualization
* Better test discovery
* Multiple programming-language sandboxes
* Automated unit-test generation
* Static code analysis
* Patch rollback
* Persistent conversation memory
* Web-based interface

These are intentionally outside the current core scope.

---

## Project Status

**Core AI Code Agent: Complete**

The current implementation demonstrates:

* LLM reasoning
* Tool calling
* LangGraph state management
* File inspection
* Code execution
* Docker sandboxing
* Error diagnosis
* Human approval
* Safe file modification
* Post-edit verification
