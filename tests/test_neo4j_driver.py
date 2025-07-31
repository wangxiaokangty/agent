import pytest

from core.driver.neo4j.driver import Neo4jClient


@pytest.mark.filterwarnings("ignore:")
def test_driver_initialize_from_dotenv():
    client = Neo4jClient()
    assert client is not None
