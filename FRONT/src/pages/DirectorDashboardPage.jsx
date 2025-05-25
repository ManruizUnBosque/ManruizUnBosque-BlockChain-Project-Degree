import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import TimelineIcon from '@mui/icons-material/Timeline';

function DirectorDashboardPage() {
  const { user } = useAuth();

  // Ejemplo de datos, reemplaza por datos reales desde tu backend
  const resumenProyectos = {
    asignados: 5,
    enRevision: 2,
    aprobados: 2,
    rechazados: 1,
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Panel de Director/Gestor
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Bienvenido, {user?.username || 'Director'}. Aquí puedes gestionar los proyectos asignados y su estado.
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <SupervisorAccountIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Proyectos Asignados</Typography>
              <Typography variant="h4">{resumenProyectos.asignados}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <TimelineIcon color="warning" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">En Revisión</Typography>
              <Typography variant="h4">{resumenProyectos.enRevision}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={2}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Aprobados</Typography>
              <Typography variant="h4">{resumenProyectos.aprobados}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={2}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="error" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Rechazados</Typography>
              <Typography variant="h4">{resumenProyectos.rechazados}</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
      {/* Aquí puedes agregar más widgets o acciones rápidas */}
    </Container>
  );
}

export default DirectorDashboardPage;