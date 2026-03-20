# 🛡️ ShieldCart 

<samp>AI-Powered Parametric Income Insurance for Q-Commerce Delivery Partners</samp>

> **Guidewire DEVTrails 2026** | University Hackathon  
> **Persona:** Grocery / Q-Commerce Delivery Partners (Zepto & Blinkit)  
> **Platform:** Web Application  
> **Stack:** React / Next.js · Node.js · Python (ML Services) · MySQL
> **Phase 1 Status:**  Complete — Submitted March 20, 2026

---

## Problem Statement

Q-Commerce delivery partners working with platforms like **Zepto** and **Blinkit** operate under brutal time pressure — delivering groceries in 10 minutes. But when external disruptions hit (a flash flood, an extreme heat wave, a local curfew), these workers lose their income instantly with zero safety net.

Unlike food delivery, Q-Commerce riders operate hyperlocally — often confined to a 2–3 km radius dark store zone. This makes them **disproportionately vulnerable** to hyper-local disruptions: a waterlogged lane, a market shutdown, or an AQI spike can shut down an entire dark store zone, wiping out a worker's entire day of earnings.

**ShieldCart** is a parametric income insurance platform built exclusively for this persona — providing automated, zero-claim, weekly-priced income protection triggered by real-world disruption events.

---

## Persona & Scenarios

### Who We're Protecting: The Q-Commerce Delivery Partner

| Attribute | Detail |
|---|---|
| Platform | Zepto / Blinkit |
| Work Pattern | 8–12 hour shifts, hyperlocal dark store zones |
| Weekly Earnings | ₹3,000 – ₹7,000 per week |
| Risk Profile | Highly exposed to hyperlocal weather & civic disruptions |
| Pain Point | No income protection, no sick leave, no buffer |

### Persona-Based Scenarios

**Scenario 1 — Flash Flood in Zone (Environmental)**  
Rahul delivers for Zepto in Andheri West, Mumbai. A sudden monsoon flood inundates his dark store zone. The platform marks his zone as inactive for 6 hours. Rahul loses ₹600 in income that shift. ShieldCart detects the rainfall threshold breach via weather API, auto-triggers a claim, and credits ₹480 (80% coverage) to his UPI within the hour — no forms, no calls.

**Scenario 2 — Extreme Heat Advisory (Environmental)**  
During a 47°C heat wave in Delhi, the government issues an outdoor work advisory. Deliveries in Priya's Blinkit zone drop by 70% for 2 days. ShieldCart's heat index trigger fires automatically. Priya receives a partial payout proportional to her lost hours, credited to her wallet.

**Scenario 3 — Local Curfew / Section 144 (Social)**  
A sudden curfew is imposed in a ward in Bengaluru following a local incident. Delivery operations halt for 8 hours. ShieldCart's civic disruption monitor (sourced from public advisories + traffic APIs) detects the zone lockdown and initiates automatic payouts to all active policyholders in the affected pin codes.

**Scenario 4 — Severe AQI Pollution Event (Environmental)**  
AQI in Gurugram crosses 400+ (Severe category). Platform delivery volumes collapse as customers and riders avoid outdoor activity. ShieldCart's pollution trigger fires for riders in the impacted grid, covering income loss for hours worked below their historical weekly average.

---

## Application Workflow

```
Worker Onboarding
      │
      ▼
[Risk Profiling via AI]  ←── Work zone, delivery history, pin code risk score
      │
      ▼
[Weekly Policy Creation]  ←── Dynamic premium calculated, policy activated
      │
      ▼
[Real-Time Disruption Monitoring]  ←── Weather API · AQI API · Traffic API · Civic Alerts
      │
   Trigger Fired?
   ┌──── YES ────┐
   │             │
   ▼             ▼
[Auto Claim   [No action,
 Initiated]    monitoring
   │            continues]
   ▼
[Fraud Detection Engine]  ←── GPS validation · Anomaly checks · Duplicate prevention
   │
   ▼
[Instant Payout]  ←── UPI / Wallet credit (Razorpay mock)
   │
   ▼
[Worker Dashboard Update]  ←── Payout history · Active coverage · Disruption log
```

---

## Weekly Premium Model

Q-Commerce workers are paid weekly by their platforms. Our insurance model mirrors this cycle exactly.

### Base Premium Formula

```
Weekly Premium = Base Rate × Zone Risk Multiplier × Coverage Tier Multiplier × Loyalty Discount
```

