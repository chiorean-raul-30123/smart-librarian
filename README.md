# smart-librarian
Book recommendation chatbot with GPT, RAG and Tool Calling based on the user's interests

# contributors 
developed with Adina Denisa Horj 

## quick start (local)
```
# 1. create & activate venv
python -m venv venv
.\venv\Scripts\activate

# 2. install deps
 pip install -r requirements.txt

# 3. create .env file
OPENAI_API_KEY=sk-***
CHROMA_OPENAI_API_KEY=sk-***

# 4. create vector store
python build_vector_db.py

# 5. launch chatbot 
python chatbot.py

# sample calls 
Vreau o carte despre magie si aventura.
Ce îmi recomanzi dacă iubesc poveștile fantastice?

## project layout 
smart-librarian-main/
|-- src/
    |-- build_vector_db.py        # creează vector DB local (ChromaDB)
    |-- chatbot.py                # CLI chatbot cu GPT + Tool Calling
|-- data/
    |-- book_summaries.md         # 10+ cărți în format structurat
|-- .env                          # chei OpenAI
|-- requirements.txt              # dependențe (openai, chromadb, dotenv)
