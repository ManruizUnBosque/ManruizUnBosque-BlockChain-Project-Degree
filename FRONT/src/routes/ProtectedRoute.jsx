import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

const ProtectedRoute = ({ allowedRoles }) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    // Muestra un spinner mientras se carga el estado de autenticación
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    // Idealmente, redirigir a una página de "No Autorizado" o al dashboard principal
    // Por ahora, redirigimos al login, pero podrías crear una página específica /unauthorized
    console.warn(`User role ${user.role} not in allowed roles: ${allowedRoles.join(', ')}`);
    return <Navigate to="/login" state={{ from: location }} replace />; // O a /unauthorized
  }

  return <Outlet />;
};

export default ProtectedRoute;