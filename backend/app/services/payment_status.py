VALID_STATUS_TRANSITIONS = {
    "created": ["authorized", "failed"],
    "authorized": ["captured", "failed"],
    "captured": ["settled", "refunded"],
    "settled": ["refunded"],
    "failed": [],
    "refunded": []
}


def can_transition(current_status: str, new_status: str) -> bool:
    allowed_next_statuses = VALID_STATUS_TRANSITIONS.get(current_status, [])
    return new_status in allowed_next_statuses