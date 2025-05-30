from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama,OllamaEmbeddings
def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings