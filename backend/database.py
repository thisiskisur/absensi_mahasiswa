from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    foto_wajah = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship dengan tabel absensi
    absensi = db.relationship('Absensi', backref='mahasiswa', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nim': self.nim,
            'nama': self.nama,
            'jurusan': self.jurusan,
            'foto_wajah': self.foto_wajah,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Absensi(db.Model):
    __tablename__ = 'absensi'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_mahasiswa = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jam = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='hadir')  # hadir/izin/alpa
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_mahasiswa': self.id_mahasiswa,
            'nama_mahasiswa': self.mahasiswa.nama if self.mahasiswa else None,
            'nim': self.mahasiswa.nim if self.mahasiswa else None,
            'tanggal': self.tanggal.strftime('%Y-%m-%d'),
            'jam': self.jam.strftime('%H:%M:%S'),
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nama': self.nama,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
