# Panduan Setup Sistem Absensi Mahasiswa

## 📋 Prerequisites

Sebelum menjalankan sistem, pastikan Anda telah menginstall:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download Node.js](https://nodejs.org/)
3. **XAMPP** - [Download XAMPP](https://www.apachefriends.org/)
4. **Webcam** - Untuk testing fitur face recognition

## 🗄️ Setup Database

### 1. Start XAMPP
- Buka XAMPP Control Panel
- Start Apache dan MySQL services
- Pastikan kedua service berjalan (status hijau)

### 2. Buat Database
- Buka browser, akses `http://localhost/phpmyadmin`
- Klik "New" untuk membuat database baru
- Masukkan nama database: `absensi_mahasiswa`
- Klik "Create"

### 3. Import SQL
- Pilih database `absensi_mahasiswa`
- Klik tab "Import"
- Klik "Choose File" dan pilih file `database/absensi.sql`
- Klik "Go" untuk import

### 4. Verifikasi Database
Setelah import berhasil, Anda akan melihat 3 tabel:
- `admin` - Data admin sistem
- `mahasiswa` - Data mahasiswa
- `absensi` - Data absensi

## 🚀 Menjalankan Backend

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Konfigurasi Environment
Buat file `.env` di folder `backend` dengan isi:
```
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
DATABASE_URL=mysql+pymysql://root:@localhost/absensi_mahasiswa
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Jalankan Server
```bash
python app.py
```

Backend akan berjalan di `http://localhost:5000`

## 🎨 Menjalankan Frontend

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Jalankan Development Server
```bash
npm start
```

Frontend akan berjalan di `http://localhost:3000`

## 🔐 Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Mahasiswa (Sample Data)
- NIM: `2021001`
- Password: `2021001` (sama dengan NIM)

## 📱 Fitur yang Tersedia

### Admin Dashboard
- Melihat daftar mahasiswa
- Menambah mahasiswa baru
- Melihat riwayat absensi
- Statistik kehadiran

### Mahasiswa
- Login dengan NIM
- Absensi dengan face recognition
- Melihat status absensi hari ini

## 🐛 Troubleshooting

### Error Database Connection
- Pastikan XAMPP MySQL berjalan
- Cek nama database: `absensi_mahasiswa`
- Pastikan user `root` tanpa password

### Error Face Recognition
- Pastikan webcam terdeteksi
- Install dependencies face_recognition dengan benar
- Pastikan pencahayaan cukup

### Error Frontend
- Pastikan backend berjalan di port 5000
- Cek console browser untuk error detail
- Pastikan semua dependencies terinstall

## 📞 Support

Jika mengalami masalah, cek:
1. Console browser (F12)
2. Terminal backend untuk error logs
3. Pastikan semua prerequisites terpenuhi

## 🔄 Update System

Untuk update sistem:
1. Pull latest code
2. Install ulang dependencies jika ada perubahan
3. Restart backend dan frontend servers
