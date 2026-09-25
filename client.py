import os
from openai import OpenAI


client = OpenAI(
    api_key= os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages =[
        {"role": "system","content" : "Your are a virtual assitant named friday skilled in genral tasks like Alexa and google cloud"},
             {"role": "user", "content": "what is time travel"}  ]
)

print(completion.choices[0].message.content)


# pip install openai
