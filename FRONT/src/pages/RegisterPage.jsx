import React, { useState } from 'react';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import MenuItem from '@mui/material/MenuItem';
import CircularProgress from '@mui/material/CircularProgress';
import { useNavigate } from 'react-router-dom';

const roles = [
  { value: 'estudiante', label: 'Estudiante' },
  { value: 'docente', label: 'Docente' },
  { value: 'director_gestor', label: 'Director/Gestor' },
  { value: 'vicerrectoria', label: 'Vicerrectoría' },
];

function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    role: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.message || 'Error al registrar usuario');
        setLoading(false);
        return;
      }

      setSuccess('Registro exitoso. Ahora puedes iniciar sesión.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError('Error de red o del servidor');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 10 }}>
      <Paper elevation={6} sx={{ p: 5, borderRadius: 4, boxShadow: 6 }}>
        <Typography component="h1" variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>
          Registro Profesional
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Usuario"
            name="username"
            value={form.username}
            onChange={handleChange}
            required
            fullWidth
            autoFocus
            variant="outlined"
          />
          <TextField
            label="Correo electrónico"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            required
            fullWidth
            variant="outlined"
          />
          <TextField
            label="Contraseña"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            required
            fullWidth
            variant="outlined"
          />
          <TextField
            select
            label="Rol"
            name="role"
            value={form.role}
            onChange={handleChange}
            required
            fullWidth
            variant="outlined"
          >
            {roles.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            fullWidth
            size="large"
            sx={{
              mt: 1,
              py: 1.5,
              fontWeight: 'bold',
              fontSize: '1.1rem',
              letterSpacing: 1,
              boxShadow: 3,
              borderRadius: 2,
            }}
            startIcon={loading && <CircularProgress size={22} color="inherit" />}
          >
            {loading ? 'Registrando...' : 'Registrarse'}
          </Button>
          {error && (
            <Typography color="error" sx={{ mt: 1, textAlign: 'center', fontWeight: 'bold' }}>
              {error}
            </Typography>
          )}
          {success && (
            <Typography color="success.main" sx={{ mt: 1, textAlign: 'center', fontWeight: 'bold' }}>
              {success}
            </Typography>
          )}
        </Box>
      </Paper>
    </Container>
  );
}

export default RegisterPage;