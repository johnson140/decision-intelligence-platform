# Decision Intelligence Platform - Frontend

React frontend for the Decision Intelligence Platform.

## Setup

1. Install dependencies:
```bash
npm install
```

## Running the Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Features

- CSV file upload for transaction data
- Real-time decision insight generation
- Filterable decision insights by priority
- Summary dashboard with key metrics
- Clean, modern UI optimized for business users

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── DataUpload.jsx      # CSV upload component
│   │   ├── DecisionInsights.jsx # Decision insights display
│   │   └── Summary.jsx          # Summary dashboard
│   ├── App.jsx                  # Main application component
│   ├── main.jsx                 # Application entry point
│   └── index.css                # Global styles
├── index.html                   # HTML template
└── vite.config.js               # Vite configuration
```
