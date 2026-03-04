"""
Additional unit tests for interaction filtering and model defaults.

These are lightweight, pure-Python tests that avoid DB/network access
so they run quickly as part of the unit test suite.

All tests in this file (test_interactions_ai.py) are created by AI and are not modified by dev, only kept or rejected.
"""

from datetime import datetime

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id
from app.routers.interactions_old import _filter_by_item_id


# KEPT: this test is essential to check that all interactions with the same item_id are returned, not just the first one
def test_filter_multiple_matches_returns_all_matching_items() -> None:
    interactions = [
        InteractionLog(id=1, learner_id=10, item_id=42, kind="view"),
        InteractionLog(id=2, learner_id=11, item_id=42, kind="attempt"),
        InteractionLog(id=3, learner_id=12, item_id=43, kind="view"),
    ]

    result = _filter_by_item_id(interactions, 42)

    assert len(result) == 2
    assert {i.id for i in result} == {1, 2}



# KEPT: this test is important to check that no interactions when there is no such item_id in the interactions list
def test_filter_returns_empty_when_no_item_matches() -> None:
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=1, kind="a"),
        InteractionLog(id=2, learner_id=2, item_id=2, kind="b"),
    ]

    result_equal = _filter_by_item_id(interactions, 9999)
    assert result_equal == []

    result_max = filter_by_max_item_id(interactions, -9999)
    assert result_max == []



""" Dev requested a comment about intentions of that test

Dev comment: # FIXED: this test is a good idea to check the functionality, however, dev advises AI to give a comment about negative id cases
Prompt: Let us return to test_interactions_ai.py. Read the file and the comment. 
Take a look at the third test with ADVISED FIX. 
Write a comment explaining your vision on how you came to such idea and why it might be important to consider such case. 
Do not modify other tests and comments, write your answer in line 44 (use more lines if you consider it necessary)

AI answer:
Rationale / vision:
- I added a test for zero and negative `item_id` values because code that
  conditionally applies a filter (e.g. `if item_id:`) will treat `0` as
  falsy and therefore skip filtering — hiding a subtle bug.
- Negative IDs sometimes appear in fixtures, migrations, or external data
  during tests; ensuring the filter matches by equality (not by truthiness)
  prevents incorrect behavior when non-positive IDs are present.
- This check also documents the intended semantics: `item_id` is an
  exact-match filter and `None` means "no filter"; covering edge values
  guards against regressions and clarifies expectations for future devs.

Dev decision: KEEP
"""
# KEEP: this test is important to check that filter works correct for all item_id values, including edge cases like zero and negative numbers
def test_filter_handles_zero_and_negative_item_ids() -> None:
    interactions = [
        InteractionLog(id=1, learner_id=1, item_id=0, kind="zero"),
        InteractionLog(id=2, learner_id=2, item_id=-1, kind="neg"),
    ]

    result_zero = _filter_by_item_id(interactions, 0)
    assert len(result_zero) == 1 and result_zero[0].id == 1

    result_neg = _filter_by_item_id(interactions, -1)
    assert len(result_neg) == 1 and result_neg[0].id == 2

    result_all = filter_by_max_item_id(interactions, 0)
    assert len(result_all) == 2


# DISCARDED: this test is rather checking datetime.utcnow() behavior than InteractionLog and POST /interactions ones
# def test_created_at_default_is_recent_and_a_datetime() -> None:
#     before = datetime.utcnow()
#     entry = InteractionLog(id=None, learner_id=1, item_id=1, kind="k")
#     after = datetime.utcnow()
#     assert hasattr(entry, "created_at")
#     assert isinstance(entry.created_at, datetime)
#     # created_at should be between 'before' and 'after' timestamps
#     assert before <= entry.created_at <= after


# DISCARDED: this test repeats the test_filter_returns_all_when_max_item_id_is_none test
# def test_filter_returns_same_list_object_when_item_id_is_none() -> None:
#     interactions = [
#         InteractionLog(id=1, learner_id=1, item_id=1, kind="x"),
#     ]
#
#     result = _filter_by_item_id(interactions, None)
#
#     # When no filter is requested, the original list object should be returned
#     assert result is interactions
