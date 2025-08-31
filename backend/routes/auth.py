from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from database import db, Admin, Mahasiswa
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login untuk admin dan mahasiswa"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type', 'admin')  # admin atau mahasiswa
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username dan password diperlukan'
            }), 400
        
        if user_type == 'admin':
            # Login admin
            admin = Admin.query.filter_by(username=username).first()
            if admin and check_password_hash(admin.password, password):
                access_token = create_access_token(
                    identity={'id': admin.id, 'username': admin.username, 'type': 'admin'},
                    expires_delta=timedelta(hours=24)
                )
                return jsonify({
                    'success': True,
                    'message': 'Login berhasil',
                    'token': access_token,
                    'user': {
                        'id': admin.id,
                        'username': admin.username,
                        'nama': admin.nama,
                        'type': 'admin'
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Username atau password salah'
                }), 401
        
        elif user_type == 'mahasiswa':
            # Login mahasiswa (menggunakan NIM sebagai username)
            mahasiswa = Mahasiswa.query.filter_by(nim=username).first()
            if mahasiswa:
                # Untuk mahasiswa, password sama dengan NIM
                if password == mahasiswa.nim:
                    access_token = create_access_token(
                        identity={'id': mahasiswa.id, 'nim': mahasiswa.nim, 'type': 'mahasiswa'},
                        expires_delta=timedelta(hours=24)
                    )
                    return jsonify({
                        'success': True,
                        'message': 'Login berhasil',
                        'token': access_token,
                        'user': {
                            'id': mahasiswa.id,
                            'nim': mahasiswa.nim,
                            'nama': mahasiswa.nama,
                            'jurusan': mahasiswa.jurusan,
                            'type': 'mahasiswa'
                        }
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Password salah'
                    }), 401
            else:
                return jsonify({
                    'success': False,
                    'message': 'NIM tidak ditemukan'
                }), 401
        
        else:
            return jsonify({
                'success': False,
                'message': 'Tipe user tidak valid'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register mahasiswa baru"""
    try:
        data = request.get_json()
        nim = data.get('nim')
        nama = data.get('nama')
        jurusan = data.get('jurusan')
        
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
        
        # Create new mahasiswa
        new_mahasiswa = Mahasiswa(
            nim=nim,
            nama=nama,
            jurusan=jurusan,
            foto_wajah=''  # Will be updated when photo is uploaded
        )
        
        db.session.add(new_mahasiswa)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mahasiswa berhasil didaftarkan',
            'data': new_mahasiswa.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get profile user yang sedang login"""
    try:
        current_user = get_jwt_identity()
        user_type = current_user.get('type')
        
        if user_type == 'admin':
            admin = Admin.query.get(current_user['id'])
            if admin:
                return jsonify({
                    'success': True,
                    'data': admin.to_dict()
                }), 200
        elif user_type == 'mahasiswa':
            mahasiswa = Mahasiswa.query.get(current_user['id'])
            if mahasiswa:
                return jsonify({
                    'success': True,
                    'data': mahasiswa.to_dict()
                }), 200
        
        return jsonify({
            'success': False,
            'message': 'User tidak ditemukan'
        }), 404
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@auth_bp.route('/init-admin', methods=['POST'])
def init_admin():
    """Initialize admin pertama kali (untuk development)"""
    try:
        # Check if admin already exists
        existing_admin = Admin.query.first()
        if existing_admin:
            return jsonify({
                'success': False,
                'message': 'Admin sudah ada'
            }), 400
        
        # Create default admin
        admin = Admin(
            username='admin',
            password=generate_password_hash('admin123'),
            nama='Administrator'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Admin berhasil dibuat',
            'data': {
                'username': 'admin',
                'password': 'admin123'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
