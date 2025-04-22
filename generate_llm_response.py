from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai import ChatOpenAI

from tools import call_vectordb
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/rag_for_ncert/.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

tools = [call_vectordb]

llm = ChatOpenAI(temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. If the question is related to sound, use the vector DB for a more accurate answer."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x.get("chat_history", []),
        "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def generate_llm_response(input_text, chat_history=None):
    response = agent_executor.invoke({"input": input_text, "chat_history": chat_history or []})
    return response