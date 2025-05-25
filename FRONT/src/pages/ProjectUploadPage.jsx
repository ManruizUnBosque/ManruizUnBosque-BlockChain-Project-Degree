import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useAuth } from '../contexts/AuthContext';

function ProjectUploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const { accessToken } = useAuth();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Por favor selecciona un archivo.');
      return;
    }
    setLoading(true);
    setMessage('');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/upload_document', {
        method: 'POST',
        body: formData,
        headers: {
          // If your endpoint requires authentication, add the token:
          // 'Authorization': `Bearer ${accessToken}`,
        },
      });
      if (response.ok) {
        setMessage('Archivo subido correctamente.');
      } else {
        setMessage('Error al subir el archivo.');
      }
    } catch (error) {
      setMessage('Error de red al subir el archivo.');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Subir Proyecto de Grado
        </Typography>
        <Typography variant="body1" gutterBottom>
          Utiliza el siguiente formulario para cargar tu proyecto de grado. Asegúrate de que el archivo cumpla con los requisitos establecidos por la universidad.
        </Typography>
        <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUploadIcon />}
          >
            Seleccionar Archivo
            <input type="file" hidden onChange={handleFileChange} />
          </Button>
          <Button variant="contained" color="primary" onClick={handleUpload} disabled={loading}>
            {loading ? 'Subiendo...' : 'Subir Proyecto'}
          </Button>
          {message && <Typography color="secondary">{message}</Typography>}
        </Box>
      </Paper>
    </Container>
  );
}

export default ProjectUploadPage;