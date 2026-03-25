"""Data Analyst LangGraph agent."""
from __future__ import annotations
import operator
from typing import Annotated, List, Optional, TypedDict
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver


class AnalystState(TypedDict):
    question: str
    schema: str
    sql: Optional[str]
    query_result: Optional[str]
    error: Optional[str]
    analysis: Optional[str]
    chart_spec: Optional[str]
    final_answer: str
    retry_count: int
    history: Annotated[List[str], operator.add]


def should_retry(state: AnalystState) -> str:
    if state.get("error") and state["retry_count"] < 3:
        return "retry"
    return "analyze"


def build_analyst_graph(schema_loader, sql_writer, executor, analyzer, visualizer):
    workflow = StateGraph(AnalystState)
    workflow.add_node("schema_loader", schema_loader.run)
    workflow.add_node("sql_writer", sql_writer.run)
    workflow.add_node("executor", executor.run)
    workflow.add_node("analyzer", analyzer.run)
    workflow.add_node("visualizer", visualizer.run)

    workflow.set_entry_point("schema_loader")
    workflow.add_edge("schema_loader", "sql_writer")
    workflow.add_edge("sql_writer", "executor")
    workflow.add_conditional_edges("executor", should_retry, {"retry": "sql_writer", "analyze": "analyzer"})
    workflow.add_edge("analyzer", "visualizer")
    workflow.add_edge("visualizer", END)

    return workflow.compile(checkpointer=MemorySaver())