| Parameter | Description |
|---|---|
| **Base Rate** | ₹35/week (covers up to ₹1,500 income loss) |
| **Zone Risk Multiplier** | 0.8× (low-risk zone) to 1.4× (flood/heat-prone zone) |
| **Coverage Tier** | Basic (50%), Standard (70%), Premium (90%) of avg daily income |
| **Loyalty Discount** | –5% after 4 consecutive active weeks |

### Coverage Tiers

| Tier | Weekly Premium | Max Weekly Payout | Best For |
|---|---|---|---|
| Basic | ₹25–40 | ₹1,200 | New workers / trial |
| Standard | ₹45–70 | ₹2,500 | Regular full-time riders |
| Premium | ₹80–120 | ₹4,500 | High-earner / monsoon season |

> Premiums are dynamically recalculated **every Sunday night** for the upcoming week using the latest risk signals. Workers can opt in or out of renewal at any time.

### Why Weekly?
- Zepto/Blinkit pay out partner earnings weekly → insurance cost aligns with income cycle
- Workers can pause coverage during personal leave without losing their premium history
- Reduces default risk — no annual commitment required

---

## Parametric Triggers

These are objective, externally-verifiable thresholds. When crossed, claims are auto-initiated without any manual filing.

| Trigger ID | Event Type | Data Source | Threshold | Payout % |
|---|---|---|---|---|
| T1 | Heavy Rainfall | OpenWeatherMap API | > 50mm in 3 hours in pin code | 80% daily avg |
| T2 | Extreme Heat | OpenWeatherMap / IMD | Heat Index > 44°C for 4+ hours | 60% daily avg |
| T3 | Severe AQI | CPCB / AQI India API | AQI > 350 (Severe) for 6+ hours | 50% daily avg |
| T4 | Zone Curfew / Section 144 | Government advisory + traffic APIs | Verified zone lockdown | 90% daily avg |
| T5 | Platform Downtime | Blinkit/Zepto API mock | Platform inactive > 2 hours | 70% daily avg |

> All triggers are **parametric** — payouts are based purely on whether the threshold was crossed, not on whether the worker "filed" anything. This eliminates claims friction entirely.

---

## AI / ML Integration Plan

### 1. Dynamic Premium Calculation (Risk Scoring Model)
- **Algorithm:** Gradient Boosted Trees (XGBoost)
- **Features:** Worker's zone pin code, historical disruption frequency in that zone, season, platform (Zepto vs Blinkit), average weekly earnings declared at onboarding
- **Output:** A personalized weekly premium, updated every Sunday
- **Data Sources:** Historical weather (OpenWeatherMap), historical AQI (CPCB), historical disruption logs (mock)

### 2. Fraud Detection Engine
- **GPS Spoofing Detection:** Cross-validate worker's last GPS ping against the claimed disruption zone. If the worker was 15+ km away from the disrupted zone, flag the claim.
- **Anomaly Detection:** Compare claimed inactive hours against platform-reported delivery volume in that zone (via mock API). Unusual mismatch → human review queue.
- **Duplicate Claim Prevention:** Hash-based deduplication on (worker_id + trigger_id + date) to prevent the same event triggering multiple payouts.
- **Historical Pattern Analysis:** Isolation Forest model trained on synthetic claim data to flag statistical outliers in claim frequency.

### 3. Predictive Risk Alerts (Proactive UX)
- 48-hour weather forecast model alerts workers before a likely trigger event
- Workers see a "High disruption probability this week" badge in their dashboard
- Helps workers decide whether to upgrade their coverage tier before a risk event

---

## Tech Stack & Architecture

```
Frontend (React / Next.js)
├── Worker Dashboard (Tailwind CSS)
├── Onboarding Flow
├── Policy Management UI
├── Claims History & Payout Tracker
└── Admin / Insurer Dashboard

Backend (Node.js / Express)
├── Auth Service (JWT)
├── Policy Service
├── Trigger Monitoring Service (cron + WebSocket)
├── Claims Engine
└── Payout Service (Razorpay mock)

ML Services (Python / FastAPI)
├── Premium Calculation Model (XGBoost)
├── Fraud Detection Model (Isolation Forest)
└── Predictive Risk Alerts (Time-series forecast)

Database
├── MySQL (policies, claims, workers)
└── Redis (real-time trigger state, session cache)

External APIs (Mock/Free Tier)
├── OpenWeatherMap API (weather triggers)
├── AQI India / CPCB API (pollution triggers)
├── HERE Maps / Google Maps (zone validation)
└── Razorpay Sandbox (payout simulation)
```

