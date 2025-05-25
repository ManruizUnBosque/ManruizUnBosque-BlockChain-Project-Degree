import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import PageLayout from './components/layout/PageLayout';
import ProtectedRoute from './routes/ProtectedRoute';

// Import your pages (create placeholders if they don't exist yet)
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage'; // General dashboard
import StudentDashboardPage from './pages/StudentDashboardPage';
import DirectorDashboardPage from './pages/DirectorDashboardPage';
import CommitteeDashboardPage from './pages/CommitteeDashboardPage';
import ViceDashboardPage from './pages/ViceDashboardPage';
import ProjectUploadPage from './pages/ProjectUploadPage';
import ProjectDetailsPage from './pages/ProjectDetailsPage';
import UserProfilePage from './pages/UserProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Component to redirect to the role-specific dashboard
const RoleBasedRedirect = () => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;

  switch (user.role) {
    case 'estudiante':
      return <Navigate to="/dashboard/student" replace />;
    case 'director_gestor':
      return <Navigate to="/dashboard/director" replace />;
    case 'comite':
      return <Navigate to="/dashboard/committee" replace />;
    case 'vicerrectoria':
      return <Navigate to="/dashboard/vice" replace />;
    default:
      return <Navigate to="/dashboard" replace />; // General dashboard or fallback
  }
};

function AppRoutes() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Protected routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<PageLayout><RoleBasedRedirect /></PageLayout>} />
        <Route path="/dashboard" element={<PageLayout><DashboardPage /></PageLayout>} />
        <Route path="/profile" element={<PageLayout><UserProfilePage /></PageLayout>} />
        
        {/* Role-specific routes (examples) */}
        {/* Student */}
        <Route element={<ProtectedRoute allowedRoles={['estudiante']} />}>
          <Route path="/dashboard/student" element={<PageLayout><StudentDashboardPage /></PageLayout>} />
          <Route path="/project/upload" element={<PageLayout><ProjectUploadPage /></PageLayout>} />
          <Route path="/project/:projectId" element={<PageLayout><ProjectDetailsPage /></PageLayout>} />
        </Route>

        {/* Director/Gestor */}
        <Route element={<ProtectedRoute allowedRoles={['director_gestor']} />}>
          <Route path="/dashboard/director" element={<PageLayout><DirectorDashboardPage /></PageLayout>} />
        </Route>

        {/* Committee */}
        <Route element={<ProtectedRoute allowedRoles={['comite']} />}>
          <Route path="/dashboard/committee" element={<PageLayout><CommitteeDashboardPage /></PageLayout>} />
        </Route>

        {/* Vice-rectory */}
        <Route element={<ProtectedRoute allowedRoles={['vicerrectoria']} />}>
          <Route path="/dashboard/vice" element={<PageLayout><ViceDashboardPage /></PageLayout>} />
        </Route>
      </Route>
      
      {/* Not found route */}
      <Route path="*" element={<PageLayout showSidebarOption={false}><NotFoundPage /></PageLayout>} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;