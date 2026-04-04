import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, JSON, Integer, ForeignKey, Index, func, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class SuspiciousPattern(Base):
    """
    Detects and tracks suspicious attack patterns - especially coordinated fraud rings.
    Identifies when multiple users exhibit synchronized suspicious behavior.
    """
    __tablename__ = "suspicious_patterns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Characteristics of the suspicious pattern
    pattern_type: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g., "gps_spoofing_ring", "device_cluster_attacks"
    pattern_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # User IDs involved in this pattern
    involved_user_ids: Mapped[list] = mapped_column(JSON, nullable=False)  # [user_id1, user_id2, ...]
    user_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Claim IDs involved in this pattern
    involved_claim_ids: Mapped[list] = mapped_column(JSON, nullable=False)  # [claim_id1, claim_id2, ...]
    claim_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Common characteristics across the ring
    common_characteristics: Mapped[dict] = mapped_column(JSON, nullable=False)  # e.g., {"location": "...", "device_ids": [...], "claimed_condition": "..."}

    # Coordination indicators
    coordination_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1, how likely they're coordinating
    time_clustering_hours: Mapped[int] = mapped_column(Integer, default=0)  # Claims within X hours of each other
    
    # Attack characteristics
    total_fraudulent_payout: Mapped[float] = mapped_column(Float, default=0.0)
    detection_confidence: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1

    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_suspicious_patterns_created_at", "created_at"),
        Index("ix_suspicious_patterns_pattern_type", "pattern_type"),
        Index("ix_suspicious_patterns_is_active", "is_active"),
    )
