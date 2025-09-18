import chromadb

from semantic_service import ModelType, get_llm_model

# import chromadb
# client = chromadb.PersistentClient(path="./chroma_db")
# collection = client.get_or_create_collection(name="sky_news_sample_collection")


class VectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="sky_news_sample_collection"
        )

    def health_check(self):
        try:
            _ = self.collection.count()
            return True
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def get_semantic_data(self, query, n_results=3):
        embed_model = get_llm_model(ModelType.EMBED)
        query_embedding = embed_model.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["metadatas", "documents"],
        )
        return results["documents"]  # List of lists of documents


class CloudStore:
    def __init__(self):
        pass


class StoreFactory:
    # env - based ahh
    pass
