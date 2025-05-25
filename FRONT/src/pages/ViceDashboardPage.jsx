import React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import TimelineIcon from '@mui/icons-material/Timeline';
import SupervisorAccountIcon from '@mui/icons-material/SupervisorAccount';
import AssessmentIcon from '@mui/icons-material/Assessment';

function ViceDashboardPage() {
  // Datos de ejemplo, reemplaza por datos reales de tu backend
  const resumen = {
    totalProyectos: 20,
    enRevision: 5,
    aprobados: 12,
    rechazados: 3,
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Panel de Vicerrectoría
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Bienvenido/a. Aquí puedes supervisar el estado global de los proyectos de grado y tomar decisiones estratégicas.
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssessmentIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Total Proyectos</Typography>
              <Typography variant="h4">{resumen.totalProyectos}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <TimelineIcon color="warning" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">En Revisión</Typography>
              <Typography variant="h4">{resumen.enRevision}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Aprobados</Typography>
              <Typography variant="h4">{resumen.aprobados}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="error" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Rechazados</Typography>
              <Typography variant="h4">{resumen.rechazados}</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Acciones rápidas */}
      <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<SupervisorAccountIcon />}
        >
          Ver Gestión de Proyectos
        </Button>
        <Button
          variant="outlined"
          color="primary"
          startIcon={<AssessmentIcon />}
        >
          Generar Reporte Global
        </Button>
      </Box>
    </Container>
  );
}

export default ViceDashboardPage;