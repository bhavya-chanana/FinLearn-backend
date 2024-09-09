from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Initialize the client with the model and API token
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token="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",  # Replace with your actual Hugging Face API token
)

# Initialize the retrieval model
retriever = SentenceTransformer('all-MiniLM-L6-v2')

# Example document corpus (you should replace this with your actual documents)
corpus = [
    """Title: Finance Basics for Everyone: A Guide for Women, Children, and Teenagers

Introduction:

Brief overview of the importance of understanding finance.
Explanation of how financial literacy can impact life decisions and future stability.
Chapter 1: Understanding Money

For Women:

Empowerment through Finance: Understanding budgeting and saving to achieve financial independence.
Managing Household Finances: Tips for tracking expenses, setting financial goals, and creating a budget.
Investing Basics: Introduction to investment options and their importance for long-term financial health.
For Children:

What is Money?: Simple explanation of money and its uses.
Saving and Spending: The basics of saving money in a piggy bank and the importance of budgeting.
Fun Financial Activities: Interactive games and activities to teach saving and smart spending.
For Teenagers:

Earning Money: Understanding part-time jobs, allowances, and entrepreneurial activities.
Budgeting Basics: How to create a simple budget and track personal expenses.
Savings and Goals: Setting financial goals and understanding the importance of saving for future needs.
Chapter 2: Budgeting and Saving

For Women:

Creating a Personal Budget: Steps to develop a budget that suits individual needs.
Saving for Emergencies: Importance of an emergency fund and how to build one.
Retirement Planning: Basics of retirement savings and investment options.
For Children:

Piggy Bank Savings: Simple methods for saving and understanding how savings grow.
Understanding Needs vs. Wants: Teaching the difference between needs and wants and how to prioritize.
For Teenagers:

Managing Your Money: Using apps or spreadsheets to track income and expenses.
Building a Savings Habit: Tips for setting aside money regularly and tracking progress.
Chapter 3: Introduction to Investing

For Women:

Investment Basics: Introduction to stocks, bonds, and mutual funds.
Risk and Return: Understanding the relationship between risk and potential returns.
Investment Strategies: Tips for starting with low-risk investments and gradually building a diverse portfolio.
For Children:

What is Investing?: Simplified explanation of investing and its benefits.
Saving vs. Investing: Basic differences between saving money and investing it.
For Teenagers:

Types of Investments: Overview of common investment options like savings accounts, stocks, and bonds.
Investment Apps and Tools: Introduction to tools and apps that help manage investments and track growth.
Chapter 4: Financial Responsibility

For Women:

Debt Management: Understanding different types of debt and strategies for managing and reducing it.
Credit Scores: Basics of credit scores and their impact on financial health.
For Children:

Understanding Debt: Simple explanation of borrowing and repaying money.
Responsibility with Money: Basic principles of being responsible with money and making smart choices.
For Teenagers:

Building Credit: How to start building a positive credit history and why it matters.
Avoiding Debt: Tips for avoiding unnecessary debt and managing existing debt responsibly.
Conclusion:

Summary of key points for each group.
Encouragement to continue learning and seeking resources for financial education.
Appendix:

Additional resources for further reading.
Contact information for financial advisors or educational programs."""
]

# Encode the corpus
corpus_embeddings = retriever.encode(corpus, convert_to_tensor=True)

def retrieve_documents(query, corpus_embeddings, corpus):
    query_embedding = retriever.encode(query, convert_to_tensor=True)
    # Compute similarity scores
    scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0].tolist()  # Convert to list
    # Retrieve top 3 documents
    top_results = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    return [corpus[i] for i in top_results]

def chat():
    print("Chatbot: Hello! I'm a chatbot. Type 'exit' to end the conversation.")
    
    # Define the system prompt
    system_prompt = "You are an expert financial advisor. Provide clear and concise answers to financial queries.\
        When the conversation strarts with someone, always ask about their age and gender. Give your advice based on the gender and age.\
        Always ask small queries after answering questions so that the user is able to understand more about finance."
    
    while True:
        user_input = input("You: ")
        
        # Exit the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # Retrieve relevant documents
        retrieved_docs = retrieve_documents(user_input, corpus_embeddings, corpus)
        context_with_docs = "\n".join(retrieved_docs)
        
        # Generate a response from the model with the system prompt and context
        responses = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},  # System prompt
                {"role": "user", "content": f"Context: {context_with_docs}\nQuestion: {user_input}"}
            ],
            max_tokens=500,
            stream=True,
        )
        
        response_text = ""
        for message in responses:
            response_text += message.choices[0].delta.content
        
        # Print the model's response
        print(f"Chatbot: {response_text}")

if __name__ == "__main__":
    chat()
