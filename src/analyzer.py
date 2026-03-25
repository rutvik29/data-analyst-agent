"""Pandas-based data analysis agent."""
import json
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

ANALYST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a senior data analyst. Analyze the query results and provide clear, business-focused insights. Mention key numbers, trends, anomalies, and recommendations."),
    ("human", "Question: {question}\n\nSQL: {sql}\n\nResults (first 20 rows):\n{results}\n\nProvide analysis:")
])

class DataAnalyzer:
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0.1)
        self.chain = ANALYST_PROMPT | self.llm

    def run(self, state: dict) -> dict:
        results_raw = state.get("query_result", "[]")
        df = pd.DataFrame(json.loads(results_raw))
        top_rows = df.head(20).to_string(index=False) if not df.empty else "No results"
        result = self.chain.invoke({"question": state["question"], "sql": state.get("sql",""), "results": top_rows})
        return {"analysis": result.content, "history": ["[Analyzer] Generated insights"]}
