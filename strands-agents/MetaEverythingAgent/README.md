# Meta-Everything Agent (Strands SDK Implementation)

A self-evolving AI system built on the [Strands SDK](https://github.com/strands-agents/sdk-python) that embodies a "meta-everything" philosophy. Meta-Everything Agent dynamically adapts to any problem domain through runtime tool creation, multi-agent orchestration, and continuous learning.

## Features

### Meta-Everything Capabilities

**Meta-Agent**: Dynamically spawns specialized agents for complex tasks using the swarm tool

**Meta-Tooling**: Creates and modifies tools at runtime using the editor tool

**Meta-Learning**: Persistent cross-session memory enables continuous improvement

**Meta-Cognition**: Self-reflection and confidence assessment drives strategic decisions

**External Integration**: Access web APIs and external data sources using the http_request tool

**System Operations**: Install packages and run system commands using the shell tool

**Time Awareness**: Track time across timezones for scheduling and temporal analysis using the current_time tool

## Quick Start

### Prerequisites

- Python 3.10+
- AWS credentials configured (for Bedrock models)
- (Optional) Mem0 API key or OpenSearch instance for cloud memory

### Installation

```bash
# Clone the repository
git clone https://github.com/sriaradhyula/agentic-community-meta-agent.git
cd agentic-community-meta-agent/strands-agents/MetaEverythingAgent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package and dependencies
pip install -e .

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

### Basic Usage

```bash
# Simple task
python -m src.main "Create a tool to analyze sentiment in text"

# Complex task with more steps
python -m src.main "Build a system to monitor and visualize server health metrics" --steps 20

# Use a different model
python -m src.main "Generate a financial report" --model us.anthropic.claude-3-5-sonnet-20241022-v1:0

# Disable thinking mode for faster execution
python -m src.main "Summarize this document" --no-thinking

# Custom memory location
python -m src.main "Learn about quantum computing" --memory-path ./quantum_memory

# Fetch external data
python -m src.main "Get the current weather in San Francisco and analyze the trend"

# Install and use packages
python -m src.main "Install and use pandas to analyze a CSV file"

# Time-based task
python -m src.main "Create a reminder system that tracks tasks with timestamps"
```

## Architecture

```mermaid
graph TB
    subgraph "Meta-Everything Agent Core"
        A[MetaEverythingAgent Class] --> B[Dynamic Prompts]
        A --> C[Memory System]
        A --> D[Tool Integration]
    end
    
    subgraph "Meta Capabilities"
        E[Meta-Agent<br/>Swarm Orchestration]
        F[Meta-Tooling<br/>Runtime Creation]
        G[Meta-Learning<br/>Persistent Memory]
        H[Meta-Cognition<br/>Self-Reflection]
    end
    
    subgraph "External Tools"
        I[HTTP Request]
        J[Shell Commands]
        K[Python REPL]
        L[File Editor]
        M[Time Awareness]
    end
    
    A --> E
    A --> F
    A --> G
    A --> H
    
    D --> I
    D --> J
    D --> K
    D --> L
    D --> M
    
    style A fill:#1976d2,color:#fff
    style E fill:#388e3c,color:#fff
    style F fill:#f57c00,color:#fff
    style G fill:#7b1fa2,color:#fff
    style H fill:#d32f2f,color:#fff
```

### Project Structure

```
MetaEverythingAgent/
├── src/
│   ├── agent.py       # Core MetaEverythingAgent class
│   ├── prompts.py     # System prompts enabling meta behaviors
│   ├── main.py        # CLI interface
│   └── tools/
│       ├── __init__.py
│       └── memory.py  # Memory management tool
├── pyproject.toml     # Project configuration
├── .env.example       # Environment template
└── README.md          # Documentation
```

## How It Works

```mermaid
flowchart TD
    A[User Objective] --> B{Analyze Problem}
    B --> C[Check Memory]
    C --> D{Confidence Level?}
    
    D -->|High >80%| E[Direct Execution]
    D -->|Medium 50-80%| F[Create Tools]
    D -->|Low <50%| G[Spawn Agents]
    
    E --> H[Execute Solution]
    F --> I[Test & Deploy]
    G --> J[Coordinate Swarm]
    
    I --> H
    J --> H
    
    H --> K[Store Learnings]
    K --> L[Complete Objective]
    
    style A fill:#e1f5fe
    style L fill:#c8e6c9
    style K fill:#fff3e0
```

### Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant MetaEverythingAgent
    participant Memory
    participant Tools
    participant Swarm
    
    User->>MetaEverythingAgent: Provide Objective
    MetaEverythingAgent->>Memory: Retrieve Similar Experiences
    Memory-->>MetaEverythingAgent: Past Solutions & Insights
    
    MetaEverythingAgent->>MetaEverythingAgent: Assess Confidence
    
    alt High Confidence
        MetaEverythingAgent->>Tools: Use Existing Tools
        Tools-->>MetaEverythingAgent: Execute & Return Results
    else Medium Confidence
        MetaEverythingAgent->>Tools: Create New Tool
        MetaEverythingAgent->>Tools: Test Tool
        Tools-->>MetaEverythingAgent: Tool Ready
    else Low Confidence
        MetaEverythingAgent->>Swarm: Spawn Specialized Agents
        Swarm->>Memory: Share Context
        Swarm-->>MetaEverythingAgent: Collaborative Results
    end
    
    MetaEverythingAgent->>Memory: Store New Learnings
    MetaEverythingAgent->>User: Return Solution
```

## Examples

### Creating a Custom Tool

```python
from src import MetaEverythingAgent

agent = MetaEverythingAgent()
result = agent.run("Create a tool to fetch and parse RSS feeds")
# Meta-Everything Agent will create a custom RSS parser tool and test it
```

### Multi-Agent Orchestration

```python
result = agent.run("Analyze market trends and generate investment recommendations")
# Meta-Everything Agent will spawn research, analysis, and recommendation agents
```

### Learning from Experience

```python
# First run
result = agent.run("Build a web scraper for news articles")

# Later run - will use learned strategies
result = agent.run("Create a scraper for blog posts")
```

## Memory Backends

```mermaid
graph LR
    A[Meta-Everything Agent] --> B{Memory Backend}
    
    B --> C[FAISS<br/>Local Storage]
    B --> D[Mem0 Platform<br/>Cloud Memory]
    B --> E[OpenSearch<br/>AWS Managed]
    
    C --> F[No Config Needed]
    D --> G[API Key Required]
    E --> H[Host URL Required]
    
    style A fill:#2196f3,color:#fff
    style C fill:#4caf50,color:#fff
    style D fill:#ff9800,color:#fff
    style E fill:#9c27b0,color:#fff
```

### FAISS (Default)
Local vector storage
- No configuration needed
- Stores in `./meta_everything_agent_memory_*`

### Mem0 Platform
Cloud-based memory
- Set `MEM0_API_KEY` in `.env`
- Automatic cloud sync

### OpenSearch
AWS managed search
- Set `OPENSEARCH_HOST` in `.env`
- Enterprise-scale memory

## CLI Options

```bash
python -m src.main [objective] [options]

Options:
  --model MODEL         Model ID (default: Sonnet 4 for Bedrock, llama3.2:3b for Ollama)
  --server TYPE         Server type: 'remote' or 'local' (default: remote)
  --steps STEPS         Max execution steps (default: 10)
  --no-thinking        Disable interleaved thinking
  --memory-path PATH   Custom FAISS memory location
  --no-memory          Disable memory system
  --verbose, -v        Enable verbose logging
```

## Dependencies

Meta-Everything Agent uses:
- `strands-agents==0.1.6` - Core agent framework
- `strands-agents-tools` - Extended tool library from feature branch
- `mem0ai` - Memory management system
- `faiss-cpu` - Vector storage backend
- `boto3` - AWS SDK for Bedrock models
- `opensearch-py` - OpenSearch client
- `rich` - Terminal formatting

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
