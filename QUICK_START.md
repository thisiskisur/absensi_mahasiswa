# 🚀 Quick Start Guide - Sistem Absensi Mahasiswa

## ✅ Status Sistem
- ✅ Backend API: Berfungsi di port 5001
- ✅ Database: Terhubung dan berfungsi
- ✅ Admin Login: Berfungsi
- ✅ Mahasiswa Login: Berfungsi
- ✅ Frontend: Siap digunakan

## 🎯 Cara Menjalankan Sistem

### 1. Jalankan Backend (Terminal 1)
```bash
cd backend
python app.py
```
Backend akan berjalan di: `http://localhost:5001`

### 2. Jalankan Frontend (Terminal 2)
```bash
cd frontend
npm start
```
Frontend akan berjalan di: `http://localhost:3000`

## 🔐 Login Credentials

### Admin
- **Username**: `admin`
- **Password**: `admin123`
- **Akses**: Dashboard admin untuk mengelola mahasiswa dan absensi

### Mahasiswa
- **NIM**: `2021001`
- **Password**: `2021001` (sama dengan NIM)
- **Akses**: Halaman absensi untuk melakukan absen

## 📱 Fitur yang Tersedia

### Admin Dashboard (`/dashboard`)
- Melihat daftar mahasiswa
- Menambah mahasiswa baru
- Melihat riwayat absensi
- Statistik kehadiran

### Mahasiswa Absensi (`/absensi`)
- Login dengan NIM
- Absensi dengan face recognition
- Melihat status absensi hari ini

## 🔧 Troubleshooting

### Jika ada error:
1. **Pastikan XAMPP MySQL berjalan**
2. **Pastikan database `absensi_mahasiswa` sudah dibuat**
3. **Restart backend server jika diperlukan**

### Test API:
```bash
cd backend
python test_db.py
```

## 🎉 Selamat Menggunakan!
Sistem sudah siap digunakan untuk absensi mahasiswa dengan face recognition!
