from langgraph.graph import StateGraph,START,END
from typing import TypedDict

#define state

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float
    category: str

def calculate_bmi(state:BMIState) -> BMIState:
    weight = state["weight_kg"]
    height = state["height_m"]
    bmi  = weight / (height**2)
    state['bmi'] = round(bmi,2)
    return state

def label_bmi(state: BMIState) -> BMIState:
    bmi = state['bmi']
    if bmi < 18.5:
        state['category'] = "underweight"
    elif bmi < 25:
        state['category'] = "normal"
    elif bmi < 30:
        state['category'] = "overweight"
    else:
        state['category'] = "obese"
    return state


#define your graph
graph = StateGraph(BMIState)

# add nodes to your graph
graph.add_node("calculate_bmi",calculate_bmi)
graph.add_node("label_bmi",label_bmi)

# add edges to your graph
graph.add_edge(START,"calculate_bmi")
graph.add_edge('calculate_bmi',"label_bmi")
graph.add_edge("label_bmi",END)


# compile your graph
workflow = graph.compile()


#execute your graph
intial_state = {"weight_kg":50,"height_m":1.73}
output_state = workflow.invoke(intial_state)
print(output_state)


# from IPython.display import Image
# Image(workflow.get_graph().draw_mermaid_png()) # this code will work only in jupyter


