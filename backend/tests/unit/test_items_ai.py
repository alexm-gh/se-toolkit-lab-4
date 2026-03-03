"""Additional unit tests for item models and schemas.

These tests exercise model defaults, attribute handling, and schema
defaults without touching the database so they run quickly.

All tests in this file (test_items_ai.py) are created by AI and are not modified by dev.

All tests are kept by dev as all of them cover cases of items functionality.
"""

from datetime import datetime

from app.models.item import ItemRecord, ItemCreate, ItemUpdate

def test_itemrecord_defaults_and_created_at() -> None:
    before = datetime.utcnow()
    item = ItemRecord(title="Sample Item")
    after = datetime.utcnow()

    assert item.type == "step"
    assert item.description == ""
    assert isinstance(item.attributes, dict)
    assert hasattr(item, "created_at")
    assert isinstance(item.created_at, datetime)
    assert before <= item.created_at <= after


def test_itemcreate_and_itemupdate_schema_defaults() -> None:
    create = ItemCreate(title="Create Title")
    assert create.type == "step"
    assert create.parent_id is None
    assert create.description == ""

    update = ItemUpdate(title="New Title")
    assert update.title == "New Title"
    assert update.description == ""


def test_itemrecord_attributes_accepts_nested_structures() -> None:
    nested = {"levels": [1, {"a": "b"}], "flag": True}
    item = ItemRecord(title="With attrs", attributes=nested)

    assert isinstance(item.attributes, dict)
    assert item.attributes["levels"][1]["a"] == "b"
    assert item.attributes["flag"] is True
