#!/usr/bin/env python3
"""
Meta-Everything Agent CLI - A self-evolving AI system that adapts to any problem domain.

Usage:
    python main.py "Your objective here"
    python main.py "Create a tool to analyze stock prices" --model us.anthropic.claude-opus-4-20250514-v1:0
    python main.py "Build a weather monitoring system" --steps 20
    python main.py "Solve this problem" --server local --model llama3.2:3b
    python main.py "Create an API client" --no-thinking
"""

import argparse
import logging
import sys
import os
from typing import Optional
from .agent import MetaEverythingAgent
from .tools import initialize_memory_system

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity."""
    if verbose:
        logging.getLogger("strands").setLevel(logging.DEBUG)
        logging.getLogger("meta_agent").setLevel(logging.DEBUG)
    else:
        logging.getLogger("strands").setLevel(logging.INFO)
        logging.getLogger("meta_agent").setLevel(logging.INFO)


def main():
    """Main entry point for Meta-Everything Agent CLI."""
    parser = argparse.ArgumentParser(
        description="Meta-Everything Agent - A self-evolving AI system that adapts to any problem domain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using default Bedrock model (Sonnet 3.7)
  python main.py "Create a web scraper for news articles"
  
  # Using specific Bedrock model with thinking
  python main.py "Build a data analysis pipeline" --model us.anthropic.claude-opus-4-20250514-v1:0
  
  # Using local Ollama model
  python main.py "Solve complex math problems" --server local --model llama3.2:3b
  
  # Extended execution with verbose output
  python main.py "Generate a report on climate data" --steps 20 --verbose
  
  # Custom memory location
  python main.py "Learn about quantum computing" --memory-path ./quantum_memory
        """
    )
    
    parser.add_argument(
        "objective",
        help="The objective or problem to solve"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help="Model ID to use (default: Sonnet 3.7 for Bedrock, llama3.2:3b for Ollama)"
    )
    
    parser.add_argument(
        "--server",
        choices=["remote", "local"],
        default="remote",
        help="Server type: 'remote' for Bedrock, 'local' for Ollama (default: remote)"
    )
    
    parser.add_argument(
        "--steps",
        type=int,
        default=10,
        help="Maximum number of execution steps (default: 10)"
    )
    
    parser.add_argument(
        "--no-thinking",
        action="store_true",
        help="Disable interleaved thinking mode (only affects supported models)"
    )
    
    parser.add_argument(
        "--memory-path",
        type=str,
        help="Custom path for FAISS memory storage (default: auto-generated)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--no-memory",
        action="store_true",
        help="Disable memory system (useful for testing)"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    os.environ["BYPASS_TOOL_CONSENT"] = "true"

    try:
        if not args.no_memory:
            memory_config = None
            if args.memory_path:
                memory_config = {
                    "vector_store": {
                        "config": {
                            "path": args.memory_path
                        }
                    }
                }
            initialize_memory_system(config=memory_config)
        
        display_model = args.model or (MetaEverythingAgent.DEFAULT_BEDROCK_MODEL if args.server == "remote" else MetaEverythingAgent.DEFAULT_OLLAMA_MODEL)
        logger.info(f"Initializing Meta-Everything Agent with model: {display_model}")
        
        agent = MetaEverythingAgent(
            model_id=args.model,
            server_type=args.server,
            thinking=not args.no_thinking,
            objective=args.objective,
            max_steps=args.steps
        )
        
        logger.info(f"Starting objective: {args.objective}")
        print(f"\n{'='*60}")
        print(f"Objective: {args.objective}")
        print(f"Server: {args.server.capitalize()}")
        print(f"Model: {display_model}")
        print(f"Max Steps: {args.steps}")
        print(f"Thinking: {'Enabled' if not args.no_thinking and args.server == 'remote' else 'Disabled'}")
        print(f"Memory: {'Enabled' if not args.no_memory else 'Disabled'}")
        print(f"{'='*60}\n")
        
        print("\nMeta-Everything Agent is working...\n")
        
        result = agent(f"""You have been given the following objective: {args.objective}

You have up to {args.steps} steps to complete this objective. You are currently on step 1.

Please work autonomously to complete the objective. When you have successfully completed the objective or determined it cannot be completed, use the stop() tool with an appropriate reason.

Remember:
- Check memory for relevant past experiences
- Use available tools effectively
- Create new tools if needed
- Store learnings for future use
- Call stop() when the objective is complete

Begin working on the objective now.""")
        
        summary = agent.get_execution_summary()
        
        print(f"\n{'='*60}")
        print("Execution Complete!")
        print(f"{'='*60}")
        print(f"Steps taken: {summary['steps_taken']}")
        print(f"Tools created: {len(summary['tools_created'])}")
        if summary['tools_created']:
            for tool in summary['tools_created']:
                print(f"  - {tool}")
        print(f"Agents spawned: {len(summary['agents_spawned'])}")
        if summary['agents_spawned']:
            for agent_info in summary['agents_spawned']:
                print(f"  - {agent_info}")
        print(f"Learnings stored: {summary['learnings_stored']}")
        print(f"{'='*60}\n")
        
        if result:
            print("Final Result:")
            print("-" * 60)
            print(result)
            print("-" * 60)
        
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()