from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum


class ClaimTypeEnum(str, Enum):
    weather_disruption = "weather_disruption"
    supply_chain_failure = "supply_chain_failure"
    accident_damage = "accident_damage"
    delivery_delay = "delivery_delay"
    other = "other"


class ClaimStatusEnum(str, Enum):
    pending = "pending"
    under_review = "under_review"
    approved_low_risk = "approved_low_risk"
    approved_medium_risk = "approved_medium_risk"
    needs_manual_review = "needs_manual_review"
    rejected_fraud = "rejected_fraud"
    paid = "paid"


class FraudSignalRequest(BaseModel):
    signal_type: str  # e.g., "gps_location", "device_motion", "network_data"
    raw_data: Dict[str, Any]
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy_meters: Optional[float] = None


class CreateClaimRequest(BaseModel):
    claim_type: ClaimTypeEnum
    claim_amount: float
    claimed_location: Dict[str, float]  # {"latitude": x, "longitude": y}
    claimed_condition: str  # e.g., "red_alert_weather"
    fraud_signals: List[FraudSignalRequest] = []


class FraudAnalysisResult(BaseModel):
    fraud_risk_score: float  # 0-1
    differentiation_score: float  # 0-1, confidence in real vs fake
    fairness_score: float  # 0-1, higher = more likely legit user
    synchronized_attack_flag: bool
    recommended_status: ClaimStatusEnum
    manual_review_required: bool
    manual_review_reason: Optional[str] = None
    analysis_details: Dict[str, Any]


class ClaimOut(BaseModel):
    id: str
    user_id: str
    claim_type: str
    claim_amount: float
    fraud_risk_score: Optional[float]
    differentiation_score: Optional[float]
    fairness_score: Optional[float]
    synchronized_attack_flag: bool
    status: str
    manual_review_required: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserRiskProfileOut(BaseModel):
    user_id: str
    claim_frequency_per_month: float
    average_claim_amount: float
    claim_approval_rate: float
    fraud_suspicion_count: int
    legit_verified_count: int
    false_positives_resolved: int
    appeals_accepted: int
    trust_score: float

    model_config = {"from_attributes": True}


class SuspiciousPatternOut(BaseModel):
    id: str
    pattern_type: str
    pattern_name: str
    user_count: int
    claim_count: int
    coordination_score: float
    detection_confidence: float
    total_fraudulent_payout: float
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
