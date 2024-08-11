from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.duckdb import DuckDBVectorStore

llm = OpenAI(model="gpt-4o-mini")

embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
)

Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader("./data/gym/").load_data()

vector_store = DuckDBVectorStore(database_name="gym.duckdb", table_name="gym", persist_dir="./", embed_dim=1536,
                                 text_search_config={"overwrite": True})
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# con = duckdb.connect("datacamp.duckdb")
# tb = con.execute("SHOW ALL TABLES").fetchdf()

# query_engine = index.as_query_engine()
# response = query_engine.query("Suggest a 5 min exercise for neck and how to do it")
# display(Markdown(f"<b>{response.response}</b>"))

memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

chat_engine = CondensePlusContextChatEngine.from_defaults(
    index.as_retriever(),
    memory=memory,
    llm=llm
)

response = chat_engine.chat(
    "Suggest a 5 min exercise for neck and how to do it"
)
print(response.response)

response = chat_engine.chat(
    "Could you please provide another one?"
)
print(response.response)

if __name__ == '__main__':
    pass
