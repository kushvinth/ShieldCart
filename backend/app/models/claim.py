import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, JSON, Enum, ForeignKey, Index, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class ClaimStatus(str, enum.Enum):
    pending = "pending"
    under_review = "under_review"
    approved_low_risk = "approved_low_risk"
    approved_medium_risk = "approved_medium_risk"
    needs_manual_review = "needs_manual_review"
    rejected_fraud = "rejected_fraud"
    paid = "paid"


class ClaimType(str, enum.Enum):
    weather_disruption = "weather_disruption"
    supply_chain_failure = "supply_chain_failure"
    accident_damage = "accident_damage"
    delivery_delay = "delivery_delay"
    other = "other"


class Claim(Base):
    """Parametric insurance claim with fraud detection metadata."""
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    claim_type: Mapped[ClaimType] = mapped_column(Enum(ClaimType), nullable=False)
    claim_amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Location-based trigger data
    claimed_location: Mapped[dict] = mapped_column(JSON, nullable=False)  # {"latitude": x, "longitude": y}
    claimed_condition: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g., "red_alert_weather"

    # Fraud detection scores (populated after analysis)
    fraud_risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-1, higher = more suspicious
    differentiation_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # confidence in real vs fake
    fairness_score: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-1, higher = more likely legit user
    synchronized_attack_flag: Mapped[bool] = mapped_column(Boolean, default=False)

    # Status
    status: Mapped[ClaimStatus] = mapped_column(
        Enum(ClaimStatus), default=ClaimStatus.pending, nullable=False
    )

    # Fraud analysis metadata
    fraud_analysis: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # detailed analysis results
    manual_review_required: Mapped[bool] = mapped_column(Boolean, default=False)
    manual_review_reason: Mapped[str | None] = mapped_column(String(512), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="claims")
    fraud_signals: Mapped[list["FraudSignal"]] = relationship(back_populates="claim", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_claims_user_id", "user_id"),
        Index("ix_claims_status", "status"),
        Index("ix_claims_fraud_risk_score", "fraud_risk_score"),
        Index("ix_claims_created_at", "created_at"),
    )
