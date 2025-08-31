-- Database: absensi_mahasiswa
-- Created for XAMPP MySQL

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS absensi_mahasiswa;
USE absensi_mahasiswa;

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS absensi;
DROP TABLE IF EXISTS mahasiswa;
DROP TABLE IF EXISTS admin;

-- Create admin table
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create mahasiswa table
CREATE TABLE mahasiswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nim VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(50) NOT NULL,
    foto_wajah VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create absensi table
CREATE TABLE absensi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_mahasiswa INT NOT NULL,
    tanggal DATE NOT NULL,
    jam TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'hadir',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_mahasiswa) REFERENCES mahasiswa(id) ON DELETE CASCADE
);

-- Insert default admin user
INSERT INTO admin (username, password, nama) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.Gi', 'Administrator');

-- Insert sample mahasiswa data (for testing)
INSERT INTO mahasiswa (nim, nama, jurusan, foto_wajah) VALUES 
('2021001', 'Ahmad Fauzi', 'Teknik Informatika', ''),
('2021002', 'Siti Nurhaliza', 'Sistem Informasi', ''),
('2021003', 'Budi Santoso', 'Teknik Komputer', ''),
('2021004', 'Dewi Sartika', 'Manajemen Informatika', ''),
('2021005', 'Rudi Hermawan', 'Teknik Informatika', '');

-- Insert sample absensi data (for testing)
INSERT INTO absensi (id_mahasiswa, tanggal, jam, status) VALUES 
(1, CURDATE(), '08:00:00', 'hadir'),
(2, CURDATE(), '08:15:00', 'hadir'),
(3, CURDATE(), '08:30:00', 'hadir'),
(4, CURDATE(), '09:00:00', 'izin'),
(5, CURDATE(), NULL, 'alpa');

-- Create indexes for better performance
CREATE INDEX idx_mahasiswa_nim ON mahasiswa(nim);
CREATE INDEX idx_absensi_mahasiswa ON absensi(id_mahasiswa);
CREATE INDEX idx_absensi_tanggal ON absensi(tanggal);
CREATE INDEX idx_absensi_status ON absensi(status);

-- Show table structure
DESCRIBE admin;
DESCRIBE mahasiswa;
DESCRIBE absensi;

-- Show sample data
SELECT 'Admin Users:' as info;
SELECT id, username, nama, created_at FROM admin;

SELECT 'Mahasiswa Data:' as info;
SELECT id, nim, nama, jurusan, created_at FROM mahasiswa;

SELECT 'Absensi Data:' as info;
SELECT a.id, m.nama, a.tanggal, a.jam, a.status 
FROM absensi a 
JOIN mahasiswa m ON a.id_mahasiswa = m.id 
ORDER BY a.tanggal DESC, a.jam DESC;
