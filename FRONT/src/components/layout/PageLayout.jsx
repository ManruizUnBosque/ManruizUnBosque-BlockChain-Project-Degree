import React from 'react';
import Box from '@mui/material/Box';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { useAuth } from '../../contexts/AuthContext';

const PageLayout = ({ children, showSidebarOption = true }) => {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const { isAuthenticated } = useAuth();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // Determina si el sidebar debe mostrarse basado en la autenticación y la opción
  const shouldShowSidebar = isAuthenticated && showSidebarOption;

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Navbar onDrawerToggle={handleDrawerToggle} showSidebarButton={shouldShowSidebar} />
      {shouldShowSidebar && (
        <Sidebar 
          mobileOpen={mobileOpen}
          onDrawerToggle={handleDrawerToggle}
        />
      )}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: shouldShowSidebar ? `calc(100% - 240px)` : '100%' }, // 240px es el drawerWidth
          mt: ['56px', '64px'], // Altura del AppBar (móvil, desktop)
          backgroundColor: (theme) => theme.palette.background.default,
          overflow: 'auto', // Para permitir scroll en el contenido si es necesario
        }}
      >
        {/* Toolbar fantasma para empujar el contenido debajo del AppBar fijo */}
        {/* <Toolbar /> No es necesario si mt está bien configurado */}
        {children}
      </Box>
    </Box>
  );
};

export default PageLayout;