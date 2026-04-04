# CapitalSense - Parametric Insurance Platform

**Secure. Intelligent. Fair.**

## Overview

CapitalSense is a parametric insurance platform for small businesses and delivery workers. It automatically triggers insurance payouts when predefined conditions are met, eliminating manual claims processing.

### Key Challenge

A sophisticated fraud ring of 500+ delivery workers successfully exploited beta platforms by spoofing GPS locations to fake weather emergencies, draining liquidity pools. Your platform requires **enterprise-grade fraud detection**.

---

## 🛡️ Anti-Fraud System Architecture

### 4-Component Fraud Detection Framework

#### 1. **Differentiation Logic** (Real vs. Fake Detection)
- Validates if claimed situations are genuinely real
- Cross-references external data (weather APIs, incident reports)
- Analyzes signal corroboration (GPS + motion + weather data)
- Returns confidence score (0-1) on claim authenticity

#### 2. **Multi-Signal Data System** (Beyond GPS)
Incorporates:
- **GPS Location Data** — Accuracy, consistency, velocity analysis
- **Device Motion Data** — Accelerometer, gyroscope to detect if device is actually moving
- **Network Data** — IP geolocation, device fingerprinting, connection patterns
- **Behavioral Data** — Claim history, temporal patterns, typical claim hours
- **External Data** — Real-time weather, incident reports, traffic data

ML-based anomaly detection flags outliers across all signals.

#### 3. **Synchronized Attack Detection** (Fraud Rings)
Identifies coordinated fraud campaigns:
- Clusters claims with identical/similar characteristics (location, condition, time)
- Detects when 3+ users claim from same location within 24 hours
- Tracks suspicious patterns and flagged attack rings
- Coordination score indicates likelihood of organized fraud

#### 4. **Fairness Layer** (Prevent False Positives)
Protects legitimate users from being unfairly flagged:
- User trust score based on historical claim approval rate
- False positive tracking — users with previous false flags get protection
- Appeal mechanisms — accepted appeals increase fairness score
- Temporal fairness — high-risk scores balanced against user reputation
- Result: Legit users won't get permanently banned for appearing "sus"

---

## 📊 Database Schema

### New Models for Fraud Detection

#### `Claim` — Insurance Claim Record
```
- claim_type: weather_disruption, supply_chain_failure, accident_damage, etc.
- claim_amount: Insurance payout amount
- claimed_location: GPS coordinates of reported incident
- claimed_condition: "red_alert_weather", etc.
- fraud_risk_score: 0-1 (higher = more fraudulent)
- differentiation_score: Confidence in real vs. fake
- fairness_score: User trustworthiness
- synchronized_attack_flag: Part of fraud ring?
- status: pending, under_review, approved_low_risk, approved_medium_risk, needs_manual_review, rejected_fraud, paid
```

#### `FraudSignal` — Multi-Signal Data Collection
```
- signal_type: gps_location, device_motion, network_data, behavioral_pattern, external_weather, device_fingerprint, temporal_pattern
- raw_data: JSON flexible data for each signal type
- gps_latitude/longitude: GPS coordinates
- gps_accuracy_meters: Position accuracy
- reliability: high, medium, low, tampered
- anomaly_score: ML-computed outlier detection (0-1)
- tampering_indicators: Suspicious patterns detected
```

#### `UserRiskProfile` — Behavioral Baseline
```
- claim_frequency_per_month: Baseline claim rate
- average_claim_amount: Typical claim size
- claim_approval_rate: Historical approval %
- primary_locations: Known user locations
- location_variance_km: Geographic pattern spread
- typical_claim_hours: User's typical claim times
- primary_device_ids: Known devices used
- fraud_suspicion_count: Times flagged
- legit_verified_count: Verified legitimate claims
- false_positives_resolved: Wrong flags that were corrected
- appeals_accepted: Successful appeals
- trust_score: Overall user trustworthiness (0-1)
```

#### `SuspiciousPattern` — Attack Ring Tracking
```
- pattern_type: gps_spoofing_ring, device_cluster_attacks, etc.
- pattern_name: Human-readable ring description
- involved_user_ids: [user_id1, user_id2, ...]
- involved_claim_ids: [claim_id1, claim_id2, ...]
- common_characteristics: Shared suspicious traits
- coordination_score: Likelihood of organized attack (0-1)
- total_fraudulent_payout: Estimated fraud loss
- detection_confidence: How sure we are (0-1)
- is_active: Currently investigating?
```

