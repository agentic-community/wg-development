"""Meta-Everything Agent - A self-evolving AI system that adapts to any problem domain."""

import logging
import os
from typing import Any, Dict, List, Optional, Union
from strands import Agent
from strands.models import BedrockModel
from strands_tools import (
    swarm, editor, load_tool, think, 
    python_repl, stop, http_request, shell, current_time
)
from .prompts import get_meta_system_prompt
from .tools import mem0_memory

logger = logging.getLogger(__name__)


class MetaEverythingAgent(Agent):
    """
    A self-evolving agent that embodies the "meta-everything" philosophy.
    
    Capabilities:
    - Meta-Agent: Spawns specialized agents for complex tasks
    - Meta-Tooling: Creates and modifies tools at runtime
    - Meta-Learning: Learns from experiences across sessions
    - Meta-Cognition: Reflects on approaches and adapts strategies
    """
    
    # Model configurations
    THINKING_MODELS = [
        "us.anthropic.claude-opus-4-20250514-v1:0",
        "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        "us.anthropic.claude-sonnet-4-20250514-v1:0"
    ]
    
    DEFAULT_BEDROCK_MODEL = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    DEFAULT_OLLAMA_MODEL = "llama3.2:3b"
    
    def __init__(
        self, 
        model_id: Optional[str] = None,
        server_type: str = "remote",
        thinking: bool = True,
        objective: Optional[str] = None,
        max_steps: int = 10,
        additional_tools: Optional[List[Any]] = None,
        **kwargs
    ):
        """
        Initialize MetaAgent with meta capabilities.
        
        Args:
            model_id: Model identifier (default: Sonnet 3.7 for Bedrock, llama3.2:3b for Ollama)
            server_type: "remote" for Bedrock or "local" for Ollama
            thinking: Enable interleaved thinking mode (only for supported models)
            objective: The objective to accomplish (used for dynamic prompt generation)
            max_steps: Maximum steps allowed for completing the objective
            additional_tools: Additional tools to include
            **kwargs: Additional arguments passed to base Agent
        """
        meta_tools = [
            swarm,
            editor,
            load_tool,
            mem0_memory,
            think,
            python_repl,
            http_request,
            shell,
            current_time,
            stop
        ]
        
        # Add any additional tools
        if additional_tools:
            meta_tools.extend(additional_tools)
        
        if server_type == "local":
            if not model_id:
                model_id = self.DEFAULT_OLLAMA_MODEL
            model_config = {
                "model_id": model_id,
                "base_url": os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            }
            thinking = False
        else:
            if not model_id:
                model_id = self.DEFAULT_BEDROCK_MODEL
            
            supports_thinking = model_id in self.THINKING_MODELS and thinking
            
            if supports_thinking:
                model_config = BedrockModel(
                    model_id=model_id,
                    region_name='us-east-1',
                    model_kwargs={
                        "temperature": 1.0,
                        "max_tokens": 4026,
                        "anthropic_beta": ["interleaved-thinking-2025-05-14"],
                        "thinking": {"type": "enabled", "budget_tokens": 8000}
                    }
                )
            else:
                model_config = BedrockModel(
                    model_id=model_id,
                    region_name='us-east-1',
                    model_kwargs={
                        "temperature": 0.95,
                        "max_tokens": 4096,
                        "top_p": 0.95
                    }
                )
        
        self.server_type = server_type
        self.objective = objective
        self.max_steps = max_steps
        self.current_step = 0
        self.tools_list = ", ".join([tool.name if hasattr(tool, 'name') else str(tool) for tool in meta_tools])
        
        if objective:
            system_prompt = get_meta_system_prompt(
                objective=objective,
                current_step=1,
                max_steps=max_steps,
                server_type=server_type,
                tools_available=self.tools_list
            )
        else:
            system_prompt = kwargs.get('system_prompt', 'You are MetaAgent, an adaptive AI system.')
        
        super().__init__(
            model=model_config,
            tools=meta_tools,
            system_prompt=system_prompt,
            **kwargs
        )
        
        self.created_tools = []
        self.spawned_agents = []
        self.learning_count = 0
        
        if objective:
            self._initialize_context(objective)
    
    def __call__(self, message: str = None, **kwargs) -> str:
        """
        Override call to update system prompt dynamically based on progress.
        
        This allows the agent to work within the Strands event loop while
        maintaining awareness of its progress toward the objective.
        """
        self.current_step += 1
        
        if self.objective and self.current_step <= self.max_steps:
            self.system_prompt = get_meta_system_prompt(
                objective=self.objective,
                current_step=self.current_step,
                max_steps=self.max_steps,
                server_type=self.server_type,
                tools_available=self.tools_list
            )
        
        if message is None and self.objective:
            message = f"Continue working on the objective. This is step {self.current_step} of {self.max_steps}."
        elif message is None:
            message = "How can I help you today?"
        
        result = super().__call__(message, **kwargs)
        
        return result
    
    def _initialize_context(self, objective: str):
        """Initialize execution context by checking memory for relevant past experiences."""
        try:
            memories = self.tool.mem0_memory(
                action="retrieve",
                query=objective,
                user_id="meta_agent"
            )
            
            if memories and len(memories) > 0:
                logger.info(f"Found {len(memories)} relevant memories")
        except Exception as e:
            logger.warning(f"Memory initialization failed: {e}")
    
    def reset(self):
        """Reset the agent state for a new objective."""
        self.current_step = 0
        self.created_tools = []
        self.spawned_agents = []
        self.learning_count = 0
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the execution."""
        return {
            "steps_taken": self.current_step,
            "tools_created": self.created_tools,
            "agents_spawned": self.spawned_agents,
            "learnings_stored": self.learning_count
        }