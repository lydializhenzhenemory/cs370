import openai
import numpy as np

# Load the API key from a file
with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()

# Set the API key
openai.api_key = api_key

# Define your prompt
prompt = "Your prompt goes here"

# Make a request to the OpenAI API using GPT-4
response = openai.Completion.create(
  engine="gpt-4", # Specify the GPT-4 engine
  prompt=prompt,
  max_tokens=100, # Adjust based on your needs
  n=1, # Number of completions to generate
  stop=None, # Optional: Specify stopping criteria
  temperature=0.7 # Adjust creativity. Lower is more deterministic
)

# Print the text of the response
print(response.choices[0].text.strip())
