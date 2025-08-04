from langgraph.graph import StateGraph,START,END
from typing import Any, Dict, List, Optional,Annotated,TypedDict
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_openai import ChatOpenAI,AzureChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import os 
from dotenv import load_dotenv
load_dotenv()

model = AzureChatOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    model="gpt-4o-mini",
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    openai_api_version="2024-08-01-preview",
)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    # take user query from state
    message = state['messages']

    # send to llm
    response = model.invoke(message)
    # response store state
    return {'messages': [response]}


checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot_workflow = graph.compile(checkpointer=checkpointer)

# initial_state = {"messages": [HumanMessage(content="What is the capital of France?")]}
# output_state = chatbot_workflow.invoke(initial_state)
# print(output_state['messages'][-1].content)  # Print the response from the model


thread_id = '1'
config = {'configurable': {'thread_id': thread_id}}
while True:
    user_input = input("Type here: ")
    print('You:', user_input)

    if user_input.strip().lower() in ["exit", "quit",'bye']:
        print("Exiting the chatbot. Goodbye!")
        break

    config = {'configurable' : {'thread_id': thread_id}}

    response = chatbot_workflow.invoke({"messages": [HumanMessage(content=user_input)]},config=config)
    print('AI',response['messages'][-1].content)  # Print the response from the model