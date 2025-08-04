from langgraph.graph import StateGraph,START,END
from typing import Any, Dict, List, Optional,Annotated,TypedDict
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI,AzureChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver,MemorySaver
import os 
from dotenv import load_dotenv
load_dotenv()

llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    model="gpt-4o-mini",
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version="2024-08-01-preview",
)



class JokeState(TypedDict):

    topic: str
    joke: str
    explanation: str



def generate_joke(state: JokeState):

    prompt = f'generate a joke on the topic {state["topic"]}'
    response = llm.invoke(prompt).content

    return {'joke': response}

def generate_explanation(state: JokeState):

    prompt = f'write an explanation for the joke - {state["joke"]}'
    response = llm.invoke(prompt).content

    return {'explanation': response}


graph = StateGraph(JokeState)

graph.add_node('generate_joke', generate_joke)
graph.add_node('generate_explanation', generate_explanation)

graph.add_edge(START, 'generate_joke')
graph.add_edge('generate_joke', 'generate_explanation')
graph.add_edge('generate_explanation', END)

checkpointer = InMemorySaver()

workflow = graph.compile(checkpointer=checkpointer)


config1 = {"configurable": {"thread_id": "1"}}
workflow.invoke({'topic':'pizza'}, config=config1)

workflow.get_state(config1)

list(workflow.get_state_history(config1))


#Fault Tolerance


