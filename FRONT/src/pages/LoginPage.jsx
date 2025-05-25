import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import CircularProgress from '@mui/material/CircularProgress';
import Slide from '@mui/material/Slide';

function LoginPage() {
  const [identifier, setidentifier] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleShowPassword = () => setShowPassword((show) => !show);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier:identifier, password }),
      });

      if (!response.ok) {
        setError('Usuario o contraseña incorrectos');
        setLoading(false);
        return;
      }

      const data = await response.json();
      // Ajusta según la estructura real de tu backend
      login(data.user, data.access_token, data.refresh_token);
      navigate('/');
    } catch (err) {
      setError('Error de red o del servidor');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 10 }}>
      <Slide direction="down" in mountOnEnter unmountOnExit>
        <Paper elevation={6} sx={{ p: 5, borderRadius: 4, boxShadow: 6 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ m: 1, bgcolor: 'primary.main', width: 56, height: 56 }}>
              <LockOutlinedIcon fontSize="large" />
            </Avatar>
            <Typography component="h1" variant="h5" sx={{ fontWeight: 'bold', mb: 1 }}>
              Iniciar Sesión
            </Typography>
            <Typography variant="body2" color="text.secondary" align="center">
              Accede a GradoChain con tus credenciales institucionales
            </Typography>
          </Box>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Usuario"
              value={identifier}
              onChange={(e) => setidentifier(e.target.value)}
              required
              fullWidth
              autoFocus
              autoComplete="identifier"
              variant="outlined"
            />
            <TextField
              label="Contraseña"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              fullWidth
              autoComplete="current-password"
              variant="outlined"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="Mostrar/ocultar contraseña"
                      onClick={handleShowPassword}
                      edge="end"
                      size="large"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
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
              {loading ? 'Ingresando...' : 'Ingresar'}
            </Button>
            {error && (
              <Typography color="error" sx={{ mt: 1, textAlign: 'center', fontWeight: 'bold' }}>
                {error}
              </Typography>
            )}
          </Box>
        </Paper>
      </Slide>
    </Container>
  );
}

export default LoginPage;