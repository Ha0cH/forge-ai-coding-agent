# Forge AI Coding Agent

Forge is a command-line AI coding assistant built with Python and the Gemini API. It uses function calling to inspect files, read and modify code, and execute Python programs within a controlled working directory.

The project demonstrates core concepts behind modern AI agents, including tool calling, iterative reasoning loops, file system interactions, and safe code execution.

## Features

- Read file contents
- List files and directories
- Write and modify files
- Execute Python scripts
- Gemini function calling integration
- Iterative agent feedback loop
- Working directory sandboxing for safer file operations

## Tech Stack

- Python 3.13
- Gemini API (google-genai)
- Function Calling
- argparse
- dotenv

## Project Structure

```text
forge/
├── main.py
├── prompts.py
├── config.py
├── functions/
│   ├── call_functions.py
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
└── calculator/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Ha0cH/forge-ai-coding-agent.git 
cd forge-ai-coding-agent
```

Create and activate a virtual environment:

```bash
python -m venv .venv source .venv/bin/activate 
```

Install dependencies:

```bash
pip install -r requirements.txt 
```

Create a .env file:

```env
GEMINI_API_KEY=your_api_key_here 
```

## Usage

Basic prompt:

```bash
uv run main.py "What files are in the root directory?" 
```

Read a file:

```bash
uv run main.py "Read pkg/calculator.py" 
```

Fix a bug:

```bash
uv run main.py "Fix the bug in pkg/calculator.py" 
```

Enable verbose mode:

```bash
uv run main.py "Read main.py" --verbose 
```

## How It Works

1. The user enters a prompt.
2. Forge sends the request to Gemini.
3. Gemini decides whether a tool should be used.
4. Forge executes the requested tool.
5. Tool results are returned to Gemini.
6. Gemini continues reasoning until a final response is generated.

This creates an agent loop that allows the model to interact with a codebase rather than only generating text.

## Example Tools

### get_files_info

Lists files and directories within the working directory.

### get_file_content

Reads file contents safely within the sandboxed workspace.

### write_file

Creates or modifies files inside the working directory.

### run_python_file

Executes Python files with optional command-line arguments and captures output.

## Safety

Forge restricts file access to a configured working directory and validates paths before reading, writing, or executing files. This helps prevent accidental access to files outside the project workspace.

## Learning Objectives

This project was built to explore:

- Agentic AI workflows
- Function calling
- Tool execution
- File system operations
- Python subprocess management
- Secure path validation
- Iterative LLM reasoning loops

## Future Improvements

- Additional development tools
- Multi-file code refactoring
- Test execution and analysis
- Git integration
- Improved error recovery and retry handling
- Support for additional LLM providers

## License

MIT License