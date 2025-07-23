from langgraph.graph import StateGraph,START,END
from typing import TypedDict


class BatesmanState(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int

    sr: float
    bpb: float
    boundary_rate: float
    summary: str

def calculate_sr(state:BatesmanState) -> BatesmanState:
    runs = state['runs']
    balls = state['balls']
    sr = (runs/balls)*100
    return {'sr':sr}

def calculate_bpb(state:BatesmanState) -> BatesmanState:
    fours = state['fours']
    sixes = state['sixes']
    bpb = state['balls']/(fours + sixes)
    state['bpb'] = bpb
    return {'bpb':bpb}

def calculate_boundary_percent(state:BatesmanState) -> BatesmanState:
    fours = state['fours']*4
    sixes = state['sixes']*6
    boundary_rate = (fours + sixes)/state['runs']
    state['boundary_rate'] = boundary_rate*100
    return {'boundary_rate':boundary_rate}

def summary(state:BatesmanState) -> BatesmanState:
    summary = f"""
        Strike Rate - {state['sr']} \n
        balls per boundary - {state['bpb']} \n
        boundary percentage - {state['boundary_rate']}
    """
    return {'summary':summary}


graph = StateGraph(BatesmanState)

graph.add_node('calculate_sr',calculate_sr)
graph.add_node('calculate_bpb',calculate_bpb)
graph.add_node('calculate_boundary_percent',calculate_boundary_percent)
graph.add_node('summary',summary)


graph.add_edge(START,'calculate_sr')
graph.add_edge(START,'calculate_bpb')
graph.add_edge(START,'calculate_boundary_percent')

graph.add_edge('calculate_sr','summary')
graph.add_edge('calculate_bpb','summary')
graph.add_edge('calculate_boundary_percent','summary')

graph.add_edge('summary',END)

workflow = graph.compile()

intial_state = {"runs":50,"balls":100,"fours":20,"sixes":10}
output_state = workflow.invoke(intial_state)
print(output_state)