import os
from dotenv import load_dotenv
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

INDEX_NAME = "horus-index"


def query_agent(query: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    document_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)
    agent = create_retrieval_chain(
        retriever=docsearch.as_retriever(), combine_docs_chain=document_chain
    )

    result = agent.invoke(input={"input": query})

    return result["answer"]


if __name__ == "__main__":
    query_agent("What is Horus labs?")
