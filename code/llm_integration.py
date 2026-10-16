import os
from dotenv import load_dotenv
from openai import OpenAI

# Step 1: Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is missing!")

# Step 2: Initialize OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Step 3: Define our assistant
system_prompt = """
You are an AI Business Research Assistant.

Your responsibilities:
1. Help entrepreneurs evaluate business ideas.
2. Analyze potential market opportunities.
3. Identify business risks.
4. Provide practical business recommendations.
5. Clearly distinguish facts from assumptions.
"""

# Step 4: Ask a business question
question = input("Enter your business research question: ")

# Step 5: Send the question to the AI model
try:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=500
    )

    # Step 6: Display the response
    print("\n===== AI Business Research =====\n")

    print(response.choices[0].message.content)

except Exception as error:
    print(f"API Error: {error}")