---
name: material-ui
description: Builds React applications with Material UI (MUI) components implementing Material Design. Use when creating modern UIs with Google's design system, custom theming, or accessible form controls.
---

# Material UI (MUI)

React component library implementing Google's Material Design with extensive customization.

## Quick Start

```bash
npm install @mui/material @emotion/react @emotion/styled
npm install @mui/icons-material
```

```tsx
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Button from '@mui/material/Button';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Button variant="contained">Hello World</Button>
    </ThemeProvider>
  );
}
```

## Core Components

### Button

```tsx
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import LoadingButton from '@mui/lab/LoadingButton';
import DeleteIcon from '@mui/icons-material/Delete';
import SendIcon from '@mui/icons-material/Send';

// Variants
<Button variant="text">Text</Button>
<Button variant="contained">Contained</Button>
<Button variant="outlined">Outlined</Button>

// Colors
<Button color="primary">Primary</Button>
<Button color="secondary">Secondary</Button>
<Button color="success">Success</Button>
<Button color="error">Error</Button>

// Sizes
<Button size="small">Small</Button>
<Button size="medium">Medium</Button>
<Button size="large">Large</Button>

// With icons
<Button variant="contained" startIcon={<SendIcon />}>Send</Button>
<Button variant="outlined" endIcon={<DeleteIcon />}>Delete</Button>

// Icon button
<IconButton color="primary" aria-label="delete">
  <DeleteIcon />
</IconButton>

// Loading button
<LoadingButton loading variant="contained">Submit</LoadingButton>
<LoadingButton loading loadingPosition="start" startIcon={<SaveIcon />}>
  Save
</LoadingButton>
```

### TextField

```tsx
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import Visibility from '@mui/icons-material/Visibility';

// Variants
<TextField label="Outlined" variant="outlined" />
<TextField label="Filled" variant="filled" />
<TextField label="Standard" variant="standard" />

// States
<TextField label="Required" required />
<TextField label="Disabled" disabled />
<TextField label="Error" error helperText="Invalid input" />

// Types
<TextField label="Password" type="password" />
<TextField label="Number" type="number" />
<TextField label="Multiline" multiline rows={4} />

// With adornments
<TextField
  label="Amount"
  InputProps={{
    startAdornment: <InputAdornment position="start">$</InputAdornment>,
  }}
/>

<TextField
  label="Password"
  type={showPassword ? 'text' : 'password'}
  InputProps={{
    endAdornment: (
      <InputAdornment position="end">
        <IconButton onClick={handleClickShowPassword}>
          {showPassword ? <VisibilityOff /> : <Visibility />}
        </IconButton>
      </InputAdornment>
    ),
  }}
/>
```

### Select

```tsx
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

// Basic select
<FormControl fullWidth>
  <InputLabel id="demo-label">Age</InputLabel>
  <Select
    labelId="demo-label"
    id="demo-select"
    value={age}
    label="Age"
    onChange={handleChange}
  >
    <MenuItem value={10}>Ten</MenuItem>
    <MenuItem value={20}>Twenty</MenuItem>
    <MenuItem value={30}>Thirty</MenuItem>
  </Select>
</FormControl>

// Multiple select
<Select
  multiple
  value={personName}
  onChange={handleChange}
  renderValue={(selected) => selected.join(', ')}
>
  {names.map((name) => (
    <MenuItem key={name} value={name}>
      <Checkbox checked={personName.indexOf(name) > -1} />
      <ListItemText primary={name} />
    </MenuItem>
  ))}
</Select>
```

### Dialog

```tsx
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
} from '@mui/material';

function AlertDialog() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button variant="outlined" onClick={() => setOpen(true)}>
        Open Dialog
      </Button>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Confirm Delete
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete this item?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleDelete} autoFocus color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
```

### Card

```tsx
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
} from '@mui/material';

<Card sx={{ maxWidth: 345 }}>
  <CardMedia
    component="img"
    height="140"
    image="/image.jpg"
    alt="Product"
  />
  <CardContent>
    <Typography gutterBottom variant="h5" component="div">
      Product Name
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Product description goes here. This is a brief overview.
    </Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Share</Button>
    <Button size="small">Learn More</Button>
  </CardActions>
</Card>
```

