from app.llm import llm


response = llm.invoke("What is Python? Answer in one sentence.")

print(response.text)

