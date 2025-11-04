# This is the code for database.py

import qdrant_client
from sentence_transformers import SentenceTransformer
import uuid # Used to create unique IDs for our facts

# 1. Load the model that turns text into vectors (embeddings)
# This model runs on your computer. It might take a moment
# to download the first time it's used.
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model loaded.")

# 2. Set up the Qdrant database client
# We will use an "in-memory" database for simplicity.
# This means the database runs in RAM and is reset when
# the server stops.
client = qdrant_client.QdrantClient(":memory:")

# 3. Define the name of our "collection"
COLLECTION_NAME = "genai_facts"

# 4. Create the collection
# We tell Qdrant what kind of vectors we're storing
# The 'all-MiniLM-L6-v2' model creates vectors of size 384
print(f"Creating collection: {COLLECTION_NAME}")
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=qdrant_client.http.models.VectorParams(
        size=384,  # Size of the vectors from our model
        distance=qdrant_client.http.models.Distance.COSINE
    )
)
print("Collection created.")

# 5. A function to add new facts to our "memory"
def add_fact(fact_text: str):
    """Converts a text fact into a vector and stores it in Qdrant."""
    
    # Convert the text fact into a vector
    vector = model.encode(fact_text).tolist()
    
    # Give the fact a unique ID
    fact_id = str(uuid.uuid4())
    
    # Store the fact in Qdrant
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            qdrant_client.http.models.PointStruct(
                id=fact_id,
                vector=vector,
                payload={"text": fact_text} # The original text
            )
        ]
    )
    print(f"Added fact to memory: {fact_text}")

# 6. A function to search our "memory"
def search_memory(query_text: str):
    """Searches the Qdrant database for the most relevant fact."""
    
    # Convert the user's query into a vector
    query_vector = model.encode(query_text).tolist()
    
    # Search the database
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=1  # Return only the single best match
    )
    
    if search_results:
        # Return the text of the best matching fact
        return search_results[0].payload['text']
    else:
        return None

# --- 7. ADD OUR FIRST MEMORIES ---
# We feed the bot some specific knowledge.
print("Adding initial facts to the bot's memory...")
add_fact("LangChain is a framework for developing applications powered by language models.")
add_fact("RAG, or Retrieval-Augmented Generation, is a technique where a model retrieves facts from a database before answering a question.")
add_fact("Qdrant is a vector database used for high-performance similarity search.")
add_fact("Streamlit is a Python library used to create and share web apps for machine learning and data science.")
add_fact("FastAPI is a modern, fast web framework for building APIs with Python.")
print("Bot memory is ready.")