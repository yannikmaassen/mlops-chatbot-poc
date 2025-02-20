import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=".env.local")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing! Add it to the .env file.")

openai_client = OpenAI(api_key=api_key)

__all__ = ["openai_client"]