"""Tests for dds_glossary.main module."""

from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import MonkeyPatch


def test_init_datasets(client: TestClient, monkeypatch: MonkeyPatch) -> None:
    """Test the /init_datasets endpoint."""
    saved_datasets = [
        {"dataset": "saved.rdf", "dataset_url": "http://example.com/saved.rdf"}
    ]
    failed_datasets = [
        {"dataset": "failed.rdf", "dataset_url": "http://example.com/failed.rdf"}
    ]
    monkeypatch.setattr(
        "dds_glossary.controllers.GlossaryController.init_datasets",
        lambda *_, **__: (saved_datasets, failed_datasets),
    )

    response = client.post("/init_datasets")
    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "saved_datasets": saved_datasets,
        "failed_datasets": failed_datasets,
    }


def test_get_concept_schemes_empty(client: TestClient) -> None:
    """Test the /schemes endpoint with an empty database."""
    response = client.get("/schemes")
    assert response.json() == {"concept_schemes": []}
    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == "application/json"