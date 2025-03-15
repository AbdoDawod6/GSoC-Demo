import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
import ollama
import re

# Initialize FastAPI app
app = FastAPI()

# Neo4j Database Credentials
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "123456789"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Request Model for API
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Welcome to the GSoC Chatbot API! Visit /docs for Swagger UI."}

# 🏛 **Updated Schema**
SCHEMA = """
- `(:Gene)-[:ASSOCIATED_WITH]->(:Disease)`
- `(:Gene)-[:REGULATES]->(:Protein)`
- `(:Disease)-[:HAS_SYMPTOM]->(:Symptom)`
- `(:Gene)-[:INTERACTS_WITH]->(:Gene)`
- `(:Drug)-[:TREATS]->(:Disease)`
- `(:Person)-[:HAS_CONDITION]->(:Disease)`
"""

# 📌 **Example Queries**
EXAMPLES = """
**Q:** Find genes related to Lung Cancer.
**A:** MATCH (g:Gene)-[:ASSOCIATED_WITH]->(d:Disease {name: "Lung Cancer"}) RETURN g.name;

**Q:** Find all relationships for the gene "APOE".
**A:** MATCH (g:Gene {name: "APOE"})-[r]->(n) RETURN type(r), labels(n), n.name;

**Q:** Find diseases related to the gene "TP53".
**A:** MATCH (g:Gene {name: "TP53"})-[:ASSOCIATED_WITH]->(d:Disease) RETURN d.name;

**Q:** Find drugs that treat Alzheimer's.
**A:** MATCH (dr:Drug)-[:TREATS]->(d:Disease {name: "Alzheimer's"}) RETURN dr.name;
"""

@app.post("/generate-cypher/")
def generate_cypher(request: QueryRequest):
    """ Generate a valid Cypher query from natural language """

    # Construct the LLM prompt
    full_prompt = f"""
    You are a **Neo4j Cypher query expert**. Generate a precise **Cypher MATCH query** based on the user's question.
    
    **⚠️ STRICT RULES:**
    1️⃣ **Only return the Cypher query** (no explanations, no comments).
    2️⃣ **Start the response with `MATCH`**.
    3️⃣ **Ensure the query is syntactically correct for Neo4j.**
    4️⃣ **Do not include any additional text, headers, or formatting.**

    ### **Schema**
    {SCHEMA}

    ### **Examples**
    {EXAMPLES}

    ### **User Question:**
    {request.question}
    """

    print("[🔹 Sending prompt to Ollama LLM...]")
    response = ollama.chat(
        model="deepseek-coder:1.3b",
        messages=[{"role": "system", "content": "Create a valid Neo4j Cypher query."},
                  {"role": "user", "content": full_prompt}]
    )

    cypher_query = response["message"]["content"].strip()

    # 🛑 **Fix: Remove Extra Text After `RETURN` Clause**
    cypher_query = re.split(r"\n", cypher_query)[0]  # Keep only the first line
    cypher_query = re.sub(r";.*$", "", cypher_query)  # Remove extra comments

    # 🛑 **Ensure Query Starts with MATCH and Contains RETURN**
    if not cypher_query.startswith("MATCH") or "RETURN" not in cypher_query:
        raise HTTPException(status_code=400, detail="Generated Cypher query is invalid.")

    print(f"[✅ Generated Cypher Query]\n{cypher_query}")

    return run_cypher_query(cypher_query)

def run_cypher_query(query: str):
    """ Executes Cypher query in Neo4j and returns results """
    try:
        with driver.session() as session:
            result = session.run(query)
            data = [record.data() for record in result]
            print("[🔹 Neo4j Query Results]", data)
            return {"query": query, "results": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neo4j Error: {str(e)}")

# 🚀 **Run Uvicorn when executing `python app.py`**
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
