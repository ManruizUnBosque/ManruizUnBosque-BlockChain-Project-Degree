import React from 'react';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import { Link as RouterLink } from 'react-router-dom';
import Box from '@mui/material/Box';

function NotFoundPage() {
  return (
    <Container component="main" maxWidth="sm" sx={{ textAlign: 'center', mt: 8 }}>
      <Box sx={{ p: 3 }}>
        <Typography variant="h1" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Página No Encontrada
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Lo sentimos, la página que estás buscando no existe o ha sido movida.
        </Typography>
        <Button component={RouterLink} to="/" variant="contained" color="primary">
          Volver al Inicio
        </Button>
      </Box>
    </Container>
  );
}

export default NotFoundPage;