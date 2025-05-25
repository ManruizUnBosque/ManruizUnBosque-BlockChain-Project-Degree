import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Divider from '@mui/material/Divider';

// Importa los iconos que necesites
import DashboardIcon from '@mui/icons-material/Dashboard';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import PeopleIcon from '@mui/icons-material/People'; // Ejemplo para Comité
import SchoolIcon from '@mui/icons-material/School'; // Ejemplo para Estudiante
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount'; // Ejemplo para Director
import GavelIcon from '@mui/icons-material/Gavel'; // Ejemplo para Vicerrectoría

import { useAuth } from '../../contexts/AuthContext';

const drawerWidth = 240;

const Sidebar = ({ mobileOpen, onDrawerToggle }) => {
  const { user } = useAuth(); // Para mostrar items según el rol
  const location = useLocation();

  // Define tus items de menú aquí, podrías hacerlos dinámicos según el rol
  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/', roles: ['estudiante', 'director_gestor', 'comite', 'vicerrectoria'] },
    { text: 'Subir Proyecto', icon: <CloudUploadIcon />, path: '/project/upload', roles: ['estudiante'] },
    // Ejemplo de items específicos por rol:
    
    { text: 'Proyectos Asignados', icon: <SupervisorAccountIcon />, path: '/director/projects', roles: ['director_gestor'] },
    { text: 'Revisión Comité', icon: <PeopleIcon />, path: '/committee/review', roles: ['comite'] },
    { text: 'Gestión General', icon: <GavelIcon />, path: '/vice/management', roles: ['vicerrectoria'] },
  ];

  const drawerContent = (
    <div>
      <Toolbar /> {/* Para alinear con el AppBar */}
      <Divider />
      <List>
        {menuItems.filter(item => !item.roles || (user && item.roles.includes(user.role))).map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton component={RouterLink} to={item.path} selected={location.pathname === item.path}>
              <ListItemIcon>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      aria-label="mailbox folders"
    >
      {/* Drawer para móvil */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawerContent}
      </Drawer>
      {/* Drawer para desktop */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
        open // El drawer permanente siempre está abierto en desktop
      >
        {drawerContent}
      </Drawer>
    </Box>
  );
};

export default Sidebar;