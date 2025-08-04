import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(
        self,
        url: str = None,
        auth: tuple = None,
        database: str = "neo4j",  # type: ignore
    ) -> None:  # type: ignore
        if url is None:
            load_dotenv()
            url = os.getenv("NEO4J_URL")
            if not url:
                raise ValueError(
                    "please fill NEO4J_URL in .env file in the project's root"
                )
        self.database = database
        self.driver = GraphDatabase.driver(url, auth=auth)
