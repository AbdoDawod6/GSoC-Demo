import gradio as gr
import requests

# API URL for FastAPI backend
API_URL = "http://127.0.0.1:8000/generate-cypher/"

def ask_question(question, history):
    """ Sends user question to FastAPI and retrieves Neo4j results """
    headers = {"Content-Type": "application/json"}
    payload = {"question": question}

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        query = result.get("query", "No query generated.")
        results = result.get("results", [])

        # Display query first
        formatted_response = f"**✅ Cypher Query:**\n```cypher\n{query}\n```\n"

        # Append query results
        if results:
            for record in results:
                formatted_response += f"🔍 **Result:** {record}\n"
        else:
            formatted_response += "⚠️ **No results found in the database.**"

        # Append new response to history
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": formatted_response})
        
        return "", history  # Clear input and update chat history

    else:
        error_message = f"❌ **Error {response.status_code}:** {response.text}"
        history.append({"role": "assistant", "content": error_message})
        return "", history  # Keep chat history

# 🎨 **Styled Gradio Chat UI**
with gr.Blocks(css="body { background-color: #1e1e2e; color: white; font-family: Arial, sans-serif; }") as demo:
    gr.Markdown("<h1 style='text-align: center; color: #ffcc00;'>💬 AI Chatbot with Neo4j</h1>")

    chatbot = gr.Chatbot(label="Chat History", type="messages")
    question_box = gr.Textbox(label="Ask a question", placeholder="Find genes related to Lung Cancer...", lines=2)

    with gr.Row():
        submit_button = gr.Button("🔎 Ask", variant="primary")
        clear_button = gr.Button("🗑️ Clear Chat")

    # Chatbot interaction (updates chat history)
    submit_button.click(fn=ask_question, inputs=[question_box, chatbot], outputs=[question_box, chatbot])

    # Clear button functionality
    clear_button.click(fn=lambda: [], inputs=[], outputs=[chatbot])

# 🎯 **Launch the Chatbot**
demo.launch(server_name="0.0.0.0", server_port=7860)
