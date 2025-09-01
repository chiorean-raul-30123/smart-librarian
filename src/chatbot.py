import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
from chromadb import PersistentClient

# -------------------- SETUP --------------------
# Încarcă cheia API din fișierul .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)

embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key=api_key
)
# Creează un client persistent pentru vectorii salvați pe disc
chroma_client = PersistentClient(path="vector_db")
collection = chroma_client.get_collection(name="books", embedding_function=embedding_func)

# -------------------- SUMMARIES --------------------
# Dicționar cu rezumate complete pentru fiecare titlu cunoscut
book_summaries_dict = {
    "The Hobbit": (
        "Bilbo Baggins, un hobbit confortabil și fără aventuri, este luat prin surprindere "
        "atunci când este invitat într-o misiune de a recupera comoara piticilor păzită de dragonul Smaug. "
        "Pe parcursul călătoriei, el descoperă curajul, loialitatea și resursele interioare pe care nu știa că le are. "
        "Întâlnește elfi, orci, gnomi și un inel magic care va deveni legendar. "
        "Această aventură definește teme de prietenie, maturizare și depășirea propriilor limite."
    ),
    "1984": (
        "Romanul lui George Orwell prezintă o societate distopică în care gândirea liberă este considerată crimă, "
        "iar cetățenii sunt supravegheați permanent de o autoritate totalitară numită Big Brother. "
        "Winston Smith, un angajat al Ministerului Adevărului, începe să pună la îndoială realitatea impusă de partid. "
        "Începe o relație clandestină și o revoltă personală care îl va duce spre distrugere. "
        "Este o poveste despre libertate, control, manipulare psihologică și represiune ideologică."
    ),
    "To Kill a Mockingbird": (
        "Scout Finch își petrece copilăria în sudul segregaționist al Americii anilor ’30, observând nedreptățile lumii adulte. "
        "Tatăl ei, avocatul Atticus Finch, apără un bărbat de culoare acuzat pe nedrept de viol. "
        "Prin ochii inocenți ai lui Scout și ai fratelui ei, romanul explorează teme de rasism, moralitate și compasiune. "
        "Este o poveste profundă despre umanitate și lupta pentru justiție într-o societate nedreaptă."
    ),
    "Brave New World": (
        "Aldous Huxley imaginează o societate viitoare unde totul este controlat genetic și psihologic pentru a menține fericirea. "
        "Nu există familie, religie sau emoții autentice – doar conformitate și consum. "
        "Bernard Marx și John, ‘sălbaticul’, înfruntă aceste reguli, punând sub semnul întrebării noțiunea de libertate. "
        "O critică ascuțită a hedonismului, tehnologiei fără control moral și uniformizării sociale."
    ),
    "The Catcher in the Rye": (
        "Holden Caulfield, un adolescent alienat, fuge din internatul său și petrece câteva zile rătăcind prin New York. "
        "Este dezgustat de ipocrizia adulților și încearcă să găsească autenticitatea într-o lume falsă. "
        "Vocea sa cinică, confuză și sensibilă l-a transformat într-un simbol al adolescenței moderne. "
        "Romanul explorează teme precum identitatea, izolare, trauma și tranziția spre maturitate."
    ),
    "Fahrenheit 451": (
        "Guy Montag este un pompier însărcinat cu arderea cărților într-o societate în care cititul este interzis. "
        "După o întâlnire cu o tânără visătoare, începe să se îndoiască de valorile sistemului și caută cunoașterea. "
        "Într-o lume de ecrane, cenzură și manipulare, el luptă pentru libertate intelectuală. "
        "Romanul este un manifest pentru importanța gândirii critice și a libertății de exprimare."
    ),
    "The Alchemist": (
        "Santiago, un păstor andaluz, visează la o comoară ascunsă lângă piramide și pornește într-o călătorie inițiatică. "
        "Pe drum întâlnește oameni care îl învață lecții spirituale despre destin, iubire și ascultarea inimii. "
        "Romanul este o alegorie despre sensul vieții și încrederea în propria chemare interioară. "
        "Temele centrale sunt descoperirea sinelui și urmarea visului personal (‘Legenda Personală’)."
    ),
    "The Lord of the Rings": (
        "Inelul Puterii, creat de maleficul Sauron, trebuie distrus pentru a salva Pământul de Mijloc. "
        "Frodo, un hobbit modest, acceptă sarcina grea de a transporta inelul până la Muntele Destinului. "
        "Împreună cu prietenii lui și alte creaturi magice, pornește într-o călătorie epică. "
        "Romanul este o capodoperă despre sacrificiu, prietenie, bine vs. rău, și puterea aparent celor slabi."
    ),
    "Animal Farm": (
        "Animalele de la o fermă preiau conducerea într-o revoltă împotriva oamenilor. "
        "Inițial proclamă egalitatea, dar porcii preiau controlul și devin noii tirani. "
        "Romanul este o satiră dură la adresa comunismului sovietic, simbolizând degradarea idealurilor revoluționare. "
        "Se axează pe teme de putere, corupție și manipulare politică."
    ),
    "Life of Pi": (
        "Piscine Molitor ‘Pi’ Patel supraviețuiește unui naufragiu în mijlocul oceanului, trăind luni de zile într-o barcă alături de un tigru bengalez. "
        "Romanul îmbină supraviețuirea cu spiritualitatea, imaginația și credința. "
        "Povestea sa este atât realistă, cât și alegorică, provocând cititorul să aleagă între fapte și credință. "
        "Temele principale sunt supraviețuirea, divinitatea și natura adevărului."
    ),
    "Slaughterhouse-Five": (
        "Billy Pilgrim, un soldat american, este capturat în timpul celui de-al Doilea Război Mondial și supraviețuiește bombardamentului de la Dresda. "
        "Este ‘dezlipit de timp’ și călătorește între război, viața postbelică și o planetă extraterestră. "
        "Romanul este o critică absurdă a războiului, combinând realitatea dură cu elemente science-fiction. "
        "Temele includ trauma, absurditatea vieții și lipsa de control asupra destinului."
    ),
    "The Book Thief": (
        "Liesel Meminger, o fetiță germană, descoperă puterea cuvintelor în timpul celui de-al Doilea Război Mondial. "
        "Furând și citind cărți interzise, găsește refugiu din realitatea brutală în povești. "
        "Naratorul este Moartea, care oferă o perspectivă emoționantă și poetică asupra războiului și umanității. "
        "Romanul explorează compasiunea, curajul, pierderea și supraviețuirea prin literatură."
    )
}

