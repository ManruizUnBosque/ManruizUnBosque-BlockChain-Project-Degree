import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import TimelineIcon from '@mui/icons-material/Timeline';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

function StudentDashboardPage() {
  const { user, accessToken } = useAuth();
  const [proyectos, setProyectos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Ejemplo de datos, reemplaza por datos reales desde tu backend
  const resumenProyectos = {
    total: proyectos.length,
    aprobados: proyectos.filter(p => p.estado === 'aprobado').length,
    enRevision: proyectos.filter(p => p.estado === 'en_revision').length,
    rechazados: proyectos.filter(p => p.estado === 'rechazado').length,
  };

  useEffect(() => {
    const fetchProyectos = async () => {
      setLoading(true);
      setError('');
      try {
        // Obtener el token desde localStorage
        const token = localStorage.getItem('accessToken');
        const response = await axios.get('http://localhost:5000/api/mis_proyectos', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setProyectos(response.data.proyectos || []);
      } catch (err) {
        setError('Error al cargar los proyectos');
      }
      setLoading(false);
    };
    fetchProyectos();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        ¡Bienvenido, {user?.username || 'Estudiante'}!
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Aquí puedes gestionar tus proyectos de grado, subir nuevos documentos y consultar el estado de tus entregas.
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        {/* Resumen de proyectos */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="primary" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Proyectos Totales</Typography>
              <Typography variant="h4">{resumenProyectos.total}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <TimelineIcon color="success" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">En Revisión</Typography>
              <Typography variant="h4">{resumenProyectos.enRevision}</Typography>
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 3, display: 'flex', alignItems: 'center' }}>
            <AssignmentTurnedInIcon color="error" sx={{ fontSize: 40, mr: 2 }} />
            <Box>
              <Typography variant="h6">Rechazados</Typography>
              <Typography variant="h4">{resumenProyectos.rechazados}</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Acciones rápidas */}
      <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<CloudUploadIcon />}
          component={RouterLink}
          to="/project/upload"
        >
          Subir Nuevo Proyecto
        </Button>
        <Button
          variant="outlined"
          color="primary"
          startIcon={<AssignmentTurnedInIcon />}
          component={RouterLink}
          to="/student/projects"
        >
          Ver Mis Proyectos
        </Button>
      </Box>

      {/* Listado de proyectos */}
      <Box sx={{ mt: 5 }}>
        <Typography variant="h5" gutterBottom>
          Mis Proyectos
        </Typography>
        {loading ? (
          <Typography>Cargando proyectos...</Typography>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : proyectos.length === 0 ? (
          <Typography>No tienes proyectos registrados.</Typography>
        ) : (
          <Paper sx={{ mt: 2, p: 2 }}>
            <Grid container spacing={2}>
              {proyectos.map((proyecto, idx) => (
                <Grid item xs={12} md={6} key={proyecto.id || idx}>
                  <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
                    <Typography variant="h6">{proyecto.nombre || 'Proyecto sin título'}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Hash SHA256: <span style={{ wordBreak: 'break-all' }}>{proyecto.hash_sha256}</span>
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <a href={decodeURIComponent(proyecto.ruta.replace(/%5C/g, '/'))} target="_blank" rel="noopener noreferrer">
                        Descargar archivo
                      </a>
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Paper>
        )}
      </Box>
    </Container>
  );
}

export default StudentDashboardPage;