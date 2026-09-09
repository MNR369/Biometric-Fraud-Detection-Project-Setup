import math

import pytest

from biometric_fraud_detection import (
    BiometricFraudDetector,
    Classification,
    InvalidObservationError,
)


def test_low_risk_assessment() -> None:
    assessment = BiometricFraudDetector().assess(1.0, 1.0, 0, 0.0)

    assert assessment.risk_score == 0.0
    assert assessment.is_fraud is False
    assert assessment.classification is Classification.LOW_RISK


def test_review_assessment() -> None:
    assessment = BiometricFraudDetector().assess(0.0, 0.85, 0, 0.0)

    assert assessment.risk_score == pytest.approx(0.5025)
    assert assessment.is_fraud is False
    assert assessment.classification is Classification.REVIEW


def test_fraud_assessment_at_threshold() -> None:
    assessment = BiometricFraudDetector().assess(0.0, 0.0, 5, 1.0)

    assert assessment.risk_score == 1.0
    assert assessment.is_fraud is True
    assert assessment.classification is Classification.FRAUD


def test_risk_formula_caps_attempt_signal() -> None:
    detector = BiometricFraudDetector(fraud_threshold=1.0)

    assessment = detector.assess(1.0, 1.0, 10, 0.0)

    assert assessment.risk_score == pytest.approx(0.10)
    assert assessment.classification is Classification.LOW_RISK


@pytest.mark.parametrize(
    "name, value",
    [
        ("match_score", -0.01),
        ("match_score", 1.01),
        ("match_score", math.inf),
        ("liveness_score", math.nan),
        ("device_risk", -1),
        ("device_risk", 2),
    ],
)
def test_probability_inputs_must_be_finite_and_bounded(name: str, value: float) -> None:
    observations = {
        "match_score": 1.0,
        "liveness_score": 1.0,
        "attempts": 0,
        "device_risk": 0.0,
    }
    observations[name] = value

    with pytest.raises(InvalidObservationError):
        BiometricFraudDetector().assess(**observations)


@pytest.mark.parametrize("attempts", [-1, 1.5, True, False])
def test_attempts_must_be_a_non_negative_integer(attempts: object) -> None:
    with pytest.raises(InvalidObservationError):
        BiometricFraudDetector().assess(1.0, 1.0, attempts, 0.0)


def test_custom_threshold_controls_classification() -> None:
    assessment = BiometricFraudDetector(fraud_threshold=0.50).assess(
        0.5, 0.7, 0, 0.0
    )

    assert assessment.risk_score == pytest.approx(0.33)
    assert assessment.classification is Classification.REVIEW


def test_threshold_must_be_finite_and_bounded() -> None:
    with pytest.raises(InvalidObservationError):
        BiometricFraudDetector(fraud_threshold=math.inf)