---

## 🔌 API Endpoints

### Claims & Fraud Detection

#### Submit Claim with Fraud Analysis
```
POST /api/v1/claims/submit

Request:
{
  "claim_type": "weather_disruption",
  "claim_amount": 5000,
  "claimed_location": {"latitude": 28.6139, "longitude": 77.2090},
  "claimed_condition": "red_alert_weather",
  "fraud_signals": [
    {
      "signal_type": "gps_location",
      "raw_data": {...},
      "gps_latitude": 28.6139,
      "gps_longitude": 77.2090,
      "gps_accuracy_meters": 45
    },
    {
      "signal_type": "device_motion",
      "raw_data": {"stay_still_probability": 0.1, "movement": "active"}
    },
    {
      "signal_type": "external_weather",
      "raw_data": {"alert_level": "red", "type": "thunderstorm"}
    }
  ]
}

Response:
{
  "id": "claim-uuid",
  "user_id": "user-uuid",
  "claim_type": "weather_disruption",
  "claim_amount": 5000,
  "fraud_risk_score": 0.15,
  "differentiation_score": 0.85,
  "fairness_score": 0.92,
  "synchronized_attack_flag": false,
  "status": "approved_low_risk",
  "manual_review_required": false,
  "created_at": "2026-04-04T15:30:00Z"
}
```

#### Get User's Claims
```
GET /api/v1/claims/my-claims

Response: [Claim, Claim, ...]
```

#### Get User Risk Profile
```
GET /api/v1/claims/risk-profile

Response:
{
  "user_id": "user-uuid",
  "claim_frequency_per_month": 2.5,
  "average_claim_amount": 3500,
  "claim_approval_rate": 0.98,
  "fraud_suspicion_count": 0,
  "legit_verified_count": 25,
  "false_positives_resolved": 1,
  "appeals_accepted": 0,
  "trust_score": 0.95
}
```

#### Get Suspicious Patterns (Admin)
```
GET /api/v1/claims/suspicious-patterns

Response: [SuspiciousPattern, SuspiciousPattern, ...]
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL or SQLite
- Virtual environment

### Installation

```bash
cd backend
source .venv/bin/activate  # or use your venv activation
pip install -r requirements.txt
```

### Setup Database

```bash
# Auto-create tables in development
python server.py

# Or use Alembic migrations for production
alembic upgrade head
```

### Run Server

```bash
python server.py
# Server runs on http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 🔐 Fraud Detection Scoring

### Fraud Risk Score (0-1)
**Formula:**
```
final_score = base_fraud_score × fairness_dampening

where:
  base_fraud_score = (differentiation × 0.3) + (avg_anomaly × 0.4) + (synchronized × 0.2)
  fairness_dampening = 1.0 - (fairness_score × 0.3)
```

### Claim Status Decision Tree

```
if synchronized_attack_flag:
  → REJECTED_FRAUD (automatic denyg)
  
else if fraud_risk < 0.3:
  → APPROVED_LOW_RISK (auto-payout)
  
else if 0.3 ≤ fraud_risk < 0.6:
  → APPROVED_MEDIUM_RISK (if fairness > 0.6)
  → NEEDS_MANUAL_REVIEW (if fairness ≤ 0.6)
  
else if fraud_risk ≥ 0.6 AND fairness > 0.6:
  → NEEDS_MANUAL_REVIEW (fairness check — avoid false positive)
  
else if fraud_risk ≥ 0.85:
  → NEEDS_MANUAL_REVIEW (high fraud signals)
  
else:
  → REJECTED_FRAUD
```

---

## 📈 Key Metrics

| Metric | Purpose |
|--------|---------|
| **Differentiation Score** | Confidence claim is real (not spoofed) |
| **Anomaly Scores** | Individual signal trustworthiness |
| **Fairness Score** | User history protection factor |
| **Coordination Score** | Organized fraud likelihood |
| **Trust Score** | User's long-term reputation |

---

## 🎯 Feature Highlights

