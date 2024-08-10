from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.duckdb import DuckDBVectorStore
from llama_index.core import StorageContext

from IPython.display import Markdown, display
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

import duckdb
import os
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini")

embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
)

Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader("./data/").load_data()

vector_store = DuckDBVectorStore(database_name="gym.duckdb", table_name="gym", persist_dir="./", embed_dim=1536,
                                 text_search_config={"overwrite": True})
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# con = duckdb.connect("datacamp.duckdb")
# tb = con.execute("SHOW ALL TABLES").fetchdf()

query_engine = index.as_query_engine()
response = query_engine.query("What all exercise are available?")
display(Markdown(f"<b>{response.response}</b>"))

if __name__ == '__main__':
    pass
