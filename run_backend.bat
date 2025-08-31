@echo off
echo Starting Backend Server...
echo.
echo Make sure you have:
echo 1. Python 3.8+ installed
echo 2. XAMPP MySQL running
echo 3. Database 'absensi_mahasiswa' created
echo.
cd backend
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
python app.py
pause
