# Project Setup Guide

This guide will walk you through setting up your **Neo4j-based chatbot** from scratch. It covers:

- Installing dependencies  
- Setting up **Neo4j** and loading the dataset  
- Installing and configuring **Ollama**  
- Running the FastAPI backend  
- Launching the frontend  

---

## 1. Install Required Dependencies

Ensure you have **Python 3.8+** installed. Then install required packages:

```
pip install -r requirements.txt
```

---

## 2. Set Up Neo4j and Load the Dataset

### 2.1 Download and Install Neo4j

#### Option 1: Install Neo4j Desktop

1. **Download Neo4j** from [Neo4j Download Page](https://neo4j.com/download/).  
2. **Install and start Neo4j Desktop**.  
3. **Create a new database**.  
4. **Set a username and password** (default: `neo4j` / `password`).  
5. **Start the database**.  


### 2.2 Download or Use Your Own Dataset


To proceed, you **must have a dataset** with genes, diseases, and their relationships.

#### Option 1: Download the Pre-prepared Dataset
Use the provided dataset in dataset.txt

#### Option 2: Use Your Own Dataset

If you have a custom dataset:

1. **Place your CSV files** in Neo4j’s **import directory** (`neo4j/import/`).  

---

### 2.3 Load Data into Neo4j

Once **Neo4j is running**, open the [Neo4j Browser](http://localhost:7474) and execute the queries in Database.txt.


### 2.4 Verify Data in Neo4j

Run the following query to **check if nodes and relationships were created successfully**:

```
MATCH (n) RETURN n LIMIT 10;
```

To **visualize relationships**:

```
MATCH (g:Gene)-[r:ASSOCIATED_WITH]->(d:Disease) RETURN g, r, d LIMIT 10;
```

Now your **Neo4j database is fully loaded** and ready to use with the chatbot! 

---

## 3. Install and Set Up Ollama (LLM for Cypher Query Generation)

### 3.1 Download Ollama

Install **Ollama** to run a local LLM:

#### Mac/Linux:

```
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:

Download and install from [Ollama's official site](https://ollama.ai/download).  

---

### 3.2 Download DeepSeek-Coder 1.3B Model

Run:

```
ollama pull deepseek-coder:1.3b
```

If your system struggles with **large models**, use a **smaller LLM**.

---

### 3.3 Verify Ollama Installation

```
ollama run deepseek-coder:1.3b
```

If it starts an **interactive session**, Ollama is correctly installed.

---

## 4. Run the FastAPI Backend

### 4.1 Start the Backend API

Execute:

```
python app.py
```

If successful, you’ll see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 5. Launch the Frontend in a split terminal 

### 5.1 Start the Frontend

Run:

```
python frontend.py
```

This should **open a web interface** in your browser.

---

### 5.2 Test the Chatbot

1. Open the browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) .  
2. Enter a question like:

   ```
   What genes are associated with breast cancer?
   ```

3. The chatbot should return a **Cypher query and its Results**.

---

## 6. Troubleshooting

### Neo4j Issues

- If you **can't connect to Neo4j**, verify it's running:

  ```
  neo4j status
  ```

### API Not Responding

Check if **FastAPI is running**:

```
curl http://127.0.0.1:8000/health
```

**Expected response**:

```
{"status": "ok"}
```

---

### Ollama Model Too Large

If the LLM is too big, try a **smaller model**:

```
ollama pull mistral:7b
```

---
