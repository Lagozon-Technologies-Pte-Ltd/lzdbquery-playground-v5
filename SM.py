from openai import OpenAI
from IngestMetadata import schema_collection
import json
import os 
import openai
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION', "2024-02-01")
AZURE_DEPLOYMENT_NAME = os.environ.get('AZURE_DEPLOYMENT_NAME')
AZURE_EMBEDDING_DEPLOYMENT_NAME= os.environ.get('AZURE_EMBEDDING_DEPLOYMENT_NAME')

#openai_client = OpenAI(api_key="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")  # Use your OpenAI or Azure OpenAI key
openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT  
openai.api_version = AZURE_OPENAI_API_VERSION  
AZURE_EMBEDDING_DEPLOYMENT = AZURE_EMBEDDING_DEPLOYMENT_NAME

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model=os.environ['AZURE_EMBEDDING_DEPLOYMENT_NAME']
    )
    return response.data[0].embedding


def get_table_and_column_schema(query: str):
    query_embedding = embed_query(query)

    table_results = schema_collection.query(
        query_embeddings=[query_embedding],
        n_results=4,
        where={"type": "table"}
    )

    table_schema = []
    table_names = []
    for distance, id, doc, meta in zip(table_results['distances'][0], table_results['ids'][0], table_results['documents'][0], table_results['metadatas'][0]):
        
        table_schema.append({"distance": distance, "identity": id, "document": doc, "metadata": meta})
        table_names.append(id)

    column_results = schema_collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        where={"type": "column"}  
    )

    column_schema = []
    for distance, id, doc, meta in zip(column_results['distances'][0], column_results['ids'][0], column_results['documents'][0], column_results['metadatas'][0]):
        column_schema.append({"distance": distance, "identity": id, "document": doc, "metadata": meta})
    
    # print(type(table_schema), type(column_schema))
    return table_schema, column_schema


# print(get_table_and_column_schema("list the part amount and the labour amount for the RO RO25A007880"))
