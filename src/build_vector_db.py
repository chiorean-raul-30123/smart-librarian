import chromadb
from chromadb.utils import embedding_functions
import openai
import os
from dotenv import load_dotenv
from chromadb.config import Settings
load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key=openai.api_key
)


client = chromadb.PersistentClient(path="vector_db")


collection = client.create_collection(name="books", embedding_function=embedding_func)


with open("data/book_summaries.md", "r", encoding="utf-8") as f:
    raw_data = f.read()


entries = raw_data.split("## Title: ")[1:]

for idx, entry in enumerate(entries):
    lines = entry.strip().split("\n")
    title = lines[0].strip()
    summary = " ".join(lines[1:]).strip()

    collection.add(
        documents=[summary],
        metadatas=[{"title": title}],
        ids=[str(idx)]
    )

print(f" Vector DB construit cu {len(entries)} cărți.")
