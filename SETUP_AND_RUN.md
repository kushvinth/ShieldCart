# CapitalSense — Setup & Run Guide

## 🚀 Backend Setup & Commands (using `uv`)

### Initial Setup

```bash
# 1. Navigate to backend
cd /Users/MacbookPro/LocalStorage/Developer/Hacks/RUSS/backend

# 2. Create virtual environment with uv
uv venv .venv

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Sync dependencies using uv
uv sync

# Or install from requirements.txt
uv pip install -r requirements.txt
```

### Run Backend Server

```bash
# Option 1: Using python server.py
python server.py

# Option 2: Direct uvicorn command
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: With uv run
uv run python server.py

# Option 4: With uv run + uvicorn
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Useful Backend Commands

```bash
# Check dependencies are installed
uv pip list

# Install additional package
uv pip install <package-name>

# Run database migrations (Alembic)
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Add fraud detection models"

# Stop the server
# Press Ctrl+C in terminal

# View API docs
# Open browser to http://localhost:8000/docs
```

### Backend API Endpoints (Local)

```
- Health: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Claims: http://localhost:8000/api/v1/claims/submit
- Auth: http://localhost:8000/api/v1/auth/signup
```

---

## 📱 iOS App Setup & Commands (Flutter)

### Prerequisites

```bash
# Check if Flutter is installed
flutter --version

# If not installed, install Flutter
# Visit https://flutter.dev/docs/get-started/install/macos

# Check if Xcode is installed (required for iOS)
xcode-select --print-path

# If not, install Xcode Command Line Tools
xcode-select --install
```

### Initial iOS Setup

```bash
# 1. Navigate to Flutter app
cd /Users/MacbookPro/LocalStorage/Developer/Hacks/RUSS/frontend/capitalsense

# 2. Get dependencies
flutter pub get

# 3. Clean build (recommended first time)
flutter clean

# 4. Get dependencies again after clean
flutter pub get
```

### Run on iOS Simulator

```bash
# Option 1: Run on default iOS simulator (simplest)
cd /Users/MacbookPro/LocalStorage/Developer/Hacks/RUSS/frontend/capitalsense
flutter run

# Option 2: Run with verbose output (for debugging)
flutter run -v

# Option 3: Run on specific simulator
# First, list available simulators
flutter emulators

# Then run on specific simulator
flutter run -d <simulator-id>
```

### Run on Physical iOS Device

```bash
# 1. Connect iPhone via USB
# 2. Trust the device on your phone
# 3. Get list of connected devices
flutter devices

# 4. Get device ID (should show "ios")
# 5. Run on device
flutter run -d <device-id>

# Or run on any connected iOS device
flutter run -d all  # Run on all connected devices
```

### iOS-Specific Commands

```bash
# Open iOS project in Xcode
open ios/Runner.xcworkspace

# Build iOS app (debug)
flutter build ios

# Build iOS app (release)
flutter build ios --release

# Clean iOS build
flutter clean

# Update iOS pods
cd ios && pod update && cd ..

# Rebuild iOS pods
cd ios && pod install --repo-update && cd ..
```

### Connect iOS App to Backend

Edit `lib/service/` configuration files:

```dart
// example: lib/service/api_client.dart
String baseUrl = "http://localhost:8000";  // For simulator
// or
String baseUrl = "http://<your-mac-ip>:8000";  // For physical device
```

To find your Mac's IP (for physical device):

```bash
ipconfig getifaddr en0   # WiFi IP
# or
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Common iOS Issues & Fixes

```bash
# Pod version conflicts
cd ios && pod install --repo-update && cd ..

# Build cache issues
flutter clean && flutter pub get

# iOS deployment target mismatch
# Edit ios/Podfile and set minimum deployment target to 11.0+

# Simulator stuck/not launching
flutter emulators --launch <emulator-id>

# Check iOS build environment
flutter doctor -v
```

---

## 🔄 Full Development Workflow

### Terminal 1: Backend Server

```bash
cd /Users/MacbookPro/LocalStorage/Developer/Hacks/RUSS/backend
source .venv/bin/activate
python server.py
# Server runs on http://localhost:8000
```

### Terminal 2: iOS App Development

```bash
cd /Users/MacbookPro/LocalStorage/Developer/Hacks/RUSS/frontend/capitalsense
flutter run -v
# App runs on iOS simulator
# Hot reload: Press 'r'
# Hot restart: Press 'R'
# Quit: Press 'q'
```

