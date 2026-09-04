"""Core biometric fraud-risk assessment logic."""

from dataclasses import dataclass
from enum import Enum
import math
from numbers import Integral


class Classification(str, Enum):
    """Risk classification for a biometric observation."""

    LOW_RISK = "LOW_RISK"
    REVIEW = "REVIEW"
    FRAUD = "FRAUD"


@dataclass(frozen=True)
class FraudAssessment:
    """Result of assessing a biometric observation."""

    risk_score: float
    is_fraud: bool
    classification: Classification


class InvalidObservationError(ValueError):
    """Raised when an observation contains invalid values."""


class BiometricFraudDetector:
    """Calculate a deterministic fraud risk score from biometric signals."""

    def __init__(self, fraud_threshold: float = 0.70) -> None:
        self._validate_probability(fraud_threshold, "fraud_threshold")
        self.fraud_threshold = fraud_threshold

    def assess(
        self,
        match_score: float,
        liveness_score: float,
        attempts: int,
        device_risk: float,
    ) -> FraudAssessment:
        """Assess observations and return their risk score and classification."""
        self._validate_probability(match_score, "match_score")
        self._validate_probability(liveness_score, "liveness_score")
        self._validate_attempts(attempts)
        self._validate_probability(device_risk, "device_risk")

        risk_score = (
            0.45 * (1 - match_score)
            + 0.35 * (1 - liveness_score)
            + 0.10 * min(attempts / 5, 1)
            + 0.10 * device_risk
        )
        risk_score = min(max(risk_score, 0.0), 1.0)

        if risk_score >= self.fraud_threshold:
            classification = Classification.FRAUD
        elif risk_score >= max(0.0, self.fraud_threshold - 0.20):
            classification = Classification.REVIEW
        else:
            classification = Classification.LOW_RISK

        return FraudAssessment(
            risk_score=risk_score,
            is_fraud=classification is Classification.FRAUD,
            classification=classification,
        )

    @staticmethod
    def _validate_probability(value: float, name: str) -> None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidObservationError(f"{name} must be a finite value in [0, 1]")
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise InvalidObservationError(f"{name} must be a finite value in [0, 1]")

    @staticmethod
    def _validate_attempts(attempts: int) -> None:
        if isinstance(attempts, bool) or not isinstance(attempts, Integral) or attempts < 0:
            raise InvalidObservationError("attempts must be a non-negative integer")
