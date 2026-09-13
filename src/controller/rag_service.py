from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient

from groq import Groq

from app.prompts.rag_prompt import RAG_PROMPT


class RAGService:

    def __init__(self):

        self.client = Groq()

        self.data_path = Path(
            "utils/knowledge.txt"
        )

        # -------------------------
        # Embedding Model
        # -------------------------

        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        # -------------------------
        # Qdrant Client
        # -------------------------

        self.qdrant_client = QdrantClient(
            url="http://localhost:6333"
        )

        self.collection_name = "rag_documents"

        # -------------------------
        # Vector Store
        # -------------------------

        self.vectorstore = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

            def ingest_document(self):

        # -------------------------
        # 1. Load TXT
        # -------------------------

        loader = TextLoader(
            str(self.data_path),
            encoding="utf-8"
        )

        documents = loader.load()

        # -------------------------
        # 2. Split
        # -------------------------

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(
            documents
        )

        # -------------------------
        # 3. Create embeddings
        # 4. Store in Qdrant
        # -------------------------

        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            url="http://localhost:6333",
            collection_name=self.collection_name,
        )

        return {
            "message": "Document indexed successfully",
            "chunks": len(chunks)
        }

        def retrieve(
        self,
        query: str,
        k: int = 4
    ):

        documents = self.vectorstore.similarity_search(
            query,
            k=k
        )

        return documents


        def generate_response(
        self,
        user_input: str
    ):

        # -------------------------
        # Retrieval
        # -------------------------

        documents = self.retrieve(
            user_input,
            k=4
        )

        # -------------------------
        # Context
        # -------------------------

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        # -------------------------
        # Prompt
        # -------------------------

        prompt = RAG_PROMPT.format(
            context=context,
            question=user_input
        )

        # -------------------------
        # LLM
        # -------------------------

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_completion_tokens=1024
        )

        answer = response.choices[0].message.content

        return {
            "question": user_input,
            "answer": answer,
            "sources": [
                {
                    "content": document.page_content,
                    "metadata": document.metadata
                }
                for document in documents
            ]
        }