✅ **Beyond GPS** — 7 signal types prevent location spoofing  
✅ **ML Anomaly Detection** — Identifies outliers across device, network, behavioral data  
✅ **Fraud Ring Detection** — Catches coordinated 500-person attacks  
✅ **Fair to Good Users** — High-reputation users protected from false bans  
✅ **Auto Payout** — Low-risk claims approved & paid instantly  
✅ **Manual Review** — High-risk claims flagged for human review  
✅ **Audit Trail** — Full fraud analysis stored for each claim  

---

## 📝 Example Scenarios

### Scenario 1: Legitimate Weather Claim (Approved)
```
User in Mumbai claims red-alert weather disruption
- GPS: Valid location, accuracy ±50m ✓
- Motion: Device actively moving ✓
- Weather API: Red alert confirmed at location ✓
- User history: 98% approval rate, 0 suspicions ✓

Result: fraud_risk_score = 0.12 → APPROVED_LOW_RISK → Auto-payout
```

### Scenario 2: GPS Spoof Attempt (Rejected)
```
User claims red-alert weather but:
- GPS: Accuracy ±200m (high uncertainty) ⚠️
- Motion: Device stationary for 8 hours ✗
- Weather API: No alert at claimed location ✗
- Pattern: 5 identical claims from same location in 6 hours ✗

Result: fraud_risk_score = 0.89, synchronized_attack_flag = true → REJECTED_FRAUD
```

### Scenario 3: Trustworthy User, Slight Anomaly (Manual Review)
```
User with 95% approval rate claims supply chain failure:
- GPS: Slightly outside normal range (+300km) ⚠️
- Motion: Normal pattern ✓
- User history: 50+ verified legitimate claims ✓
- Fairness score: 0.92 (high trust) ✓

Result: fraud_risk_score = 0.65, fairness_score = 0.92 → NEEDS_MANUAL_REVIEW (fairness protection)
```

---

## 🔧 Configuration

### Fraud Thresholds (Adjustable)

In `fraud_detection_service.py`:
```python
# Adjust these based on business risk appetite
FRAUD_THRESHOLD_APPROVE_LOW = 0.3
FRAUD_THRESHOLD_MEDIUM = 0.6
FRAUD_THRESHOLD_REVIEW = 0.7
FRAUD_THRESHOLD_REJECT = 0.85

# Fairness dampening factor
FAIRNESS_DAMPENING = 0.3  # Higher = more lenient to good users
```

---

## 📚 Architecture Diagram

```
Claim Submission
    ↓
Multi-Signal Collector (7 signal types)
    ↓
┌─────────────────────────────────────────┐
│   4-Component Fraud Analysis            │
├─────────────────────────────────────────┤
│ 1. Differentiation Logic                │→ Real vs. Fake score
│ 2. Multi-Signal Anomaly Detection       │→ Individual signal scores
│ 3. Synchronized Attack Detection        │→ Fraud ring flag
│ 4. Fairness Layer                       │→ User protection factor
└─────────────────────────────────────────┘
    ↓
Score Aggregation & Status Decision
    ↓
├─ Low Risk → APPROVED_LOW_RISK (auto-payout)
├─ Medium Risk → APPROVED_MEDIUM_RISK or MANUAL_REVIEW
├─ High Risk → NEEDS_MANUAL_REVIEW or REJECTED_FRAUD
└─ Synchronized Attack → REJECTED_FRAUD
    ↓
Database Storage + Audit Trail
    ↓
UI/Admin Dashboard
```

---

## 🚨 Production Considerations

1. **Rate Limiting** — Prevent abuse via rapid claim submissions
2. **Geographic IP Validation** — Cross-check GPS with reported IP
3. **Device Fingerprinting** — Track unique device characteristics
4. **Real-Time Weather APIs** — Integrate OpenWeather or similar
5. **ML Model Updates** — Retrain anomaly detection weekly
6. **Appeals Workflow** — Human review of rejected claims
7. **Liquidity Monitoring** — Alert on unusual payout patterns
8. **Regulatory Compliance** — Document all fraud decisions

---

## 📞 Support

For questions about fraud detection logic or integrations, refer to:
- Service: `app/services/fraud_detection_service.py`
- Models: `app/models/{claim, fraud_signal, user_risk_profile, suspicious_pattern}.py`
- Routes: `app/routers/claims.py`
- Schemas: `app/schemas/claim.py`

---

**Built with ❤️ for trustworthy parametric insurance.**
