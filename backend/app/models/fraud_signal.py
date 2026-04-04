import uuid
from datetime import datetime
from sqlalchemy import String, Float, DateTime, JSON, Enum, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class SignalType(str, enum.Enum):
    gps_location = "gps_location"
    device_motion = "device_motion"
    network_data = "network_data"
    behavioral_pattern = "behavioral_pattern"
    external_weather = "external_weather"
    device_fingerprint = "device_fingerprint"
    temporal_pattern = "temporal_pattern"


class SignalReliability(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"
    tampered = "tampered"


class FraudSignal(Base):
    """
    Multi-signal data collection for fraud detection.
    Stores GPS, device, network, behavioral, and external data.
    """
    __tablename__ = "fraud_signals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id: Mapped[str] = mapped_column(String(36), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    signal_type: Mapped[SignalType] = mapped_column(Enum(SignalType), nullable=False)

    # Raw signal data (flexible JSON to accommodate various types)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    # For GPS signals specifically
    gps_latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_accuracy_meters: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Signal reliability and suspicion indicators
    reliability: Mapped[SignalReliability] = mapped_column(
        Enum(SignalReliability), default=SignalReliability.medium, nullable=False
    )
    anomaly_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1, ML-computed
    tampering_indicators: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    claim: Mapped["Claim"] = relationship(back_populates="fraud_signals")
    user: Mapped["User"] = relationship(back_populates="fraud_signals")

    __table_args__ = (
        Index("ix_fraud_signals_claim_id", "claim_id"),
        Index("ix_fraud_signals_user_id", "user_id"),
        Index("ix_fraud_signals_type", "signal_type"),
        Index("ix_fraud_signals_created_at", "created_at"),
    )