### Snackbar

```tsx
import { Snackbar, Alert, Button } from '@mui/material';

function SnackbarDemo() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)}>Show Snackbar</Button>
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={() => setOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={() => setOpen(false)}
          severity="success"
          variant="filled"
          sx={{ width: '100%' }}
        >
          Operation completed successfully!
        </Alert>
      </Snackbar>
    </>
  );
}

// Severity options: success, info, warning, error
```

### Tabs

```tsx
import { Tabs, Tab, Box } from '@mui/material';

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index} role="tabpanel">
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function TabsDemo() {
  const [value, setValue] = useState(0);

  return (
    <Box sx={{ width: '100%' }}>
      <Tabs value={value} onChange={(e, newValue) => setValue(newValue)}>
        <Tab label="Item One" />
        <Tab label="Item Two" />
        <Tab label="Item Three" />
      </Tabs>
      <TabPanel value={value} index={0}>Content One</TabPanel>
      <TabPanel value={value} index={1}>Content Two</TabPanel>
      <TabPanel value={value} index={2}>Content Three</TabPanel>
    </Box>
  );
}
```

### Menu

```tsx
import { Menu, MenuItem, Button, ListItemIcon, ListItemText } from '@mui/material';
import ContentCut from '@mui/icons-material/ContentCut';
import ContentCopy from '@mui/icons-material/ContentCopy';
import ContentPaste from '@mui/icons-material/ContentPaste';

function MenuDemo() {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  return (
    <>
      <Button
        onClick={(e) => setAnchorEl(e.currentTarget)}
        aria-controls={open ? 'menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
      >
        Open Menu
      </Button>
      <Menu
        id="menu"
        anchorEl={anchorEl}
        open={open}
        onClose={() => setAnchorEl(null)}
      >
        <MenuItem onClick={() => setAnchorEl(null)}>
          <ListItemIcon><ContentCut fontSize="small" /></ListItemIcon>
          <ListItemText>Cut</ListItemText>
        </MenuItem>
        <MenuItem onClick={() => setAnchorEl(null)}>
          <ListItemIcon><ContentCopy fontSize="small" /></ListItemIcon>
          <ListItemText>Copy</ListItemText>
        </MenuItem>
        <MenuItem onClick={() => setAnchorEl(null)}>
          <ListItemIcon><ContentPaste fontSize="small" /></ListItemIcon>
          <ListItemText>Paste</ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}
```

## The sx Prop

MUI's styling shorthand:

```tsx
import { Box, Button } from '@mui/material';

<Box
  sx={{
    // Spacing (theme.spacing * n)
    p: 2,              // padding: 16px
    m: 1,              // margin: 8px
    px: 3,             // paddingX: 24px
    my: 'auto',        // marginY: auto

    // Colors from theme
    bgcolor: 'primary.main',
    color: 'text.secondary',

    // Sizing
    width: 300,
    maxWidth: '100%',
    height: 'auto',

    // Flexbox
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 2,

    // Border
    border: 1,
    borderColor: 'divider',
    borderRadius: 2,

    // Typography
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',

    // Shadows
    boxShadow: 3,

    // Responsive
    width: { xs: '100%', sm: 400, md: 500 },

    // Pseudo-classes
    '&:hover': {
      bgcolor: 'primary.dark',
    },

    // Nested selectors
    '& .child': {
      color: 'secondary.main',
    },
  }}
>
  Content
</Box>
```

## Theming

