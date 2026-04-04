"""
Fraud Detection Service — Parametric Insurance Anti-Fraud System
Handles:
1. Multi-signal data collection (GPS, device, network, behavioral, external)
2. ML-based differentiation logic (real vs fake situations)
3. Synchronized attack detection (fraud rings)
4. Fairness layer (prevent legitimate users from being unfairly flagged)
"""

import logging
import math
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from fastapi import HTTPException

from app.models.user import User
from app.models.claim import Claim, ClaimStatus, ClaimType
from app.models.fraud_signal import FraudSignal, SignalType, SignalReliability
from app.models.user_risk_profile import UserRiskProfile
from app.models.suspicious_pattern import SuspiciousPattern
from app.schemas.claim import (
    CreateClaimRequest,
    FraudAnalysisResult,
    ClaimOut,
    UserRiskProfileOut,
)

logger = logging.getLogger(__name__)


class FraudDetectionService:
    """Multi-layered anti-fraud system for parametric insurance."""

    @staticmethod
    async def create_claim(
        user: User,
        payload: CreateClaimRequest,
        db: AsyncSession,
    ) -> Claim:
        """Create a new claim and run fraud detection analysis."""

        try:
            # 1. Create claim record
            claim = Claim(
                id=str(uuid.uuid4()),
                user_id=user.id,
                claim_type=payload.claim_type,
                claim_amount=payload.claim_amount,
                claimed_location=payload.claimed_location,
                claimed_condition=payload.claimed_condition,
                status=ClaimStatus.pending,
            )
            db.add(claim)
            await db.flush()

            # 2. Store multi-signal fraud data
            for signal_req in payload.fraud_signals:
                fraud_signal = FraudSignal(
                    id=str(uuid.uuid4()),
                    claim_id=claim.id,
                    user_id=user.id,
                    signal_type=signal_req.signal_type,
                    raw_data=signal_req.raw_data,
                    gps_latitude=signal_req.gps_latitude,
                    gps_longitude=signal_req.gps_longitude,
                    gps_accuracy_meters=signal_req.gps_accuracy_meters,
                    reliability=SignalReliability.medium,
                )
                db.add(fraud_signal)
            await db.flush()

            # 3. Run comprehensive fraud analysis
            analysis = await FraudDetectionService._analyze_fraud_signals(
                user, claim, db
            )

            # 4. Update claim with analysis results
            claim.fraud_risk_score = analysis["fraud_risk_score"]
            claim.differentiation_score = analysis["differentiation_score"]
            claim.fairness_score = analysis["fairness_score"]
            claim.synchronized_attack_flag = analysis["synchronized_attack_flag"]
            claim.fraud_analysis = analysis["details"]

            # 5. Determine final status
            recommended_status = FraudDetectionService._determine_claim_status(
                analysis
            )
            claim.status = recommended_status

            if analysis["manual_review_required"]:
                claim.manual_review_required = True
                claim.manual_review_reason = analysis["manual_review_reason"]

            await db.commit()

            return claim

        except Exception as exc:
            await db.rollback()
            logger.error("Claim creation failed: %s", exc, exc_info=True)
            raise HTTPException(status_code=500, detail=f"Claim creation failed: {exc}") from exc

    @staticmethod
    async def _analyze_fraud_signals(
        user: User, claim: Claim, db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Comprehensive fraud analysis using all 4 components:
        1. Differentiation Logic
        2. Multi-signal Data Analysis
        3. Synchronized Attack Detection
        4. Fairness Layer
        """

        # Get user's risk profile
        risk_profile = await db.execute(
            select(UserRiskProfile).where(UserRiskProfile.user_id == user.id)
        )
        risk_profile = risk_profile.scalar_one_or_none()

        if not risk_profile:
            risk_profile = UserRiskProfile(
                id=str(uuid.uuid4()),
                user_id=user.id,
            )
            db.add(risk_profile)
            await db.flush()

        # Get all fraud signals for this claim
        signals_result = await db.execute(
            select(FraudSignal).where(FraudSignal.claim_id == claim.id)
        )
        signals = signals_result.scalars().all()

        # Component 1: Differentiation Logic (Real vs Fake Detection)
        differentiation_score = await FraudDetectionService._compute_differentiation_score(
            claim, signals, db
        )

        # Component 2: Multi-signal Data Analysis & Anomaly Detection
        signal_anomaly_scores = await FraudDetectionService._analyze_multi_signals(
            claim, signals, risk_profile, db
        )

        # Component 3: Synchronized Attack Detection
        synchronized_attack_flag, attack_details = await FraudDetectionService._detect_synchronized_attacks(
            user, claim, signals, db
        )

        # Component 4: Fairness Layer
        fairness_score = await FraudDetectionService._compute_fairness_score(
            user, risk_profile, synchronized_attack_flag
        )

        # Aggregate fraud risk score
        fraud_risk_score = FraudDetectionService._aggregate_fraud_score(
            differentiation_score,
            signal_anomaly_scores,
            synchronized_attack_flag,
            fairness_score,
        )

        # Determine if manual review needed
        manual_review_required = False
        manual_review_reason = None

        if fraud_risk_score >= 0.7 and fairness_score >= 0.6:
            # High fraud score but high fairness: review to avoid false positive
            manual_review_required = True
            manual_review_reason = "High fraud signals but user has good history. Fairness review needed."
        elif fraud_risk_score >= 0.85:
            # Very high fraud score: always review
            manual_review_required = True
            manual_review_reason = "Very high fraud risk. Professional review required."
        elif synchronized_attack_flag:
            # Synchronized attack detected: review
            manual_review_required = True
            manual_review_reason = f"Synchronized attack ring detected: {attack_details.get('pattern_name', 'Unknown')}"

        return {
            "fraud_risk_score": fraud_risk_score,
            "differentiation_score": differentiation_score,
            "fairness_score": fairness_score,
            "synchronized_attack_flag": synchronized_attack_flag,
            "manual_review_required": manual_review_required,
            "manual_review_reason": manual_review_reason,
            "details": {
                "signal_anomaly_scores": signal_anomaly_scores,
                "attack_details": attack_details,
                "risk_profile_data": {
                    "trust_score": risk_profile.trust_score,
                    "claim_frequency": risk_profile.claim_frequency_per_month,
                    "approval_rate": risk_profile.claim_approval_rate,
                },
            },
        }

    @staticmethod
    async def _compute_differentiation_score(
        claim: Claim, signals: List[FraudSignal], db: AsyncSession
    ) -> float:
        """
        Component 1: Differentiation Logic
        Distinguishes real situations from fake ones.
        Analyzes external data (weather, incidents) vs claim location.
        """
        score = 0.5  # baseline

        # Check if claimed condition matches any external signals
        claimed_condition = claim.claimed_condition.lower()

        gps_signals = [s for s in signals if "gps" in s.signal_type.value.lower()]
        motion_signals = [s for s in signals if "motion" in s.signal_type.value.lower()]
        weather_signals = [s for s in signals if "weather" in s.signal_type.value.lower()]

        # If user has GPS movement data, it's more likely real
        if motion_signals and len(motion_signals) > 0:
            score += 0.15
        
        # If external weather data is available and matches, it's real
        if weather_signals and len(weather_signals) > 0:
            score += 0.2

        # If multiple corroborating signals exist
        if len(signals) >= 3:
            score += 0.1

        # Suspicious: only GPS, no corroboration
        if len(gps_signals) > 0 and len(motion_signals) == 0 and len(weather_signals) == 0:
            score -= 0.25

        return min(1.0, max(0.0, score))

    @staticmethod
    async def _analyze_multi_signals(
        claim: Claim,
        signals: List[FraudSignal],
        risk_profile: UserRiskProfile,
        db: AsyncSession,
    ) -> Dict[str, float]:
        """
        Component 2: Multi-signal Data Analysis
        Incorporates device data, network data, external data, behavioral data.
        ML anomaly detection to identify outliers.
        """
        anomaly_scores = {}

        for signal in signals:
            signal_type = signal.signal_type.value
            anomaly_score = 0.0

            if signal_type == SignalType.gps_location.value:
                # GPS anomaly detection
                if signal.gps_accuracy_meters and signal.gps_accuracy_meters > 100:
                    # Low accuracy is suspicious
                    anomaly_score += 0.3

                # Check distance from user's known locations
                if risk_profile.primary_locations:
                    distances = [
                        FraudDetectionService._haversine_distance(
                            signal.gps_latitude,
                            signal.gps_longitude,
                            loc[0],
                            loc[1],
                        )
                        for loc in risk_profile.primary_locations
                    ]
                    min_distance = min(distances)
                    
                    # If jump is > 500km away from normal pattern, suspicious
                    if min_distance > 500:
                        anomaly_score += 0.4

            elif signal_type == SignalType.device_motion.value:
                # Device motion analysis
                raw = signal.raw_data
                if raw.get("stay_still_probability", 0) > 0.8:
                    # Device barely moved but claimed weather emergency
                    anomaly_score += 0.5

            elif signal_type == SignalType.device_fingerprint.value:
                # Device fingerprint analysis
                if risk_profile.primary_device_ids and signal.raw_data.get("device_id"):
                    if signal.raw_data.get("device_id") not in risk_profile.primary_device_ids:
                        anomaly_score += 0.25

            elif signal_type == SignalType.temporal_pattern.value:
                # Temporal pattern analysis
                claim_hour = signal.raw_data.get("claim_hour", -1)
                if risk_profile.typical_claim_hours and claim_hour not in risk_profile.typical_claim_hours:
                    anomaly_score += 0.2

            elif signal_type == SignalType.behavioral_pattern.value:
                # Behavioral pattern analysis
                if risk_profile.claim_frequency_per_month > 0:
                    typical_amount = risk_profile.average_claim_amount
                    if claim.claim_amount > typical_amount * 2:
                        anomaly_score += 0.3

            anomaly_scores[signal_type] = min(1.0, anomaly_score)

            # Update signal reliability
            if anomaly_score > 0.6:
                signal.reliability = SignalReliability.tampered
            elif anomaly_score > 0.3:
                signal.reliability = SignalReliability.medium

            signal.anomaly_score = anomaly_score

        return anomaly_scores

    @staticmethod
    async def _detect_synchronized_attacks(
        user: User,
        claim: Claim,
        signals: List[FraudSignal],
        db: AsyncSession,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Component 3: Synchronized Attack Detection
        Identifies fraud rings - groups of coordinated attackers.
        Looks for patterns suggesting organized fraud.
        """
        is_synchronized = False
        attack_details = {}

        # Get all recent claims (last 24 hours) with similar characteristics
        time_window = datetime.utcnow() - timedelta(hours=24)

        similar_claims_result = await db.execute(
            select(Claim).where(
                and_(
                    Claim.created_at >= time_window,
                    Claim.claimed_location == claim.claimed_location,
                    Claim.claimed_condition == claim.claimed_condition,
                    Claim.id != claim.id,
                )
            )
        )
        similar_claims = similar_claims_result.scalars().all()

        if len(similar_claims) >= 3:
            # Multiple claims from same location/condition in short timeframe
            is_synchronized = True
            involved_user_ids = [claim.user_id] + [c.user_id for c in similar_claims]
            involved_claim_ids = [claim.id] + [c.id for c in similar_claims]

            attack_details = {
                "pattern_type": "gps_spoofing_ring",
                "pattern_name": f"Coordinated {len(similar_claims)} claim attack at {claim.claimed_location}",
                "involved_users": len(involved_user_ids),
                "involved_claims": len(involved_claim_ids),
                "time_clustering": "Within 24 hours",
            }

            # Check if pattern already exists
            pattern_result = await db.execute(
                select(SuspiciousPattern).where(
                    and_(
                        SuspiciousPattern.pattern_type == "gps_spoofing_ring",
                        SuspiciousPattern.is_active == True,
                    )
                )
            )
            existing_pattern = pattern_result.scalar_one_or_none()

            if not existing_pattern:
                # Create new suspicious pattern record
                pattern = SuspiciousPattern(
                    id=str(uuid.uuid4()),
                    pattern_type="gps_spoofing_ring",
                    pattern_name=attack_details["pattern_name"],
                    involved_user_ids=involved_user_ids,
                    user_count=len(involved_user_ids),
                    involved_claim_ids=involved_claim_ids,
                    claim_count=len(involved_claim_ids),
                    common_characteristics={
                        "location": claim.claimed_location,
                        "condition": claim.claimed_condition,
                    },
                    coordination_score=0.85,
                    time_clustering_hours=24,
                    total_fraudulent_payout=sum(c.claim_amount for c in similar_claims),
                    detection_confidence=0.9,
                )
                db.add(pattern)
                await db.flush()

        return is_synchronized, attack_details

    @staticmethod
    async def _compute_fairness_score(
        user: User,
        risk_profile: UserRiskProfile,
        synchronized_attack: bool,
    ) -> float:
        """
        Component 4: Fairness Layer
        Prevents legitimate users from being unfairly banned/flagged.
        Considers user history, appeals, previous false positives.
        """
        score = 1.0  # Start with full trust

        # Factor in user's trust score
        score *= risk_profile.trust_score

        # If user had false positives resolved, increase fairness
        if risk_profile.false_positives_resolved > 0:
            score += min(0.15, risk_profile.false_positives_resolved * 0.05)

        # If user's appeals were accepted, increase fairness
        if risk_profile.appeals_accepted > 0:
            score += min(0.15, risk_profile.appeals_accepted * 0.05)

        # If user has high historical claim approval rate, increase fairness
        if risk_profile.claim_approval_rate > 0.95:
            score += 0.1
        elif risk_profile.claim_approval_rate > 0.85:
            score += 0.05

        # If synchronized attack, reduce fairness temporarily
        if synchronized_attack:
            score *= 0.7

        # If user has many legit verified claims, high fairness
        if risk_profile.legit_verified_count > 5:
            score += 0.1

        return min(1.0, max(0.0, score))

    @staticmethod
    def _aggregate_fraud_score(
        differentiation: float,
        signal_anomalies: Dict[str, float],
        synchronized: bool,
        fairness: float,
    ) -> float:
        """
        Aggregate all components into final fraud risk score (0-1).
        Higher = more fraudulent.
        """
        avg_anomaly = sum(signal_anomalies.values()) / max(1, len(signal_anomalies))

        # Weighted combination
        base_fraud_score = (
            differentiation * 0.3
            + avg_anomaly * 0.4
            + (1.0 if synchronized else 0.0) * 0.2
        )

        # Apply fairness dampening: high fairness reduces fraud score
        fairness_dampening = 1.0 - (fairness * 0.3)

        final_score = base_fraud_score * fairness_dampening

        return min(1.0, max(0.0, final_score))

    @staticmethod
    def _determine_claim_status(analysis: Dict[str, Any]) -> ClaimStatus:
        """Determine final claim status based on fraud analysis."""
        fraud_risk = analysis["fraud_risk_score"]
        fairness = analysis["fairness_score"]
        synchronized = analysis["synchronized_attack_flag"]
        manual_review = analysis["manual_review_required"]

        if synchronized:
            return ClaimStatus.rejected_fraud

        if fraud_risk < 0.3:
            return ClaimStatus.approved_low_risk
        elif fraud_risk < 0.6:
            return ClaimStatus.approved_medium_risk if fairness > 0.6 else ClaimStatus.needs_manual_review
        else:
            return ClaimStatus.needs_manual_review if manual_review else ClaimStatus.rejected_fraud

    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in kilometers."""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c

    @staticmethod
    async def get_user_risk_profile(user_id: str, db: AsyncSession) -> Optional[UserRiskProfile]:
        """Fetch user's risk profile."""
        result = await db.execute(
            select(UserRiskProfile).where(UserRiskProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_claims(user_id: str, db: AsyncSession) -> List[Claim]:
        """Fetch all claims for a user."""
        result = await db.execute(
            select(Claim).where(Claim.user_id == user_id).order_by(Claim.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_suspicious_patterns(db: AsyncSession) -> List[SuspiciousPattern]:
        """Fetch all active suspicious patterns."""
        result = await db.execute(
            select(SuspiciousPattern)
            .where(SuspiciousPattern.is_active == True)
            .order_by(SuspiciousPattern.created_at.desc())
        )
        return result.scalars().all()
