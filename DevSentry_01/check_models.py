import os
from dotenv import load_dotenv
from google import genai

# Load your API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Scanning your API key for approved Gemma models...\n")

# Loop through and print every model that has "gemma" in the name
for model in client.models.list():
    if "gemma" in model.name.lower():
        print(f"Exact API String: '{model.name}'")