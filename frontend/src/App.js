import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AbsensiNew from './pages/AbsensiNew';
import Navbar from './components/Navbar';

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles = [] }) => {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (allowedRoles.length > 0 && !allowedRoles.includes(user?.type)) {
    // Redirect based on user type
    if (user?.type === 'admin') {
      return <Navigate to="/dashboard" replace />;
    } else if (user?.type === 'mahasiswa') {
      return <Navigate to="/absensi" replace />;
    }
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Main App Component
const AppContent = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10B981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#EF4444',
              secondary: '#fff',
            },
          },
        }}
      />
      
      {isAuthenticated && <Navbar />}
      
      <main className={isAuthenticated ? 'pt-16' : ''}>
        <Routes>
          <Route 
            path="/login" 
            element={
              isAuthenticated ? (
                user?.type === 'admin' ? <Navigate to="/dashboard" replace /> : <Navigate to="/absensi" replace />
              ) : <Login />
            } 
          />
          
          <Route 
            path="/" 
            element={
              isAuthenticated ? (
                user?.type === 'admin' ? <Navigate to="/dashboard" replace /> : <Navigate to="/absensi" replace />
              ) : <Navigate to="/login" replace />
            } 
          />
          
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/absensi" 
            element={
              <ProtectedRoute allowedRoles={['mahasiswa']}>
                <AbsensiNew />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="*" 
            element={
              isAuthenticated ? (
                user?.type === 'admin' ? <Navigate to="/dashboard" replace /> : <Navigate to="/absensi" replace />
              ) : <Navigate to="/login" replace />
            } 
          />
        </Routes>
      </main>
    </div>
  );
};

// Root App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
