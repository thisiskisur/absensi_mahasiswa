import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  Menu, 
  X, 
  User, 
  LogOut, 
  GraduationCap, 
  Calendar,
  BarChart3
} from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    logout();
    setIsMenuOpen(false);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-lg fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to={user?.type === 'admin' ? '/dashboard' : '/absensi'}>
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex-shrink-0 flex items-center cursor-pointer"
              >
                <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                  <GraduationCap className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">
                  Absensi Mahasiswa
                </span>
              </motion.div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            {user?.type === 'admin' && (
              <>
                <Link to="/dashboard">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                      isActive('/dashboard') 
                        ? 'text-blue-600 bg-blue-50' 
                        : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    <BarChart3 className="h-4 w-4 mr-2" />
                    Dashboard
                  </motion.button>
                </Link>
                <Link to="/absensi">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                      isActive('/absensi') 
                        ? 'text-blue-600 bg-blue-50' 
                        : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                    }`}
                  >
                    <Calendar className="h-4 w-4 mr-2" />
                    Absensi
                  </motion.button>
                </Link>
              </>
            )}
            
            {user?.type === 'mahasiswa' && (
              <Link to="/absensi">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isActive('/absensi') 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  <Calendar className="h-4 w-4 mr-2" />
                  Absen Sekarang
                </motion.button>
              </Link>
            )}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center">
            <div className="ml-3 relative">
              <motion.div
                whileHover={{ scale: 1.05 }}
                className="flex items-center space-x-3 bg-gray-100 rounded-lg px-4 py-2"
              >
                <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
                <div className="text-sm">
                  <p className="font-medium text-gray-900">{user?.nama || user?.username}</p>
                  <p className="text-gray-500 capitalize">{user?.type}</p>
                </div>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={handleLogout}
                  className="text-gray-400 hover:text-red-500 transition-colors duration-200"
                  title="Logout"
                >
                  <LogOut className="h-5 w-5" />
                </motion.button>
              </motion.div>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              {isMenuOpen ? (
                <X className="block h-6 w-6" />
              ) : (
                <Menu className="block h-6 w-6" />
              )}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <motion.div
        initial={{ opacity: 0, height: 0 }}
        animate={{ 
          opacity: isMenuOpen ? 1 : 0,
          height: isMenuOpen ? 'auto' : 0
        }}
        transition={{ duration: 0.3 }}
        className="md:hidden bg-white border-t border-gray-200"
      >
        <div className="px-2 pt-2 pb-3 space-y-1">
          {user?.type === 'admin' && (
            <>
              <Link to="/dashboard" onClick={() => setIsMenuOpen(false)}>
                <motion.button
                  whileHover={{ x: 5 }}
                  className={`flex items-center w-full px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                    isActive('/dashboard') 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  <BarChart3 className="h-5 w-5 mr-3" />
                  Dashboard
                </motion.button>
              </Link>
              <Link to="/absensi" onClick={() => setIsMenuOpen(false)}>
                <motion.button
                  whileHover={{ x: 5 }}
                  className={`flex items-center w-full px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                    isActive('/absensi') 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  <Calendar className="h-5 w-5 mr-3" />
                  Absensi
                </motion.button>
              </Link>
            </>
          )}
          
          {user?.type === 'mahasiswa' && (
            <Link to="/absensi" onClick={() => setIsMenuOpen(false)}>
              <motion.button
                whileHover={{ x: 5 }}
                className={`flex items-center w-full px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                  isActive('/absensi') 
                    ? 'text-blue-600 bg-blue-50' 
                    : 'text-gray-700 hover:text-blue-600 hover:bg-blue-50'
                }`}
              >
                <Calendar className="h-5 w-5 mr-3" />
                Absen Sekarang
              </motion.button>
            </Link>
          )}
          
          <div className="border-t border-gray-200 pt-4">
            <div className="flex items-center px-3 py-2">
              <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                <User className="h-4 w-4 text-white" />
              </div>
              <div className="text-sm">
                <p className="font-medium text-gray-900">{user?.nama || user?.username}</p>
                <p className="text-gray-500 capitalize">{user?.type}</p>
              </div>
            </div>
            <motion.button
              whileHover={{ x: 5 }}
              onClick={handleLogout}
              className="flex items-center w-full px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 transition-colors duration-200"
            >
              <LogOut className="h-5 w-5 mr-3" />
              Logout
            </motion.button>
          </div>
        </div>
      </motion.div>
    </nav>
  );
};

export default Navbar;
