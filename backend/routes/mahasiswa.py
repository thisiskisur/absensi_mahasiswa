from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database import db, Mahasiswa
from model.face_recognition_model import face_model
import os
import uuid
from datetime import datetime

mahasiswa_bp = Blueprint('mahasiswa', __name__)

# Konfigurasi upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mahasiswa_bp.route('/mahasiswa', methods=['GET'])
@jwt_required()
def get_mahasiswa():
    """Get semua data mahasiswa"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        mahasiswa_list = Mahasiswa.query.all()
        data = [mahasiswa.to_dict() for mahasiswa in mahasiswa_list]
        
        return jsonify({
            'success': True,
            'data': data,
            'total': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@mahasiswa_bp.route('/mahasiswa/<int:mahasiswa_id>', methods=['GET'])
@jwt_required()
def get_mahasiswa_by_id(mahasiswa_id):
    """Get data mahasiswa berdasarkan ID"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin or the mahasiswa itself
        if current_user.get('type') == 'mahasiswa' and current_user.get('id') != mahasiswa_id:
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        mahasiswa = Mahasiswa.query.get(mahasiswa_id)
        if not mahasiswa:
            return jsonify({
                'success': False,
                'message': 'Mahasiswa tidak ditemukan'
            }), 404
        
        return jsonify({
            'success': True,
            'data': mahasiswa.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@mahasiswa_bp.route('/mahasiswa', methods=['POST'])
@jwt_required()
def create_mahasiswa():
    """Tambah mahasiswa baru dengan foto wajah"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        # Get form data
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        jurusan = request.form.get('jurusan')
        
        if not nim or not nama or not jurusan:
            return jsonify({
                'success': False,
                'message': 'NIM, nama, dan jurusan diperlukan'
            }), 400
        
        # Check if NIM already exists
        existing_mahasiswa = Mahasiswa.query.filter_by(nim=nim).first()
        if existing_mahasiswa:
            return jsonify({
                'success': False,
                'message': 'NIM sudah terdaftar'
            }), 400
        
        # Handle file upload
        foto_wajah = request.files.get('foto_wajah')
        foto_path = ''
        
        if foto_wajah and allowed_file(foto_wajah.filename):
            # Generate unique filename
            filename = secure_filename(foto_wajah.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            foto_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Ensure upload directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Save file
            foto_wajah.save(foto_path)
            
            # Verify face detection
            if not face_model.detect_face(foto_path):
                # Delete file if no face detected
                os.remove(foto_path)
                return jsonify({
                    'success': False,
                    'message': 'Tidak ada wajah terdeteksi dalam foto'
                }), 400
            
            # Check face count
            face_count = face_model.get_face_count(foto_path)
            if face_count > 1:
                # Delete file if multiple faces
                os.remove(foto_path)
                return jsonify({
                    'success': False,
                    'message': 'Hanya satu wajah yang diperbolehkan dalam foto'
                }), 400
        
        else:
            return jsonify({
                'success': False,
                'message': 'Foto wajah diperlukan dan harus dalam format PNG, JPG, JPEG, atau GIF'
            }), 400
        
        # Create mahasiswa
        new_mahasiswa = Mahasiswa(
            nim=nim,
            nama=nama,
            jurusan=jurusan,
            foto_wajah=foto_path
        )
        
        db.session.add(new_mahasiswa)
        db.session.commit()
        
        # Add face to recognition model
        face_model.add_face(foto_path, new_mahasiswa.id, nama)
        
        return jsonify({
            'success': True,
            'message': 'Mahasiswa berhasil ditambahkan',
            'data': new_mahasiswa.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        # Clean up file if error occurs
        if 'foto_path' in locals() and foto_path and os.path.exists(foto_path):
            os.remove(foto_path)
        
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@mahasiswa_bp.route('/mahasiswa/<int:mahasiswa_id>', methods=['PUT'])
@jwt_required()
def update_mahasiswa(mahasiswa_id):
    """Update data mahasiswa"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        mahasiswa = Mahasiswa.query.get(mahasiswa_id)
        if not mahasiswa:
            return jsonify({
                'success': False,
                'message': 'Mahasiswa tidak ditemukan'
            }), 404
        
        # Get form data
        data = request.get_json()
        nama = data.get('nama')
        jurusan = data.get('jurusan')
        
        if nama:
            mahasiswa.nama = nama
        if jurusan:
            mahasiswa.jurusan = jurusan
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Data mahasiswa berhasil diupdate',
            'data': mahasiswa.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@mahasiswa_bp.route('/mahasiswa/<int:mahasiswa_id>', methods=['DELETE'])
@jwt_required()
def delete_mahasiswa(mahasiswa_id):
    """Hapus mahasiswa"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        mahasiswa = Mahasiswa.query.get(mahasiswa_id)
        if not mahasiswa:
            return jsonify({
                'success': False,
                'message': 'Mahasiswa tidak ditemukan'
            }), 404
        
        # Delete photo file if exists
        if mahasiswa.foto_wajah and os.path.exists(mahasiswa.foto_wajah):
            os.remove(mahasiswa.foto_wajah)
        
        db.session.delete(mahasiswa)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mahasiswa berhasil dihapus'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@mahasiswa_bp.route('/mahasiswa/search', methods=['GET'])
@jwt_required()
def search_mahasiswa():
    """Search mahasiswa berdasarkan nama atau NIM"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        query = request.args.get('q', '')
        if not query:
            return jsonify({
                'success': False,
                'message': 'Query pencarian diperlukan'
            }), 400
        
        # Search by name or NIM
        mahasiswa_list = Mahasiswa.query.filter(
            (Mahasiswa.nama.contains(query)) | 
            (Mahasiswa.nim.contains(query))
        ).all()
        
        data = [mahasiswa.to_dict() for mahasiswa in mahasiswa_list]
        
        return jsonify({
            'success': True,
            'data': data,
            'total': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
