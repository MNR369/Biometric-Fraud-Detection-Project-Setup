import math

import pytest

from biometric_fraud_detection import IncidentRequest, InvalidObservationError


def test_incident_request_accepts_valid_values() -> None:
    request = IncidentRequest(
        match_score=0.98,
        liveness_score=0.97,
        attempts=1,
        device_risk=0.05,
    )

    assert request.match_score == 0.98
    assert request.liveness_score == 0.97
    assert request.attempts == 1
    assert request.device_risk == 0.05


@pytest.mark.parametrize(
    "field, value",
    [
        ("match_score", -0.01),
        ("match_score", 1.01),
        ("match_score", math.inf),
        ("liveness_score", math.nan),
        ("device_risk", -1),
        ("device_risk", 2),
        ("attempts", -1),
        ("attempts", 1.5),
        ("attempts", True),
    ],
)
def test_incident_request_rejects_invalid_values(field: str, value: object) -> None:
    request_values: dict[str, object] = {
        "match_score": 1.0,
        "liveness_score": 1.0,
        "attempts": 0,
        "device_risk": 0.0,
    }
    request_values[field] = value

    with pytest.raises(InvalidObservationError):
        IncidentRequest(**request_values)


def test_incident_request_is_immutable() -> None:
    request = IncidentRequest(1.0, 1.0, 0, 0.0)

    with pytest.raises(AttributeError):
        request.attempts = 1
