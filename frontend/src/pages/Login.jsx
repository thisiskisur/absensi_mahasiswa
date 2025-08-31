import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { Eye, EyeOff, User, Lock, GraduationCap } from 'lucide-react';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    userType: 'admin'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [registerData, setRegisterData] = useState({
    nim: '',
    nama: '',
    jurusan: ''
  });

  const { login, register } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRegisterChange = (e) => {
    const { name, value } = e.target;
    setRegisterData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (isRegister) {
      const result = await register(registerData.nim, registerData.nama, registerData.jurusan);
      if (result.success) {
        setRegisterData({ nim: '', nama: '', jurusan: '' });
        setIsRegister(false);
      }
    } else {
      await login(formData.username, formData.password, formData.userType);
    }

    setLoading(false);
  };

  const toggleForm = () => {
    setIsRegister(!isRegister);
    setFormData({ username: '', password: '', userType: 'admin' });
    setRegisterData({ nim: '', nama: '', jurusan: '' });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full space-y-8"
      >
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="mx-auto h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center"
          >
            <GraduationCap className="h-8 w-8 text-white" />
          </motion.div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            {isRegister ? 'Daftar Mahasiswa' : 'Masuk ke Sistem'}
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            {isRegister 
              ? 'Daftarkan diri Anda sebagai mahasiswa baru'
              : 'Sistem Absensi Mahasiswa Berbasis Pengenalan Wajah'
            }
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white py-8 px-6 shadow-xl rounded-xl"
        >
          <form className="space-y-6" onSubmit={handleSubmit}>
            {isRegister ? (
              // Register Form
              <>
                <div>
                  <label htmlFor="nim" className="block text-sm font-medium text-gray-700">
                    NIM
                  </label>
                  <div className="mt-1 relative">
                    <input
                      id="nim"
                      name="nim"
                      type="text"
                      required
                      value={registerData.nim}
                      onChange={handleRegisterChange}
                      className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                      placeholder="Masukkan NIM"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="nama" className="block text-sm font-medium text-gray-700">
                    Nama Lengkap
                  </label>
                  <div className="mt-1 relative">
                    <input
                      id="nama"
                      name="nama"
                      type="text"
                      required
                      value={registerData.nama}
                      onChange={handleRegisterChange}
                      className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                      placeholder="Masukkan nama lengkap"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="jurusan" className="block text-sm font-medium text-gray-700">
                    Jurusan
                  </label>
                  <div className="mt-1 relative">
                    <select
                      id="jurusan"
                      name="jurusan"
                      required
                      value={registerData.jurusan}
                      onChange={handleRegisterChange}
                      className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    >
                      <option value="">Pilih Jurusan</option>
                      <option value="Teknik Informatika">Teknik Informatika</option>
                      <option value="Sistem Informasi">Sistem Informasi</option>
                      <option value="Teknik Komputer">Teknik Komputer</option>
                      <option value="Manajemen Informatika">Manajemen Informatika</option>
                    </select>
                  </div>
                </div>
              </>
            ) : (
              // Login Form
              <>
                <div>
                  <label htmlFor="userType" className="block text-sm font-medium text-gray-700">
                    Tipe User
                  </label>
                  <div className="mt-1">
                    <select
                      id="userType"
                      name="userType"
                      value={formData.userType}
                      onChange={handleInputChange}
                      className="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                    >
                      <option value="admin">Admin</option>
                      <option value="mahasiswa">Mahasiswa</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                    {formData.userType === 'admin' ? 'Username' : 'NIM'}
                  </label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <User className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="username"
                      name="username"
                      type="text"
                      required
                      value={formData.username}
                      onChange={handleInputChange}
                      className="appearance-none relative block w-full pl-10 pr-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                      placeholder={formData.userType === 'admin' ? 'Masukkan username' : 'Masukkan NIM'}
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                    Password
                  </label>
                  <div className="mt-1 relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={formData.password}
                      onChange={handleInputChange}
                      className="appearance-none relative block w-full pl-10 pr-10 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                      placeholder="Masukkan password"
                    />
                    <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>
                </div>
              </>
            )}

            <div>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    {isRegister ? 'Mendaftar...' : 'Memproses...'}
                  </div>
                ) : (
                  isRegister ? 'Daftar' : 'Masuk'
                )}
              </motion.button>
            </div>

            <div className="text-center">
              <button
                type="button"
                onClick={toggleForm}
                className="text-sm text-blue-600 hover:text-blue-500 transition-colors duration-200"
              >
                {isRegister 
                  ? 'Sudah punya akun? Masuk di sini'
                  : 'Belum punya akun? Daftar di sini'
                }
              </button>
            </div>
          </form>
        </motion.div>

        <div className="text-center text-xs text-gray-500">
          <p>© 2024 Sistem Absensi Mahasiswa. All rights reserved.</p>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;
