import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

# 1. Load Environment Variables Securely
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(" API key not found. Please check your .env file.")

# 2. Initialize the LLM (The Brain)
# Using the latest gemini-3.8-flash as required by the Google API
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", google_api_key=API_KEY, temperature=0)

# 3. Define the Tools
# Tool 1: Real-time Web Search
search_tool = DuckDuckGoSearchRun(
    name="web_search",
    description="Useful for current events, real-time data, or general knowledge. Input should be a search query."
)

# Tool 2: Python Math Calculator
python_tool = PythonREPLTool(
    name="python_calculator",
    description="Useful for math, calculations, or running Python code. Input must be valid Python code and must print() the result, e.g., 'print(25 * 4 + 10)'."
)

# Tool 3: Local File Reader (Custom Tool)
@tool
def read_local_file(file_path: str) -> str:
    """Reads the content of a local text file. Use this to read files like 'sample_resume.txt'."""
    # LLMs often wrap paths in quotes or backticks. We strip them to prevent FileNotFoundError.
    clean_path = file_path.strip().strip("\"'`")
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: The file '{clean_path}' was not found in the current directory."
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Combine tools into a list
tools = [search_tool, python_tool, read_local_file]

# 4. The ReAct Prompt (The Reasoning Framework)
# This teaches the LLM how to think step-by-step and use the tools.
REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(REACT_PROMPT)

# 5. Build and Return the Agent Executor
def get_agent_executor():
    """Creates and returns the configured Agent Executor."""
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,             # Prints the Thought/Action/Observation loop to console
        handle_parsing_errors=True, # Prevents crashes if the LLM formats JSON incorrectly
        max_iterations=10         # Safety net to stop infinite loops
    )