### Custom Theme

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light', // or 'dark'
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
      contrastText: '#fff',
    },
    secondary: {
      main: '#9c27b0',
    },
    error: {
      main: '#d32f2f',
    },
    warning: {
      main: '#ed6c02',
    },
    info: {
      main: '#0288d1',
    },
    success: {
      main: '#2e7d32',
    },
    background: {
      default: '#f5f5f5',
      paper: '#fff',
    },
    text: {
      primary: 'rgba(0, 0, 0, 0.87)',
      secondary: 'rgba(0, 0, 0, 0.6)',
      disabled: 'rgba(0, 0, 0, 0.38)',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    button: {
      textTransform: 'none', // Disable uppercase
    },
  },
  shape: {
    borderRadius: 8,
  },
  spacing: 8, // Default spacing unit
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 24px',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
      defaultProps: {
        disableElevation: true,
      },
    },
    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
        size: 'small',
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});

<ThemeProvider theme={theme}>
  <CssBaseline />
  <App />
</ThemeProvider>
```

### Dark Mode

```tsx
import { createTheme, ThemeProvider } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useMemo, useState } from 'react';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState(prefersDarkMode ? 'dark' : 'light');

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === 'dark'
            ? {
                background: {
                  default: '#121212',
                  paper: '#1e1e1e',
                },
              }
            : {}),
        },
      }),
    [mode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Button onClick={() => setMode(mode === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </Button>
    </ThemeProvider>
  );
}
```

### useTheme Hook

```tsx
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

function MyComponent() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box
      sx={{
        backgroundColor: theme.palette.primary.main,
        padding: theme.spacing(2),
      }}
    >
      {isMobile ? 'Mobile View' : 'Desktop View'}
    </Box>
  );
}
```

## Layout

### Box

```tsx
import Box from '@mui/material/Box';

<Box
  component="section"
  sx={{ p: 2, border: '1px solid grey' }}
>
  Content
</Box>
```

### Container

```tsx
import Container from '@mui/material/Container';

<Container maxWidth="sm">Small container</Container>
<Container maxWidth="md">Medium container</Container>
<Container maxWidth="lg">Large container</Container>
<Container maxWidth="xl">Extra large container</Container>
```

### Grid

```tsx
import Grid from '@mui/material/Grid';

<Grid container spacing={2}>
  <Grid item xs={12} sm={6} md={4}>
    <Item>xs=12 sm=6 md=4</Item>
  </Grid>
  <Grid item xs={12} sm={6} md={4}>
    <Item>xs=12 sm=6 md=4</Item>
  </Grid>
  <Grid item xs={12} sm={12} md={4}>
    <Item>xs=12 sm=12 md=4</Item>
  </Grid>
</Grid>
```

### Stack

```tsx
import Stack from '@mui/material/Stack';

<Stack direction="row" spacing={2}>
  <Item>Item 1</Item>
  <Item>Item 2</Item>
  <Item>Item 3</Item>
</Stack>

<Stack
  direction={{ xs: 'column', sm: 'row' }}
  spacing={{ xs: 1, sm: 2, md: 4 }}
  justifyContent="center"
  alignItems="center"
>
  <Item>Item 1</Item>
  <Item>Item 2</Item>
</Stack>
```

## Forms with React Hook Form

```tsx
import { useForm, Controller } from 'react-hook-form';
import { TextField, Button, Box } from '@mui/material';

function Form() {
  const { control, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
      <Controller
        name="email"
        control={control}
        defaultValue=""
        rules={{
          required: 'Email is required',
          pattern: {
            value: /^\S+@\S+$/i,
            message: 'Invalid email',
          },
        }}
        render={({ field }) => (
          <TextField
            {...field}
            label="Email"
            fullWidth
            error={!!errors.email}
            helperText={errors.email?.message}
            margin="normal"
          />
        )}
      />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3 }}>
        Submit
      </Button>
    </Box>
  );
}
```

## Best Practices

1. **Use sx prop** - Cleaner than inline styles, theme-aware
2. **ThemeProvider at root** - Ensures consistent theming
3. **CssBaseline** - Normalize styles across browsers
4. **Component overrides** - Customize via theme.components
5. **Responsive breakpoints** - Use theme.breakpoints helpers

## Reference Files

- [references/components.md](references/components.md) - Complete component list
- [references/theming.md](references/theming.md) - Advanced theming patterns
