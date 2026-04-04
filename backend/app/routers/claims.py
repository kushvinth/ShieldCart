"""
Claims Router — Parametric Insurance Fraud Detection Endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.claim import (
    CreateClaimRequest,
    ClaimOut,
    UserRiskProfileOut,
    SuspiciousPatternOut,
    FraudAnalysisResult,
)
from app.services.fraud_detection_service import FraudDetectionService

router = APIRouter(prefix="/claims", tags=["Claims & Fraud Detection"])


@router.post("/submit", response_model=ClaimOut)
async def submit_claim(
    payload: CreateClaimRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ClaimOut:
    """
    Submit a parametric insurance claim.
    Runs multi-signal fraud detection analysis automatically.
    """
    claim = await FraudDetectionService.create_claim(current_user, payload, db)
    return claim


@router.get("/my-claims", response_model=List[ClaimOut])
async def get_my_claims(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[ClaimOut]:
    """
    Get all claims submitted by current user.
    Includes fraud analysis results.
    """
    claims = await FraudDetectionService.get_user_claims(current_user.id, db)
    return claims


@router.get("/risk-profile", response_model=UserRiskProfileOut)
async def get_risk_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserRiskProfileOut:
    """
    Get current user's risk profile.
    Shows trust score, behavioral patterns, and fairness indicators.
    """
    profile = await FraudDetectionService.get_user_risk_profile(current_user.id, db)
    if not profile:
        raise Exception("Risk profile not found")
    return profile


@router.get("/suspicious-patterns", response_model=List[SuspiciousPatternOut])
async def get_suspicious_patterns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[SuspiciousPatternOut]:
    """
    Get all active suspicious attack patterns detected.
    Shows synchronized fraud rings (admin/analyst access).
    """
    patterns = await FraudDetectionService.get_suspicious_patterns(db)
    return patterns
