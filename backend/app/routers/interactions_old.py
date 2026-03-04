"""Filter from old fork"""

from app.models.interaction import InteractionLog

def _filter_by_item_id(
    interactions: list[InteractionLog], item_id: int | None
) -> list[InteractionLog]:
    if item_id is None:
        return interactions
    return [i for i in interactions if i.item_id == item_id] # fix: filter interactions by item_id instead of learner_id