---

## Development Plan

### Phase 1 (Weeks 1–2): Ideation & Foundation - COMPLETE
- [x] Define persona, scenarios, and parametric triggers
- [x] Design premium model and coverage tiers (3-tier weekly structure)
- [x] Plan AI/ML integration strategy (XGBoost + Isolation Forest)
- [x] Adversarial Defense & Anti-Spoofing Strategy documented
- [x] Set up GitHub repository and project structure
- [x] **Functional prototype built** — 4-screen interactive web app covering full onboarding → dashboard → payout → admin flow
- [x] Live AI risk scoring with animated ring chart and breakdown bars
- [x] Dynamic premium calculator with zone, season, and loyalty multipliers
- [x] Disruption simulation with auto-payout flow (< 4s settlement demo)
- [x] Fraud ring visualiser with corroboration score breakdown
- [x] 2-minute strategy video (link to be added)

### Phase 2 (Weeks 3–4): Automation & Protection - Upcoming
- [ ] Port prototype to production Next.js + Node.js architecture
- [ ] Backend API: policy lifecycle, claims engine, trigger monitor service
- [ ] Connect real OpenWeatherMap API (free tier) for T1 and T2 triggers
- [ ] Connect CPCB AQI API for T3 trigger
- [ ] 3–5 automated parametric trigger monitors with cron scheduling
- [ ] Zero-touch claim initiation pipeline
- [ ] Mock payout via Razorpay sandbox / UPI simulator
- [ ] Basic fraud detection: GPS validation + duplicate prevention

### Phase 3 (Weeks 5–6): Scale & Optimise - Upcoming
- [ ] Advanced ML fraud detection (Isolation Forest model, full corroboration scorer)
- [ ] Ring detection: temporal clustering + device fingerprint graph
- [ ] Intelligent dual dashboard (worker earnings view + insurer loss ratio analytics)
- [ ] Predictive 48h risk alert system
- [ ] Full end-to-end demo with simulated rainstorm trigger and automated payout walkthrough
- [ ] Final pitch deck (PDF) covering persona, AI architecture, and business viability

---

## Platform Justification: Why Web?

We chose a **Web Application** over a mobile app for the following reasons:

- **Accessibility:** Q-Commerce dark store supervisors and insurance admins need a desktop-capable view for the insurer dashboard and claims management
- **Faster iteration:** Next.js enables server-side rendering, API routes, and real-time updates without a separate backend for demo purposes
- **Demo-friendly:** Browser-based demos are easier to showcase in video walkthroughs and for judges to interact with
- **Progressive Web App (PWA):** The Next.js app will be made PWA-compatible so workers can add it to their phone home screen — bridging the web/mobile gap without maintaining two codebases

---

## Adversarial Defense & Anti-Spoofing Strategy

> **Context:** A coordinated syndicate of 500 delivery workers exploited a competing parametric platform by using GPS-spoofing apps to fake their location inside a red-alert weather zone while safely at home — draining the liquidity pool via mass false payouts. Simple GPS verification is no longer sufficient. Here is how ShieldCart is architected to be resilient against exactly this attack.

---

### 1. Differentiation: Genuine Stranded Worker vs. GPS Spoofer

ShieldCart does not trust GPS coordinates alone. Instead, every claim validation runs a **multi-signal corroboration check** — a spoofer can fake their GPS, but they cannot simultaneously fake all of the following:

| Signal | What a Real Worker Shows | What a Spoofer Shows |
|---|---|---|
| **Platform Activity Log** | Last delivery scan / order accepted within the disrupted zone (from Zepto/Blinkit mock API) | No platform activity — app idle or showing home zone history |
| **Device Sensor Fingerprint** | Accelerometer + gyroscope data showing movement consistent with being on a bike/scooter in rain | Stationary device motion profile (sitting at home) |
| **Network Cell Tower ID** | Connected to a cell tower geographically inside the disrupted pin code | Connected to a tower near their registered home address |
| **Battery & Charging State** | Unplugged, battery draining (active outdoor use) | Plugged in (typical home usage pattern) |
| **Historical Zone Presence** | GPS trace shows they regularly operate in this zone across past weeks | First time the device has ever been seen in this zone |
| **App Foreground State** | Delivery platform app is active/foreground | Delivery app backgrounded or not running |

A **Corroboration Score (0–100)** is computed from these signals using a weighted ensemble model. Claims scoring below 55 are automatically flagged; above 75 are auto-approved; between 55–75 enter a soft-review queue (see UX Balance below).

