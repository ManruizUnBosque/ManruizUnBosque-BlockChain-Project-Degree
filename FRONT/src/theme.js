import { createTheme } from '@mui/material/styles';

// Define tu paleta de colores, tipografía, etc.
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Un azul estándar de MUI, puedes cambiarlo
    },
    secondary: {
      main: '#dc004e', // Un rosa/rojo estándar de MUI, puedes cambiarlo
    },
    background: {
      default: '#f4f7f6', // Coincide con tu body background
      paper: '#ffffff',   // Color para superficies como Cards, Modals
    },
    text: {
      primary: '#333333',
      secondary: '#555555',
    }
  },
  typography: {
    fontFamily: 'system-ui, Avenir, Helvetica, Arial, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
      marginBlockStart: '0.67em',
      marginBlockEnd: '0.67em',
    },
    h5: { // MUI usa h5 para títulos de diálogo/card a menudo
      fontSize: '1.5rem', // Ajusta según necesites
      fontWeight: 500,
    }
    // ... define otros estilos de tipografía
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none', // Para que los botones no estén en mayúsculas por defecto
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          // Ejemplo: si quieres que el AppBar no tenga sombra por defecto
          // boxShadow: 'none', 
        }
      }
    }
    // ... puedes anular estilos de otros componentes MUI aquí
  },
});

export default theme;