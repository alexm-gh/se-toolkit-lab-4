"""End-to-end tests for the GET /interactions endpoint."""

import httpx

def test_get_interactions_is_200(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_is_list(client: httpx.Client) -> None:
    response = client.get("/interactions/")
    assert isinstance(response.json(), list)

