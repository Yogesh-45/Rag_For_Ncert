from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai import ChatOpenAI


from voice_agent import VoiceAgent
from tools import call_vectordb
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='D:/yogi/LLM/sarvam/llm_app/backend/.env')
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

tools = [call_vectordb]



def generate_llm_response(retrieved_content, history= None):
    """
    Placeholder function to generate LLM response.
    Replace this with your actual LLM integration.
    """

    llm = ChatOpenAI(temperature=0, )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system","you are an powerful assistant who answer all queries. You must look into vectordb if query\
         is related to sound"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser())

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response= agent_executor.invoke({"input": retrieved_content})
    print(f'response check: {response}')

    VoiceAgent(response)

    print(f'voice agent k baad wala function')

    return response['output']