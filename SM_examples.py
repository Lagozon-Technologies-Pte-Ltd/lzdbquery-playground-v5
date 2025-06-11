from openai import OpenAI
from IngestExamples import schema_collection
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


def get_examples(query: str):
    query_embedding = embed_query(query)

    example_results = schema_collection.query(
        query_embeddings=[query_embedding],
        n_results=2
     
    )

    example_result = []
  
    for id , document in zip(example_results['ids'][0], example_results['documents'][0]):
        
        example_result.append({"input": id, "query": document})
      

   
    return example_result


# print(get_examples("Show all customer verbatim entries for a specific RO RO25A007880"))
