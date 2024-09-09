from flask import Flask, jsonify, request
from functions import get_expenses, add_expense
from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer, util
import numpy as np

app = Flask(__name__)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        data = request.json
        result = add_expense(data)
        return jsonify(result)
    else:
        return jsonify(get_expenses())


# Initialize the client with the model and API token
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="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",  # Replace with your actual Hugging Face API token
)

# Initialize the retrieval model
retriever = SentenceTransformer('all-MiniLM-L6-v2')

# Example document corpus
corpus = [
    """Title: Finance Basics for Everyone: A Guide for Women, Children, and Teenagers
    ...
    """
]

# Encode the corpus
corpus_embeddings = retriever.encode(corpus, convert_to_tensor=True)

def retrieve_documents(query, corpus_embeddings, corpus):
    query_embedding = retriever.encode(query, convert_to_tensor=True)
    # Compute similarity scores
    scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0].tolist()
    # Retrieve top documents
    top_results = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    return [corpus[i] for i in top_results]

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Retrieve relevant documents
    retrieved_docs = retrieve_documents(user_message, corpus_embeddings, corpus)
    context_with_docs = "\n".join(retrieved_docs)

    # Define the system prompt
    system_prompt = "You are an expert financial advisor. Provide clear and concise answers to financial queries. Always give advice based on gender and age."

    # Generate a response from the model with the system prompt and context
    responses = client.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": f"Context: {context_with_docs}\nQuestion: {user_message}"}
        ],
        max_tokens=500,
        stream=False,
    )

    response_text = responses["choices"][0]["message"]["content"]

    return jsonify({'response': response_text})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
