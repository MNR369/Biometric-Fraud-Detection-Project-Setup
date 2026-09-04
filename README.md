# Biometric Fraud Detection

A deterministic, dependency-free biometric fraud-risk baseline for Python 3.10 and newer.

## V1.0 behavior

`BiometricFraudDetector` accepts four observations:

- `match_score`: biometric match confidence in `[0, 1]`
- `liveness_score`: liveness confidence in `[0, 1]`
- `attempts`: a non-negative integer count
- `device_risk`: device risk in `[0, 1]`

The risk score is calculated as:

```text
0.45 * (1 - match_score)
+ 0.35 * (1 - liveness_score)
+ 0.10 * min(attempts / 5, 1)
+ 0.10 * device_risk
```

The score is clamped to `[0, 1]`. Scores at or above the fraud threshold are classified as `FRAUD`; scores at or above `max(0, threshold - 0.20)` are classified as `REVIEW`; all others are `LOW_RISK`. The default fraud threshold is `0.70`.

## Usage

```python
from biometric_fraud_detection import BiometricFraudDetector

assessment = BiometricFraudDetector().assess(
    match_score=0.98,
    liveness_score=0.97,
    attempts=1,
    device_risk=0.05,
)

print(assessment.classification)
```

Invalid observations raise `InvalidObservationError`.
