import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello, test message"}],
    model="llama3-70b-8192"
)
print("Response:", response.choices[0].message.content)