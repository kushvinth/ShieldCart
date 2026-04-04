import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, JSON, Integer, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class UserRiskProfile(Base):
    """
    Risk profile for each user - tracks behavior patterns for anomaly detection.
    Builden incrementally as user submits claims.
    """
    __tablename__ = "user_risk_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Behavioral baseline metrics
    claim_frequency_per_month: Mapped[float] = mapped_column(Float, default=0.0)
    average_claim_amount: Mapped[float] = mapped_column(Float, default=0.0)
    claim_approval_rate: Mapped[float] = mapped_column(Float, default=1.0)  # 0-1

    # Location patterns
    primary_locations: Mapped[list] = mapped_column(JSON, default=[])  # [[lat, lon], ...]
    location_variance_km: Mapped[float] = mapped_column(Float, default=0.0)

    # Temporal patterns
    typical_claim_hours: Mapped[list] = mapped_column(JSON, default=[])  # [0-23]
    typical_days_of_week: Mapped[list] = mapped_column(JSON, default=[])  # [0-6]

    # Device fingerprint baseline
    primary_device_ids: Mapped[list] = mapped_column(JSON, default=[])
    device_variance_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Risk indicators
    fraud_suspicion_count: Mapped[int] = mapped_column(Integer, default=0)
    legit_verified_count: Mapped[int] = mapped_column(Integer, default=0)

    # Fairness metadata
    false_positives_resolved: Mapped[int] = mapped_column(Integer, default=0)
    appeals_accepted: Mapped[int] = mapped_column(Integer, default=0)

    # Overall trust score
    trust_score: Mapped[float] = mapped_column(Float, default=1.0)  # 0-1, higher = more trustworthy

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="risk_profile")

    __table_args__ = (
        Index("ix_user_risk_profiles_user_id", "user_id"),
        Index("ix_user_risk_profiles_trust_score", "trust_score"),
    )
