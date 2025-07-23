from langgraph.graph import StateGraph,START,END
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv
import os

model = AzureChatOpenAI(
    api_key=os.environ.get("AZURE_API_KEY"),
    model="gpt-4o-mini",
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    openai_api_version="2024-08-01-preview",
)


class BlogState(TypedDict):
    title: str
    outline: str
    content: str

def create_outline(state: BlogState) -> BlogState:
    title = state['title']
    prompt = f'Generate an detailedoutline for the blog topic: {title}'
    outline = model.invoke(prompt).content
    state['outline'] = outline
    return state

def create_blog(state: BlogState) -> BlogState:
    title = state['title']
    outline = state['outline']
    prompt = f'Write a detailed blog on the title - {title} based on the outline - {outline}'
    content = model.invoke(prompt).content
    state['content'] = content
    return state

graph = StateGraph(BlogState)

graph.add_node('create_outline',create_outline)
graph.add_node('create_blog',create_blog)

graph.add_edge(START,'create_outline')
graph.add_edge('create_outline','create_blog')
graph.add_edge('create_blog',END)

workflow = graph.compile()

intial_state = {"title":"How to train your dragon"}
output_state = workflow.invoke(intial_state)
print(output_state)

