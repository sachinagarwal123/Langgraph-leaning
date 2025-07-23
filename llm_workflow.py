from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

model = AzureChatOpenAI(
    api_key=os.environ.get("AZURE_API_KEY"),
    model="gpt-4o-mini",
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    openai_api_version="2024-08-01-preview",
)

class LLMState(TypedDict):
    question: str
    answer: str

def llm_qa(state: LLMState) -> LLMState:
    question = state['question']
    prompt = f'Answer the following question: {question}'
    answer = model.invoke(prompt).content
    state['answer'] = answer
    return state



# create our graph
graph = StateGraph(LLMState)

graph.add_node('llm_qa',llm_qa)

graph.add_edge(START,'llm_qa')
graph.add_edge('llm_qa',END)

workflow = graph.compile()

intial_state = {"question":"What is the capital of France?"}
output_state = workflow.invoke(intial_state)
print(output_state)