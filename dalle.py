import os
import openai
from dotenv import load_dotenv

load_dotenv()
my_secret_key = os.getenv("OPENAI_API_KEY")
print(my_secret_key)
openai.api_key = my_secret_key
resp = openai.Image.create(
  prompt="britney baby",
  n=2,
  size="1024x1024"
)
print(resp)