---

## 🧪 Testing the Fraud Detection Feature

### 1. Start Backend
```bash
cd backend && python server.py
```

### 2. Test via API (using curl or Postman)

```bash
# Sign up
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Delivery",
    "business_name": "FastDeliver Co",
    "phone_number": "9876543210",
    "gst_number": "GST123456789"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'

# Submit claim (use token from login response)
curl -X POST http://localhost:8000/api/v1/claims/submit \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "claim_type": "weather_disruption",
    "claim_amount": 5000,
    "claimed_location": {
      "latitude": 28.6139,
      "longitude": 77.2090
    },
    "claimed_condition": "red_alert_weather",
    "fraud_signals": [
      {
        "signal_type": "gps_location",
        "raw_data": {"source": "phone_gps"},
        "gps_latitude": 28.6139,
        "gps_longitude": 77.2090,
        "gps_accuracy_meters": 45
      },
      {
        "signal_type": "device_motion",
        "raw_data": {
          "stay_still_probability": 0.15,
          "movement": "active"
        }
      },
      {
        "signal_type": "external_weather",
        "raw_data": {
          "alert_level": "red",
          "type": "thunderstorm"
        }
      }
    ]
  }'

# Get user's claims
curl -X GET http://localhost:8000/api/v1/claims/my-claims \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# Get user risk profile
curl -X GET http://localhost:8000/api/v1/claims/risk-profile \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# Get suspicious patterns
curl -X GET http://localhost:8000/api/v1/claims/suspicious-patterns \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## 📊 Monitoring & Debugging

### Backend Logs

```bash
# View logs in real-time
tail -f /tmp/capitalsense.log

# View errors only
grep ERROR /tmp/capitalsense.log

# Clear logs
rm /tmp/capitalsense.log
```

### Flutter Logs

```bash
# View Flutter device logs
flutter logs

# View logs with filtering
flutter logs | grep "fraud"
```

### Database Inspection

```bash
# If using SQLite
sqlite3 capitalsense.db

# SQL queries in SQLite CLI
SELECT * FROM claims;
SELECT * FROM fraud_signals;
SELECT * FROM user_risk_profiles;
```

---

## 🛑 Common Issues & Solutions

### Backend Won't Start

```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill process using port 8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### iOS Simulator Issues

```bash
# Simulator not launching
open -a Simulator

# Restart simulator
xcrun simctl shutdown all
xcrun simctl erase all

# List and launch specific simulator
flutter emulators --launch ios_device_name
```

### Dependencies Not Installing

```bash
# Clear Flutter pub cache
flutter pub cache repair

# Reinstall dependencies
flutter pub get --no-packages-dir

# For iOS
cd ios && rm -rf Pods Podfile.lock
pod install --repo-update
cd ..
```

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| Start backend | `python server.py` |
| Start iOS app | `flutter run` |
| Run with uv | `uv run python server.py` |
| Hot reload Flutter | Press `r` in terminal |
| Hot restart Flutter | Press `R` in terminal |
| View API docs | http://localhost:8000/docs |
| Quit Flutter app | Press `q` in terminal |
| Check device list | `flutter devices` |
| View Flutter logs | `flutter logs` |
| Clean everything | `flutter clean && flutter pub get` |
| Build iOS release | `flutter build ios --release` |

---

## 🔐 Environment Variables

### Backend (.env)

```bash
# Copy example
cp backend/.env.example backend/.env

# Edit and set:
DATABASE_URL=sqlite:///./capitalsense.db
APP_ENV=development
DEBUG=true
JWT_SECRET=your-secret-key
```

### iOS (lib/config)

```dart
// lib/service/api_config.dart
const String API_BASE_URL = "http://localhost:8000";
const String API_TIMEOUT_SECONDS = 30;
const bool ENABLE_LOGGING = true;
```

---

## 💡 Pro Tips

1. **Use hot reload** — Flutter hot reload is instant; save changes to see them immediately
2. **Check API docs** — Visit http://localhost:8000/docs for interactive endpoint testing
3. **Monitor network** — Use Xcode network debugger to see iOS app -> backend communication
4. **Parallel terminals** — Run backend in one terminal, iOS in another for best workflow
5. **Device IP** — For physical iPhone, connect via WiFi and use your Mac's local IP instead of localhost

---

**Happy coding! 🚀**
