import React from 'react';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import { useAuth } from '../contexts/AuthContext';

function DashboardPage() {
  const { user } = useAuth();
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard General
        </Typography>
        <Typography variant="body1">
          Bienvenido a GradoChain, {user?.username || 'Usuario'}.
        </Typography>
        <Typography variant="body2" sx={{mt: 2}}>
          Este es el dashboard principal. Desde aquí podrás navegar a las diferentes secciones según tu rol.
        </Typography>
        {/* Aquí podrías añadir más contenido o widgets */}
      </Paper>
    </Container>
  );
}

export default DashboardPage;