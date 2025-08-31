import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import FaceCapture from '../components/FaceCapture';
import { 
  Camera, 
  CheckCircle, 
  Clock, 
  Calendar,
  User,
  AlertCircle,
  XCircle,
  Loader
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const Absensi = () => {
  const { user } = useAuth();
  const [showCamera, setShowCamera] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [todayAbsensi, setTodayAbsensi] = useState(null);
  const [loading, setLoading] = useState(true);
  const [recognitionResult, setRecognitionResult] = useState(null);

  // Redirect non-mahasiswa users
  if (user?.type !== 'mahasiswa') {
    return <Navigate to="/dashboard" replace />;
  }

  useEffect(() => {
    checkTodayAbsensi();
  }, []);

  const checkTodayAbsensi = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = await axios.get(`/api/absensi?tanggal=${today}&mahasiswa_id=${user.id}`);
      
      if (response.data.success && response.data.data.length > 0) {
        setTodayAbsensi(response.data.data[0]);
      }
    } catch (error) {
      console.error('Error checking today absensi:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCapture = async (imageData) => {
    setShowCamera(false);
    setIsSubmitting(true);
    setRecognitionResult(null);

    try {
      // First, verify if face is detected
      const verifyResponse = await axios.post('/api/absensi/verify-face', {
        image: imageData
      });

      if (verifyResponse.data.success) {
        const { face_detected, face_count } = verifyResponse.data.data;
        
        if (!face_detected) {
          toast.error('Tidak ada wajah terdeteksi dalam foto. Silakan coba lagi.');
          setIsSubmitting(false);
          return;
        }

        if (face_count > 1) {
          toast.error('Hanya satu wajah yang diperbolehkan dalam foto. Silakan coba lagi.');
          setIsSubmitting(false);
          return;
        }

        // If face verification passes, submit attendance
        const response = await axios.post('/api/absensi', {
          image: imageData
        });

        if (response.data.success) {
          toast.success('Absensi berhasil!');
          setTodayAbsensi(response.data.data);
          setRecognitionResult({
            success: true,
            nama: response.data.data.nama,
            confidence: response.data.data.confidence
          });
        } else {
          toast.error(response.data.message || 'Absensi gagal');
          setRecognitionResult({
            success: false,
            message: response.data.message
          });
        }
      } else {
        toast.error('Gagal memverifikasi foto');
      }
    } catch (error) {
      const message = error.response?.data?.message || 'Terjadi kesalahan saat absensi';
      toast.error(message);
      setRecognitionResult({
        success: false,
        message: message
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return '-';
    return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'hadir':
        return 'text-green-600 bg-green-100';
      case 'izin':
        return 'text-yellow-600 bg-yellow-100';
      case 'alpa':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Absensi Mahasiswa
          </h1>
          <p className="text-gray-600">
            Silakan lakukan absensi dengan mengklik tombol di bawah
          </p>
        </motion.div>

        {/* User Info Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-semibold text-gray-900">{user?.nama}</h2>
              <p className="text-gray-600">NIM: {user?.nim}</p>
              <p className="text-gray-600">Jurusan: {user?.jurusan}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-500">Status</p>
              <p className="text-lg font-semibold text-blue-600 capitalize">{user?.type}</p>
            </div>
          </div>
        </motion.div>

        {/* Today's Date */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <div className="flex items-center justify-center space-x-4">
            <Calendar className="h-6 w-6 text-blue-600" />
            <span className="text-lg font-medium text-gray-900">
              {new Date().toLocaleDateString('id-ID', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </span>
            <Clock className="h-6 w-6 text-blue-600" />
            <span className="text-lg font-medium text-gray-900">
              {new Date().toLocaleTimeString('id-ID', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
              })}
            </span>
          </div>
        </motion.div>

        {/* Recognition Result */}
        {recognitionResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className={`bg-white rounded-xl shadow-lg p-6 mb-8 ${
              recognitionResult.success ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'
            }`}
          >
            <div className="text-center">
              <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${
                recognitionResult.success ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {recognitionResult.success ? (
                  <CheckCircle className="h-8 w-8 text-green-600" />
                ) : (
                  <XCircle className="h-8 w-8 text-red-600" />
                )}
              </div>
              <h3 className={`text-xl font-semibold mb-2 ${
                recognitionResult.success ? 'text-green-900' : 'text-red-900'
              }`}>
                {recognitionResult.success ? 'Absensi Berhasil!' : 'Absensi Gagal'}
              </h3>
              {recognitionResult.success ? (
                <div className="space-y-2">
                  <p className="text-gray-600">Nama: {recognitionResult.nama}</p>
                  <p className="text-gray-600">Confidence: {recognitionResult.confidence?.toFixed(2)}%</p>
                </div>
              ) : (
                <p className="text-gray-600">{recognitionResult.message}</p>
              )}
            </div>
          </motion.div>
        )}

        {/* Absensi Status */}
        {todayAbsensi ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Anda sudah melakukan absensi hari ini
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-500">Waktu Absensi</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {formatTime(todayAbsensi.jam)}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500">Tanggal</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {new Date(todayAbsensi.tanggal).toLocaleDateString('id-ID')}
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500">Status</p>
                  <span className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(todayAbsensi.status)}`}>
                    {todayAbsensi.status}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-8 mb-8"
          >
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <AlertCircle className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Anda belum melakukan absensi hari ini
              </h3>
              <p className="text-gray-600 mb-6">
                Silakan klik tombol di bawah untuk melakukan absensi
              </p>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowCamera(true)}
                disabled={isSubmitting}
                className="inline-flex items-center px-8 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-lg font-medium"
              >
                {isSubmitting ? (
                  <>
                    <Loader className="h-6 w-6 mr-3 animate-spin" />
                    Memproses...
                  </>
                ) : (
                  <>
                    <Camera className="h-6 w-6 mr-3" />
                    Absen Sekarang
                  </>
                )}
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* Instructions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-blue-50 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold text-blue-900 mb-4">
            Petunjuk Absensi
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div>
              <p className="font-medium mb-2">Sebelum Absensi:</p>
              <ul className="space-y-1 list-disc list-inside">
                <li>Pastikan pencahayaan cukup</li>
                <li>Posisikan wajah di depan kamera</li>
                <li>Pastikan tidak ada gangguan di belakang</li>
                <li>Pastikan hanya ada satu wajah dalam frame</li>
              </ul>
            </div>
            <div>
              <p className="font-medium mb-2">Saat Absensi:</p>
              <ul className="space-y-1 list-disc list-inside">
                <li>Lihat langsung ke kamera</li>
                <li>Jangan bergerak saat foto diambil</li>
                <li>Tunggu hingga proses selesai</li>
                <li>Sistem akan memverifikasi wajah Anda</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Face Capture Modal */}
      <FaceCapture
        isVisible={showCamera}
        onCapture={handleCapture}
        onClose={() => setShowCamera(false)}
      />
    </div>
  );
};

export default Absensi;
