import chromadb
# from chromadb.config import Settings
from chromadb.utils import embedding_functions
import json
import os

# Load your prepared metadata
with open("./expanded_columns.json",encoding="utf-8") as f:
    columns = json.load(f)
with open("./expanded_tables.json",encoding="utf-8") as f:
    tables = json.load(f)


# After loading columns and tables:
# print("Columns count:", len(columns))  # Check if columns is empty
# print("Tables count:", len(tables))    # Check if tables is empty

AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', "2024-02-01")
AZURE_DEPLOYMENT_NAME = os.environ.get('AZURE_DEPLOYMENT_NAME')
AZURE_EMBEDDING_DEPLOYMENT_NAME= os.environ.get('AZURE_EMBEDDING_DEPLOYMENT_NAME')

Chroma_Schema_Metadata = os.environ.get('Chroma_Schema_Metadata')




import chromadb.utils.embedding_functions as embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=AZURE_OPENAI_API_KEY,               
    api_base=AZURE_OPENAI_ENDPOINT,            
    api_type="azure",
    api_version=AZURE_OPENAI_API_VERSION,       
    model_name=AZURE_EMBEDDING_DEPLOYMENT_NAME         
)


# Initialize ChromaDB persistent client (new API)
client = chromadb.PersistentClient(path=Chroma_Schema_Metadata)  # Only the path argument is needed[4]


# Create a collection for schema elements (tables + columns)
# schema_collection = client.get_or_create_collection(name="schema_elements")
schema_collection = client.get_or_create_collection(
    name="schema_elements"
    , embedding_function=openai_ef
    
)


def serialize_metadata(metadata):
    return {
        k: json.dumps(v) if isinstance(v, (list, dict)) else v
        for k, v in metadata.items()
    }

# def prepare_ingest(items):
#     filtered_items = [item for item in items if isinstance(item, dict) and 'id' in item]
#     ids = [item['id'] for item in filtered_items]
#     documents = [item['document'] for item in filtered_items]
#     metadatas = [item['metadata'] for item in filtered_items]
#     return ids, documents, metadatas

def prepare_ingest(items):
    ids = []
    documents = []
    metadatas = []

    for item in items:
        if "column_name" in item:  # Column
            ids.append(item["column_name"])
            documents.append(item["column_desc"])
            metadatas.append(serialize_metadata(item["metadata"]))
        elif "table_name" in item:  # Table
            ids.append(item["table_name"])
            documents.append(item["table_desc"])
            metadatas.append(serialize_metadata(item["metadata"]))
    
    return ids, documents, metadatas

ids, documents, metadatas = prepare_ingest(columns + tables)

# Ingest into ChromaDB
schema_collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)
