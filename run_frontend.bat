@echo off
echo Starting Frontend Development Server...
echo.
echo Make sure you have:
echo 1. Node.js 16+ installed
echo 2. Backend server running on http://localhost:5000
echo.
cd frontend
echo Installing dependencies...
npm install
echo.
echo Starting React development server...
npm start
pause