---

### 2. Data Points Used to Detect a Coordinated Fraud Ring

Individual GPS spoofing is hard to catch in isolation — but a **coordinated ring of 500 people is statistically impossible to hide**. ShieldCart's ring detection layer analyzes:

**Temporal Clustering**
- If 30+ claims are filed within the same 10-minute window from the same pin code, this is flagged as a surge anomaly. Genuine disruptions cause staggered claims; coordinated rings fire simultaneously.

**Device Fingerprint Graph**
- Each device is identified by a fingerprint combining OS version, screen resolution, installed app signatures, and Bluetooth MAC prefix. If multiple workers share suspicious device fingerprint similarities (e.g., same spoofing app installed — many GPS spoofers leave detectable artifacts in motion sensor data), they are clustered as a potential ring.

**Social / Referral Network Graph**
- Workers who onboarded via the same referral code, registered on the same day, or share the same emergency contact number are flagged as socially connected. A surge of connected workers all claiming simultaneously is a strong ring indicator.

**Home Address vs. Claimed Zone Distance**
- Cell tower and IP geolocation at claim time is compared against the worker's registered home address. If the inferred location is > 5 km from the disrupted zone, the claim is flagged regardless of GPS coordinates.

**Velocity Impossibility Check**
- If a worker's last confirmed delivery scan (from platform API) was in Zone A, and they are now claiming to be stranded in Zone B — and the transit time between zones is physically impossible given traffic conditions — the claim is automatically rejected.

**Cross-Platform AQI / Rainfall Validation**
- The actual sensor readings at the claimed pin code (from OpenWeatherMap / CPCB API) are validated against the threshold at the exact claim timestamp. If the disruption trigger was genuine, the weather data is unambiguous. Spoofers cannot fake the weather.

---

### 3. UX Balance: Handling Flagged Claims Without Penalizing Honest Workers

The biggest risk in aggressive fraud detection is **false positives** — an honest worker in a genuine rainstorm with a spotty network connection should not be denied their payout. ShieldCart uses a **tiered response model** rather than binary approve/reject:

**Tier 1 — Auto-Approved (Corroboration Score ≥ 75)**
- Payout processed immediately (< 60 seconds)
- No friction for the worker
- Covers the majority of genuine claims

**Tier 2 — Soft Flag / Pending (Score 55–74)**
- Worker receives an in-app notification: *"Your claim is being verified — you'll hear back within 2 hours."*
- A lightweight 1-tap self-verification is offered: worker can share a 5-second ambient video clip (rain/flood visible) or a single photo with auto-metadata
- If the supplementary signal resolves the score above 75, payout is released immediately
- If unresolved after 2 hours, payout is released at 50% as a **goodwill interim credit**, with the remaining 50% released after human review (within 24 hours)
- **Critically:** A soft flag does NOT appear on the worker's record or affect their future premium if the claim is later validated. No permanent stigma for network drops.

**Tier 3 — Hard Reject (Score < 55 + Ring Signals)**
- Claim is blocked and the case is escalated to the insurer's fraud queue
- Worker receives a transparent notification: *"We could not verify your location during this event. If you believe this is an error, please contact support with your delivery platform activity log."*
- Worker is given a 48-hour appeal window with a human reviewer
- **Repeat offenders** (3+ hard-rejected claims in 90 days) are suspended pending investigation — not silently blacklisted

**Network Drop Amnesty Rule**
Bad weather causes real network outages. If a worker's device loses connectivity during a disruption event, their **last known GPS ping (up to 30 minutes prior)** is used for zone validation, not the moment of claim. This prevents honest workers from being penalized simply because the storm killed their signal at the worst possible moment.

---

## Phase 1 Prototype

A fully functional browser-based prototype has been built and delivered as part of the Phase 1 submission. It demonstrates the core end-to-end flow with real interactive state — all fields are editable, premiums calculate dynamically, and disruption simulations fire live payouts.

**Prototype file:** `docs/shieldcart-prototype.html` (open in any browser, no server needed)

### What the Prototype Demonstrates

**Screen 1 — Overview / Landing**
- Live trigger monitor showing all 5 parametric triggers (T1–T5) with real-time status badges
- Hero stats and platform overview
- Entry points to onboarding and admin views

**Screen 2 — Worker Onboarding (3 fully interactive steps)**

