import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Tus estilos globales (ahora más limpios)
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline'; // Normaliza estilos y aplica el background del tema
import theme from './theme'; // Tu tema personalizado

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Importante para que el tema se aplique correctamente */}
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
