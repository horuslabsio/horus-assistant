import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import FireCrawlLoader

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
INDEX_NAME = "horus-index"

urls = [
    [
        "https://sneaky-angelfish-80f.notion.site/Sample-team-introduction-ce8192e19acd49468f64260f6554a916",
        "https://sneaky-angelfish-80f.notion.site/Vacation-Policy-Perks-0a2c9a2291874c7ba3fcdbd6f4fda613",
        "https://sneaky-angelfish-80f.notion.site/Expense-Policy-3a18a68743034e34ae766e177fa3007f",
    ],
    [
        "https://sneaky-angelfish-80f.notion.site/Getting-Started-bb16e30ec6644465ac1d93a857b5ea93",
    ],
]


def ingest():
    for url in urls[0]:
        print(f"***Scraping {url}***")
        loader = FireCrawlLoader(api_key=firecrawl_api_key, url=url, mode="scrape")
        docs_scraped = loader.load()

    for url in urls[1]:
        print(f"***Crawling {url}***")
        loader = FireCrawlLoader(api_key=firecrawl_api_key, url=url, mode="crawl")
        docs_crawled = loader.load()

    all_docs = docs_crawled + docs_scraped
    print(f"***Adding data to Pinecone***")
    PineconeVectorStore.from_documents(
        documents=all_docs, embedding=embeddings, index_name=INDEX_NAME
    )
    print(f"***Loading to vectorstore done!***")


if __name__ == "__main__":
    ingest()