| Step | What Works |
|---|---|
| Step 1: Basic Details | All 6 fields are free-text / dropdown editable. Validation prevents empty submission. |
| Step 2: Risk Profiling | AI risk score ring updates live as you type. Zone type, season, tenure, and earnings all feed the scoring formula. Risk breakdown bars animate in real time. |
| Step 3: Choose Plan | Tier prices recalculate from your actual inputs. Clicking a tier selects it and updates the final premium with full breakdown shown. |
| Activation | Creates a real in-memory policy and unlocks the Worker Dashboard. |

**Screen 3 — Worker Dashboard (fully live)**
- Policy strip reflects everything entered during onboarding
- **"Simulate Disruption" button** — choose any of the 5 triggers, fires a claim that appears as "Processing" in the timeline and payout table, then auto-settles to "Paid" after 4 seconds with a UPI payout toast notification
- Edit My Details modal — update name, UPI, zone; changes reflect everywhere instantly
- Disruption timeline, payout history table, 48h risk forecast, and quick actions all functional
- Cancel Policy resets the entire app state

**Screen 4 — Insurer / Admin Dashboard**
- Portfolio stats update in real time as policies are created and claims fired during the session
- Fraud queue shows hard-rejected claims with corroboration score breakdown and ring detection signals
- Ring visualizer animates a pulsing fraud cluster vs. legitimate verified dots
- Claims log shows all auto-paid, soft-flagged, and rejected claims — Approve and Confirm-Reject buttons are live
- "Simulate Trigger" button shortcuts to the disruption flow

### Premium Calculation Logic (Live in Prototype)

```
Base Premium    = (Weekly Earnings ÷ 7) × 6% × 7 days

Tier Multiplier:
  Basic    → 0.72×  |  Standard → 1.00×  |  Premium → 1.60×

Zone Multiplier:
  Flood-prone → 1.30×  |  Extreme heat → 1.20×
  Industrial  → 1.10×  |  Low-risk     → 0.85×

Season Multiplier:
  Monsoon → 1.15×  |  Summer → 1.10×  |  Winter → 0.90×  |  Normal → 1.00×

Loyalty Discount:
  Tenure > 12 months → 0.95×  |  Tenure > 6 months → 0.97×

Final Premium = Base × Tier Multiplier × Zone Multiplier × Season Multiplier × Loyalty Discount
```

---

## Coverage Exclusions (As per Problem Statement)

ShieldCart **strictly excludes** the following:
-  Health or medical insurance
-  Life insurance
-  Accident coverage
-  Vehicle damage or repair costs
-  Personal liability

ShieldCart **covers only**:
-  Loss of income due to verifiable external disruptions (weather, AQI, civic events, platform downtime)

---

## Repository Structure

```
shieldcart/
├── README.md                        # This document
├── docs/
│   ├── shieldcart-prototype.html    # ✅ Phase 1 functional prototype (browser-ready)
│   └── architecture/                # Diagrams (Phase 2)
├── frontend/                        # Next.js web application (Phase 2+)
│   ├── pages/
│   │   ├── index.tsx                # Landing / overview
│   │   ├── onboarding/              # 3-step worker registration
│   │   ├── dashboard/               # Worker dashboard
│   │   └── admin/                   # Insurer admin view
│   ├── components/
│   │   ├── TriggerMonitor/          # Live parametric trigger display
│   │   ├── RiskScoring/             # AI premium calculator UI
│   │   ├── ClaimsTimeline/          # Payout history & status
│   │   └── FraudRingMap/            # Ring detection visualiser
│   └── styles/
├── backend/                         # Node.js / Express API (Phase 2+)
│   ├── services/
│   │   ├── trigger.service.ts       # Parametric trigger monitor
│   │   ├── claims.service.ts        # Auto-claim initiation
│   │   ├── payout.service.ts        # Razorpay mock integration
│   │   └── policy.service.ts        # Weekly policy lifecycle
│   ├── routes/
│   └── models/
├── ml/                              # Python FastAPI ML services (Phase 2+)
│   ├── premium_model/               # XGBoost risk scoring
│   ├── fraud_detection/             # Isolation Forest + corroboration scorer
│   └── risk_alerts/                 # 48h disruption forecast
├── mock-apis/                       # Simulated external API responses
│   ├── openweathermap.mock.json
│   ├── cpcb-aqi.mock.json
│   └── zepto-platform.mock.json
└── tests/
```

---

## Team

> Kushvinth Madhavan - Team Lead <br>
Akshat Sharma <br>
Anirudh <br>
Aadithiyaa S

---
