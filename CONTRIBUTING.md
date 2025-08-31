# 🤝 Contributing to Sistem Absensi Mahasiswa

Terima kasih atas minat Anda untuk berkontribusi pada proyek Sistem Absensi Mahasiswa! 

## 📋 Cara Berkontribusi

### 1. Fork Repository
- Klik tombol "Fork" di halaman repository GitHub
- Clone repository yang sudah di-fork ke local machine Anda

### 2. Setup Development Environment
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/absensi_mahasiswa.git
cd absensi_mahasiswa

# Setup backend
cd backend
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
```

### 3. Buat Branch untuk Fitur Baru
```bash
git checkout -b feature/nama-fitur-anda
```

### 4. Lakukan Perubahan
- Buat perubahan yang diperlukan
- Pastikan kode mengikuti standar yang ada
- Tambahkan test jika diperlukan

### 5. Commit Perubahan
```bash
git add .
git commit -m "feat: tambahkan fitur baru"
```

### 6. Push ke Repository Anda
```bash
git push origin feature/nama-fitur-anda
```

### 7. Buat Pull Request
- Buka repository Anda di GitHub
- Klik "Compare & pull request"
- Isi deskripsi perubahan
- Submit pull request

## 📝 Standar Kode

### Python (Backend)
- Gunakan PEP 8 style guide
- Tambahkan docstring untuk fungsi
- Gunakan type hints jika memungkinkan
- Pastikan semua test berjalan

### JavaScript/React (Frontend)
- Gunakan ESLint dan Prettier
- Ikuti React best practices
- Gunakan functional components dengan hooks
- Tambahkan PropTypes untuk komponen

### Commit Messages
Gunakan format conventional commits:
- `feat:` untuk fitur baru
- `fix:` untuk perbaikan bug
- `docs:` untuk dokumentasi
- `style:` untuk formatting
- `refactor:` untuk refactoring
- `test:` untuk test
- `chore:` untuk maintenance

## 🐛 Melaporkan Bug

Jika Anda menemukan bug, silakan buat issue dengan format:

### Bug Report Template
```markdown
**Deskripsi Bug**
Penjelasan singkat tentang bug yang ditemukan.

**Langkah Reproduksi**
1. Buka aplikasi
2. Klik pada ...
3. Lihat error

**Expected Behavior**
Apa yang seharusnya terjadi.

**Actual Behavior**
Apa yang sebenarnya terjadi.

**Screenshots**
Jika ada, tambahkan screenshot.

**Environment**
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 90]
- Version: [e.g. 1.0.0]

**Additional Context**
Informasi tambahan yang relevan.
```

## 💡 Mengusulkan Fitur

Jika Anda ingin mengusulkan fitur baru, buat issue dengan format:

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Penjelasan masalah yang ingin diselesaikan.

**Describe the solution you'd like**
Penjelasan solusi yang diinginkan.

**Describe alternatives you've considered**
Alternatif lain yang sudah dipertimbangkan.

**Additional context**
Informasi tambahan yang relevan.
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📚 Dokumentasi

- Update README.md jika ada perubahan setup
- Tambahkan komentar pada kode yang kompleks
- Update API documentation jika ada endpoint baru

## 🔒 Keamanan

Jika Anda menemukan masalah keamanan, jangan buat issue publik. Silakan email langsung ke maintainer.

## 📞 Kontak

Jika ada pertanyaan, silakan:
- Buat issue di GitHub
- Email: [your-email@example.com]

## 🙏 Terima Kasih

Terima kasih atas kontribusi Anda untuk membuat Sistem Absensi Mahasiswa lebih baik!
