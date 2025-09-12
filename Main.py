#home automation shiiiit
import os
import MainStrings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import tool
import logging
import importlib.util
import subprocess
from typing import List
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


ai_assistant = []

#Logging shit
log = logging.getLogger("Ai_asst")
logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

#LLM Definitions
llm_code = OllamaLLM(model=MainStrings.Models[0], temperature=0.5)
llm_general = OllamaLLM(model=MainStrings.Models[1], temperature=0.7)
llm_summary = OllamaLLM(model=MainStrings.Models[2], temperature=0.3)
router_llm = OllamaLLM(model=MainStrings.Models[3], temperature=0.3)

#External Tool Loader
def load_external_tools(folder: str = "agents", existingList: List[Tool] = []) -> List[Tool]:
    if not os.path.isdir(folder):
        log.warning("Tool folder '%s' not found.", folder)
        return existingList
    for fname in os.listdir(folder):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue
        path = os.path.join(folder, fname)
        try:
            spec = importlib.util.spec_from_file_location(fname[:-3], path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "tool") and isinstance(mod.tool, Tool):
                    existingList.append(mod.tool)
                    log.info("Loaded external tool: %s", mod.tool.name)
                else:
                    log.warning("No valid tool in %s", fname)
        except Exception as exc:
            log.warning("Failed to load %s: %s", fname, exc)
    return existingList

#define tools for shiiiit
@tool
def code_expert(query: str) -> str:
    """Expert at programming tasks and code generation."""
    print("code_expert(\""+query+"\")")
    return llm_code.invoke(query)

@tool
def general_expert(query: str) -> str:
    """Expert at general knowledge and reasoning."""
    print("general_expert(\""+query+"\")")
    return llm_general.invoke(query)

@tool
def summary_expert(query: str) -> str:
    """Expert at summarization and explanation."""
    print("summary_expert(\""+query+"\")")
    return llm_summary.invoke(query)

defaultTools = [general_expert, summary_expert]  # random registry to call for later
tools = load_external_tools(existingList=defaultTools)
ai_assistant =initialize_agent(
    tools=tools,
    llm=router_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

result = ""
try:
    if __name__ == "__main__":
        print(MainStrings.ReadyText)
        while True:
            user_input = input (MainStrings.UserPrompt)
            if user_input.lower() in MainStrings.ExitCommands:
                break
            result = ai_assistant.invoke({"input": user_input})
            print(result)
    else:
        raise ValueError("value error")
    print(f"AI_asst: {result}")
except KeyboardInterrupt:
    print("CTRL+C Pressed. Exiting...")
