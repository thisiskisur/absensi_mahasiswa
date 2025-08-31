@echo off
echo Setting up Database for Absensi Mahasiswa System
echo.
echo This script will help you set up the database in XAMPP
echo.
echo Steps:
echo 1. Make sure XAMPP is installed and MySQL service is running
echo 2. Open phpMyAdmin at http://localhost/phpmyadmin
echo 3. Create a new database named 'absensi_mahasiswa'
echo 4. Import the SQL file from database/absensi.sql
echo.
echo Database setup instructions:
echo.
echo 1. Start XAMPP Control Panel
echo 2. Start Apache and MySQL services
echo 3. Open browser and go to http://localhost/phpmyadmin
echo 4. Click "New" to create new database
echo 5. Enter "absensi_mahasiswa" as database name
echo 6. Click "Create"
echo 7. Select the "absensi_mahasiswa" database
echo 8. Click "Import" tab
echo 9. Click "Choose File" and select database/absensi.sql
echo 10. Click "Go" to import
echo.
echo Default admin credentials:
echo Username: admin
echo Password: admin123
echo.
pause
