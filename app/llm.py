
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model= "gemini-3.5-flash-lite",
    google_api_key= api_key,
    temperature= 0
)

