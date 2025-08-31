from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, Absensi, Mahasiswa
from model.face_recognition_model import face_model
from datetime import datetime, date, time
import base64
import os

absensi_bp = Blueprint('absensi', __name__)

@absensi_bp.route('/absensi', methods=['POST'])
@jwt_required()
def submit_absensi():
    """Submit absensi dengan foto wajah"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Get image data (base64)
        image_data = data.get('image')
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'Foto wajah diperlukan'
            }), 400
        
        # Recognize face
        recognition_result, error = face_model.recognize_face(image_data)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        if not recognition_result:
            return jsonify({
                'success': False,
                'message': 'Wajah tidak dikenali'
            }), 400
        
        mahasiswa_id = recognition_result['mahasiswa_id']
        nama = recognition_result['nama']
        confidence = recognition_result['confidence']
        
        # Check if user is mahasiswa and matches the recognized face
        if current_user.get('type') == 'mahasiswa' and current_user.get('id') != mahasiswa_id:
            return jsonify({
                'success': False,
                'message': 'Wajah tidak sesuai dengan akun yang login'
            }), 403
        
        # Check if already absen today
        today = date.today()
        existing_absensi = Absensi.query.filter_by(
            id_mahasiswa=mahasiswa_id,
            tanggal=today
        ).first()
        
        if existing_absensi:
            return jsonify({
                'success': False,
                'message': 'Anda sudah melakukan absensi hari ini'
            }), 400
        
        # Create absensi record
        now = datetime.now()
        new_absensi = Absensi(
            id_mahasiswa=mahasiswa_id,
            tanggal=today,
            jam=now.time(),
            status='hadir'
        )
        
        db.session.add(new_absensi)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Absensi berhasil',
            'data': {
                'nama': nama,
                'tanggal': today.strftime('%Y-%m-%d'),
                'jam': now.strftime('%H:%M:%S'),
                'confidence': confidence
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@absensi_bp.route('/absensi', methods=['GET'])
@jwt_required()
def get_absensi():
    """Get riwayat absensi"""
    try:
        current_user = get_jwt_identity()
        
        # Get query parameters
        mahasiswa_id = request.args.get('mahasiswa_id')
        tanggal = request.args.get('tanggal')
        status = request.args.get('status')
        
        # Build query
        query = Absensi.query
        
        # Filter by mahasiswa_id if provided
        if mahasiswa_id:
            query = query.filter_by(id_mahasiswa=mahasiswa_id)
        elif current_user.get('type') == 'mahasiswa':
            # If mahasiswa, only show their own absensi
            query = query.filter_by(id_mahasiswa=current_user.get('id'))
        
        # Filter by tanggal if provided
        if tanggal:
            try:
                tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d').date()
                query = query.filter_by(tanggal=tanggal_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Format tanggal tidak valid (YYYY-MM-DD)'
                }), 400
        
        # Filter by status if provided
        if status:
            query = query.filter_by(status=status)
        
        # Order by tanggal and jam (newest first)
        absensi_list = query.order_by(Absensi.tanggal.desc(), Absensi.jam.desc()).all()
        
        data = [absensi.to_dict() for absensi in absensi_list]
        
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

@absensi_bp.route('/absensi/<int:absensi_id>', methods=['GET'])
@jwt_required()
def get_absensi_by_id(absensi_id):
    """Get detail absensi berdasarkan ID"""
    try:
        current_user = get_jwt_identity()
        
        absensi = Absensi.query.get(absensi_id)
        if not absensi:
            return jsonify({
                'success': False,
                'message': 'Absensi tidak ditemukan'
            }), 404
        
        # Check if user has access to this absensi
        if current_user.get('type') == 'mahasiswa' and current_user.get('id') != absensi.id_mahasiswa:
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        return jsonify({
            'success': True,
            'data': absensi.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@absensi_bp.route('/absensi/<int:absensi_id>', methods=['PUT'])
@jwt_required()
def update_absensi(absensi_id):
    """Update status absensi (admin only)"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        absensi = Absensi.query.get(absensi_id)
        if not absensi:
            return jsonify({
                'success': False,
                'message': 'Absensi tidak ditemukan'
            }), 404
        
        data = request.get_json()
        status = data.get('status')
        
        if status and status in ['hadir', 'izin', 'alpa']:
            absensi.status = status
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Status absensi berhasil diupdate',
                'data': absensi.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Status tidak valid (hadir/izin/alpa)'
            }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@absensi_bp.route('/absensi/<int:absensi_id>', methods=['DELETE'])
@jwt_required()
def delete_absensi(absensi_id):
    """Hapus absensi (admin only)"""
    try:
        current_user = get_jwt_identity()
        
        # Check if user is admin
        if current_user.get('type') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Akses ditolak'
            }), 403
        
        absensi = Absensi.query.get(absensi_id)
        if not absensi:
            return jsonify({
                'success': False,
                'message': 'Absensi tidak ditemukan'
            }), 404
        
        db.session.delete(absensi)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Absensi berhasil dihapus'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@absensi_bp.route('/absensi/statistics', methods=['GET'])
@jwt_required()
def get_absensi_statistics():
    """Get statistik absensi"""
    try:
        current_user = get_jwt_identity()
        
        # Get query parameters
        mahasiswa_id = request.args.get('mahasiswa_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Absensi.query
        
        # Filter by mahasiswa_id if provided
        if mahasiswa_id:
            query = query.filter_by(id_mahasiswa=mahasiswa_id)
        elif current_user.get('type') == 'mahasiswa':
            # If mahasiswa, only show their own statistics
            query = query.filter_by(id_mahasiswa=current_user.get('id'))
        
        # Filter by date range if provided
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Absensi.tanggal >= start_date_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Format start_date tidak valid (YYYY-MM-DD)'
                }), 400
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Absensi.tanggal <= end_date_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Format end_date tidak valid (YYYY-MM-DD)'
                }), 400
        
        # Get all absensi in the range
        absensi_list = query.all()
        
        # Calculate statistics
        total = len(absensi_list)
        hadir = len([a for a in absensi_list if a.status == 'hadir'])
        izin = len([a for a in absensi_list if a.status == 'izin'])
        alpa = len([a for a in absensi_list if a.status == 'alpa'])
        
        # Calculate percentage
        hadir_pct = (hadir / total * 100) if total > 0 else 0
        izin_pct = (izin / total * 100) if total > 0 else 0
        alpa_pct = (alpa / total * 100) if total > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'hadir': hadir,
                'izin': izin,
                'alpa': alpa,
                'hadir_percentage': round(hadir_pct, 2),
                'izin_percentage': round(izin_pct, 2),
                'alpa_percentage': round(alpa_pct, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@absensi_bp.route('/absensi/verify-face', methods=['POST'])
@jwt_required()
def verify_face():
    """Verify apakah ada wajah dalam foto (untuk testing)"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({
                'success': False,
                'message': 'Foto wajah diperlukan'
            }), 400
        
        # Check if face is detected
        face_detected = face_model.detect_face(image_data)
        face_count = face_model.get_face_count(image_data)
        
        return jsonify({
            'success': True,
            'data': {
                'face_detected': face_detected,
                'face_count': face_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
