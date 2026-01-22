# Setup Guide

This guide will help you get the Decision Intelligence Platform up and running.

## Step-by-Step Setup

### 1. Clone or Navigate to the Project

```bash
cd decision-intelligence-platform
```

### 2. Backend Setup

#### Windows:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
# Make sure you're in the backend directory with venv activated
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit http://localhost:8000/docs to see the API documentation.

### 4. Frontend Setup (New Terminal)

Open a new terminal window and:

```bash
cd frontend
npm install
```

### 5. Start the Frontend

```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

### 6. Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Upload CSV File"
3. Select the sample file: `data/sample_data.csv`
4. View the generated decision insights!

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Module not found errors:**
- Make sure your virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port 3000 already in use:**
- Vite will automatically use the next available port
- Or update `vite.config.js` to use a different port

**npm install fails:**
- Make sure you have Node.js 16+ installed
- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

**API connection errors:**
- Make sure the backend is running on port 8000
- Check that CORS is properly configured in `backend/core/config.py`

## Verifying Installation

### Backend Check:
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"healthy"}`

### Frontend Check:
- Open http://localhost:3000
- You should see the "Decision Intelligence Platform" header

## Next Steps

- Try uploading your own CSV file with transaction data
- Explore the API documentation at http://localhost:8000/docs
- Review the decision insights generated from your data
