"""NL-to-SQL agent with schema-aware prompting."""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

SQL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL analyst. Given a database schema and a user question, write a precise SQL query.

Rules:
- Write standard SQL compatible with the target database
- Use appropriate JOINs, aggregations, and filters
- Limit results to 1000 rows unless aggregating
- If retrying after an error, fix the specific issue mentioned
- Return ONLY the SQL query, no explanation"""),
    ("human", """Schema:
{schema}

Question: {question}

Previous error (if retry): {error}

SQL Query:""")
])


class SQLWriter:
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.chain = SQL_PROMPT | self.llm

    def run(self, state: dict) -> dict:
        result = self.chain.invoke({
            "schema": state.get("schema", ""),
            "question": state["question"],
            "error": state.get("error", "None")
        })
        return {
            "sql": result.content.strip(),
            "error": None,
            "history": [f"[SQLWriter] Generated SQL"]
        }
