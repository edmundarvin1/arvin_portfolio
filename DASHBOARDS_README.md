# Portfolio Dashboards

Two interactive dashboards: Trading P&L and Gym Analytics

## 🏗️ Architecture

### Frontend-Backend Separation

```
arvin_portfolio/
├── projects/                    # FRONTEND (Design work here)
│   ├── trading-pnl/
│   │   ├── index.html          # Dashboard HTML
│   │   ├── script.js           # Fetches from API, updates UI
│   │   └── styles.css          # Dashboard styling
│   │
│   └── gym-analytics/
│       ├── index.html
│       ├── script.js
│       └── styles.css
│
└── backend/                     # BACKEND (Data logic here)
    ├── app.py                   # Flask server
    ├── requirements.txt         # Python dependencies
    ├── .env.example             # Environment variables template
    └── api/
        ├── trading.py           # Trading API endpoints
        └── gym.py               # Gym data endpoints
```

**KEY PRINCIPLE**: Frontend and backend are completely separate.
- **Frontend** calls API endpoints and displays data
- **Backend** fetches from external sources and serves JSON

## 🎨 Working on Design (Frontend Only)

If you're working on the design, you **ONLY** need to touch:
- `projects/trading-pnl/*.html, *.css`
- `projects/gym-analytics/*.html, *.css`

### Frontend Files

**HTML**: Dashboard structure
**CSS**: Styling (keep minimal, match main site aesthetic)
**script.js**:
- Fetches data from `/api/...` endpoints
- Updates DOM with data
- **DO NOT MODIFY** the `fetch()` calls or API structure

### Testing Design Changes

1. **With mock data** (no backend needed):
```javascript
// In script.js, comment out the API call and use mock data:
async function fetchTradingData() {
    // Temporarily return mock data for design work
    return {
        summary: { totalPnL: 12543.67, winRate: 67.5, ... },
        chartData: { dates: [...], cumulativePnL: [...] },
        recentTrades: [...]
    };
}
```

2. **View in browser**:
```bash
# From project root
python server.py
# Visit: http://localhost:8080/projects/trading-pnl/
```

## 💻 Working on Backend (Data Logic)

If you're implementing data fetching, you **ONLY** need to touch:
- `backend/app.py`
- `backend/api/trading.py`
- `backend/api/gym.py`

### Backend Setup

1. **Install dependencies**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. **Run backend server**:
```bash
python app.py
# Runs on http://localhost:5000
```

### API Endpoints

#### Trading Dashboard
**GET** `/api/trading/summary`

Response format:
```json
{
  "summary": {
    "totalPnL": float,
    "winRate": float,
    "totalTrades": int,
    "sharpeRatio": float
  },
  "chartData": {
    "dates": [str],
    "cumulativePnL": [float]
  },
  "recentTrades": [
    {
      "date": "YYYY-MM-DD",
      "pair": str,
      "type": "LONG|SHORT",
      "pnl": float
    }
  ]
}
```

#### Gym Analytics
**GET** `/api/gym/summary`

Response format:
```json
{
  "summary": {
    "totalWorkouts": int,
    "totalVolume": int,
    "currentStreak": int,
    "prsThisMonth": int
  },
  "volumeData": {
    "dates": [str],
    "volumes": [int]
  },
  "exerciseProgress": {
    "dates": [str],
    "exercises": [
      {
        "name": str,
        "weights": [float]
      }
    ]
  },
  "personalRecords": [
    {
      "exercise": str,
      "weight": float,
      "reps": int,
      "date": "YYYY-MM-DD"
    }
  ]
}
```

### Implementing Real Data Sources

**Trading API** (`backend/api/trading.py`):
1. Uncomment `import requests`
2. Add your trading API credentials to `.env`
3. Replace mock data with actual API calls
4. Process and format the response

**Google Sheets** (`backend/api/gym.py`):
1. Uncomment Google API imports in `requirements.txt`
2. Follow [Google Sheets API setup](https://developers.google.com/sheets/api/quickstart/python)
3. Download credentials JSON and add path to `.env`
4. Implement `get_google_sheets_data()` function
5. Process spreadsheet data into expected format

## 🚀 Full Stack Development

Running both frontend and backend together:

1. **Terminal 1** (Backend):
```bash
cd backend
source venv/bin/activate
python app.py
# Backend runs on :5000
```

2. **Terminal 2** (Frontend):
```bash
# From project root
python server.py
# Frontend serves on :8080
```

3. **Update frontend API URL**:
```javascript
// In both script.js files, update:
const API_BASE_URL = 'http://localhost:5000/api';
```

Now visit:
- Trading: http://localhost:8080/projects/trading-pnl/
- Gym: http://localhost:8080/projects/gym-analytics/

## 📦 Deployment

### Frontend Only (Current Setup)
Already deployed with your portfolio on GCP VM. Just copy the `projects/` folder.

### Adding Backend to GCP VM

1. **SSH to VM**:
```bash
gcloud compute ssh instance-20250301-143625 --zone=europe-north2-a
```

2. **Install backend**:
```bash
cd /var/www/portfolio
mkdir backend
# Copy backend files
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

3. **Create systemd service** for Flask app:
```bash
sudo nano /etc/systemd/system/portfolio-api.service
```

4. **Configure nginx** to proxy `/api/*` requests to Flask backend

5. **Update frontend API URL**:
```javascript
const API_BASE_URL = '/api';  // Same domain, proxied by nginx
```

## 🛠️ Tech Stack

**Frontend:**
- Vanilla JavaScript
- Chart.js (charting library)
- Minimalist CSS (matching portfolio style)

**Backend:**
- Python 3.11+
- Flask (lightweight API framework)
- Flask-CORS (handle cross-origin requests)

**Data Sources:**
- Trading: REST API (to be configured)
- Gym: Google Sheets API

## 📝 Development Guidelines

### For Design Work
- Keep styling minimal (black/white, clean lines)
- Match the portfolio aesthetic
- Use system fonts
- Test with mock data first
- Don't modify `fetch()` calls in JavaScript

### For Backend Work
- Keep API response format consistent
- Add error handling
- Log errors properly
- Cache data when appropriate
- Use environment variables for credentials

### Communication Between Frontend/Backend
- Frontend calls backend via `fetch()`
- Backend returns JSON
- Frontend updates DOM
- **Never mix**: Frontend doesn't query databases, backend doesn't render HTML

## 🔒 Security Notes

- **NEVER commit** `.env` file with real credentials
- **NEVER commit** Google Sheets credentials JSON
- Use environment variables for all secrets
- Add `.env` and `credentials.json` to `.gitignore`

## 🐛 Troubleshooting

**Frontend not loading data?**
- Check console for errors
- Verify backend is running (`curl http://localhost:5000/api/health`)
- Check CORS is enabled

**Backend errors?**
- Check Flask console output
- Verify `.env` variables are set
- Test API endpoints with `curl` or Postman

**CORS errors?**
- Ensure `flask-cors` is installed
- Check `CORS(app)` is called in `app.py`
