from agent_core import get_agent_executor

def format_chat_history(history: list) -> str:
    """Formats previous turns so the agent has context."""
    if not history:
        return "None"
    return "\n".join([f"{role}: {text}" for role, text in history])

def main():
    print("🚀 Initializing Multi-Tool Autonomous AI Agent...\n")
    
    # Initialize the brain
    agent_executor = get_agent_executor()
    
    print("=" * 60)
    print(" AGENT READY! Type your compound research queries below.")
    print("Examples:")
    print("  - 'What is the current price of Bitcoin? Multiply it by 2.'")
    print("  - 'Read sample_resume.txt and tell me the candidate's name.'")
    print("Type 'exit' to quit.")
    print("=" * 60)

    # Memory storage for the session
    chat_history = [] 

    while True:
        try:
            user_query = input("\n❓ You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n Agent shutting down. Goodbye!")
            break
            
        if not user_query:
            continue
        if user_query.lower() in ["exit", "quit"]:
            print("👋 Agent shutting down. Goodbye!")
            break

        print("\n🤖 Agent Thinking (watch the reasoning chain)...")
        
        try:
            # Invoke the agent with the query and formatted history
            response = agent_executor.invoke({
                "input": user_query,
                "chat_history": format_chat_history(chat_history)
            })
            
            final_answer = response["output"]
            
            print("\n✅ Final Answer:")
            print("-" * 40)
            print(final_answer)
            print("-" * 40)
            
            # Save to memory for the next turn
            chat_history.append(("User", user_query))
            chat_history.append(("Assistant", final_answer))
            
        except Exception as e:
            print(f"\n❌ System Error: {e}")
            print("Please try rephrasing your question.")

if __name__ == "__main__":
    main()