from langchain.tools import Tool
from langchain_community.retrievers import BM25Retriever


class data_tools:
    def __init__(self, docs: list):
        self.bm25_retriever = BM25Retriever.from_documents(docs)
        self.check_tool = Tool(
            name="job invitation retriever",
            func=self.extract_text,
            description="Use this tool to extract text from the job invitation pdf"
        )

    def extract_text(self, query: str) -> str:
        """Use this tool to extract text from the job invitation pdf"""
        results = self.bm25_retriever.invoke(query)

        if results:
            return "\n\n".join([doc for doc in results[:3]])
        