# -------------------- TOOLS --------------------
# Definim funcția locală care poate fi apelată de GPT ca "tool"
def get_summary_by_title(title: str) -> str:
    return book_summaries_dict.get(title, "Rezumat complet indisponibil.")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_summary_by_title",
            "description": "Returnează rezumatul complet pentru o carte",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Titlul exact al cărții"
                    }
                },
                "required": ["title"]
            }
        }
    }
]

# -------------------- RETRIEVER --------------------
# Funcție care face căutare semantică în ChromaDB pentru a găsi titlul relevant
def retrieve_books(query: str):
    results = collection.query(query_texts=[query], n_results=1)
    document = results['documents'][0][0]
    title = results['metadatas'][0][0]['title']
    return title, document

# -------------------- CHAT LOOP --------------------
# Bucla principală de chat unde interacționezi cu utilizatorul și gestionezi apelurile GPT
while True:
    user_input = input("\nCe fel de carte cauți? (scrie 'exit' pentru a ieși)\n> ")
    if user_input.lower() == "exit":
        break

    try:
        title, context = retrieve_books(user_input)

        messages = [
            {"role": "system", "content": "Ești un bibliotecar AI care recomandă cărți pe baza intereselor utilizatorului."},
            {"role": "user", "content": f"Vreau o carte despre: {user_input}"},
            {"role": "assistant", "content": f"Îți recomand cartea '{title}'. {context}"}
        ]

        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            tool_call = choice.message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if function_name == "get_summary_by_title":
                summary = get_summary_by_title(arguments["title"])

                messages.append(choice.message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": summary
                })

                final_response = openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )

                print("\nRecomandare completă:")
                print(final_response.choices[0].message.content)

        else:
            print("\nRecomandare simplă:")
            print(choice.message.content)

    except Exception as e:
        print("Eroare:", e)
