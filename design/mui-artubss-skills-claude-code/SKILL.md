---
name: mui
description: Padrões da biblioteca de componentes Material-UI v7 incluindo estilização com sx prop, integração de tema, design responsivo e hooks específicos do MUI. Use ao trabalhar com componentes MUI, estilização com sx prop, personalização de tema ou utilitários MUI.
---

# Padrões MUI v7

## Propósito

Padrões do Material-UI v7 (lançado em março de 2025) para uso de componentes, estilização com sx prop, integração de tema e design responsivo.

**Nota**: Mudanças de quebra do MUI v7 em relação ao v6:
- Deep imports não funcionam mais - use o campo exports do pacote
- `onBackdropClick` removido do Modal - use `onClose` em seu lugar
- Todos os componentes agora usam o padrão padronizado `slots` e `slotProps`
- Suporte a CSS layers via configuração `enableCssLayer` (funciona com Tailwind v4)

## Quando Usar Esta Habilidade

- Estilização de componentes com MUI sx prop
- Uso de componentes MUI (Box, Grid, Paper, Typography, etc.)
- Personalização e uso de tema
- Design responsivo com breakpoints MUI
- Utilitários e hooks específicos do MUI

---

## Início Rápido

### Componente MUI Básico

```typescript
import { Box, Typography, Button, Paper } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

const styles: Record<string, SxProps<Theme>> = {
  container: {
    p: 2,
    display: 'flex',
    flexDirection: 'column',
    gap: 2,
  },
  header: {
    mb: 3,
    fontSize: '1.5rem',
    fontWeight: 600,
  },
};

function MyComponent() {
  return (
    <Paper sx={styles.container}>
      <Typography sx={styles.header}>
        Título
      </Typography>
      <Button variant="contained">
        Ação
      </Button>
    </Paper>
  );
}
```

---

## Padrões de Estilização

### Estilos Inline (< 100 linhas)

Para componentes com estilização simples, defina os estilos no topo:

```typescript
import type { SxProps, Theme } from '@mui/material';

const componentStyles: Record<string, SxProps<Theme>> = {
  container: {
    p: 2,
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    mb: 2,
    color: 'primary.main',
  },
  button: {
    mt: 'auto',
    alignSelf: 'flex-end',
  },
};

function Component() {
  return (
    <Box sx={componentStyles.container}>
      <Typography sx={componentStyles.header}>Cabeçalho</Typography>
      <Button sx={componentStyles.button}>Ação</Button>
    </Box>
  );
}
```

### Arquivo de Estilos Separado (>= 100 linhas)

Para componentes complexos, crie um arquivo de estilos separado:

```typescript
// UserProfile.styles.ts
import type { SxProps, Theme } from '@mui/material';

export const userProfileStyles: Record<string, SxProps<Theme>> = {
  container: {
    p: 3,
    maxWidth: 800,
    mx: 'auto',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    mb: 3,
  },
  // ... muitos mais estilos
};

// UserProfile.tsx
import { userProfileStyles as styles } from './UserProfile.styles';

function UserProfile() {
  return <Box sx={styles.container}>...</Box>;
}
```

---

## Componentes Comuns

### Componentes de Layout

```typescript
// Box - Contêiner genérico
<Box sx={{ p: 2, bgcolor: 'background.paper' }}>
  Conteúdo
</Box>

// Paper - Superfície elevada
<Paper elevation={2} sx={{ p: 3 }}>
  Conteúdo
</Paper>

// Container - Conteúdo centralizado com largura máxima
<Container maxWidth="lg">
  Conteúdo
</Container>

// Stack - Contêiner flex com espaçamento
<Stack spacing={2} direction="row">
  <Item />
  <Item />
</Stack>
```

### Sistema de Grid

```typescript
import { Grid } from '@mui/material';

// Grid de 12 colunas
<Grid container spacing={2}>
  <Grid item xs={12} md={6}>
    Metade esquerda
  </Grid>
  <Grid item xs={12} md={6}>
    Metade direita
  </Grid>
</Grid>

// Grid responsivo
<Grid container spacing={3}>
  <Grid item xs={12} sm={6} md={4} lg={3}>
    Cartão
  </Grid>
  {/* Repita para mais cartões */}
</Grid>
```

### Tipografia

```typescript
<Typography variant="h1">Título 1</Typography>
<Typography variant="h2">Título 2</Typography>
<Typography variant="body1">Texto do corpo</Typography>
<Typography variant="caption">Texto pequeno</Typography>

// Com estilização customizada
<Typography
  variant="h4"
  sx={{
    color: 'primary.main',
    fontWeight: 600,
    mb: 2,
  }}
>
  Título Customizado
</Typography>
```

### Botões

```typescript
// Variantes
<Button variant="contained">Contido</Button>
<Button variant="outlined">Delineado</Button>
<Button variant="text">Texto</Button>

// Cores
<Button variant="contained" color="primary">Primária</Button>
<Button variant="contained" color="secondary">Secundária</Button>
<Button variant="contained" color="error">Erro</Button>

// Com ícones
import { Add as AddIcon } from '@mui/icons-material';

<Button startIcon={<AddIcon />}>Adicionar Item</Button>
```

---

## Integração de Tema

### Usando Valores de Tema

```typescript
import { useTheme } from '@mui/material';

function Component() {
  const theme = useTheme();

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: theme.palette.primary.main,
        color: theme.palette.primary.contrastText,
        borderRadius: theme.shape.borderRadius,
      }}
    >
      Caixa tematizada
    </Box>
  );
}
```

### Tema na Prop sx

```typescript
<Box
  sx={{
    // Acessar tema em sx
    color: 'primary.main',          // theme.palette.primary.main
    bgcolor: 'background.paper',     // theme.palette.background.paper
    p: 2,                            // theme.spacing(2)
    borderRadius: 1,                 // theme.shape.borderRadius
  }}
>
  Conteúdo
</Box>

// Callback para uso avançado
<Box
  sx={(theme) => ({
    color: theme.palette.primary.main,
    '&:hover': {
      color: theme.palette.primary.dark,
    },
  })}
>
  Passe o mouse sobre mim
</Box>
```

---

## Design Responsivo

### Breakpoints

```typescript
// Valores responsivos mobile-first
<Box
  sx={{
    width: {
      xs: '100%',    // 0-600px
      sm: '80%',     // 600-900px
      md: '60%',     // 900-1200px
      lg: '40%',     // 1200-1536px
      xl: '30%',     // 1536px+
    },
  }}
>
  Largura responsiva
</Box>

// Display responsivo
<Box
  sx={{
    display: {
      xs: 'none',    // Oculto em mobile
      md: 'block',   // Visível em desktop
    },
  }}
>
  Apenas desktop
</Box>
```

### Tipografia Responsiva

```typescript
<Typography
  sx={{
    fontSize: {
      xs: '1rem',
      md: '1.5rem',
      lg: '2rem',
    },
    lineHeight: {
      xs: 1.5,
      md: 1.75,
    },
  }}
>
  Texto responsivo
</Typography>
```

---

## Formulários

```typescript
import { TextField, Stack, Button } from '@mui/material';

<Box component="form" onSubmit={handleSubmit}>
  <Stack spacing={2}>
    <TextField
      label="Email"
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      fullWidth
      required
      error={!!errors.email}
      helperText={errors.email}
    />
    <Button type="submit" variant="contained">Enviar</Button>
  </Stack>
</Box>
```

---

## Padrões Comuns

### Componente Card

```typescript
import { Card, CardContent, CardActions, Typography, Button } from '@mui/material';

<Card>
  <CardContent>
    <Typography variant="h5" component="div">
      Título
    </Typography>
    <Typography variant="body2" color="text.secondary">
      Descrição
    </Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Saiba Mais</Button>
  </CardActions>
</Card>
```

### Dialog/Modal

```typescript
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';

<Dialog open={open} onClose={handleClose}>
  <DialogTitle>Confirmar Ação</DialogTitle>
  <DialogContent>
    Tem certeza de que deseja prosseguir?
  </DialogContent>
  <DialogActions>
    <Button onClick={handleClose}>Cancelar</Button>
    <Button onClick={handleConfirm} variant="contained">
      Confirmar
    </Button>
  </DialogActions>
</Dialog>
```

### Estados de Carregamento

```typescript
import { CircularProgress, Skeleton } from '@mui/material';

// Spinner
<Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
  <CircularProgress />
</Box>

// Skeleton
<Stack spacing={1}>
  <Skeleton variant="text" width="60%" />
  <Skeleton variant="rectangular" height={200} />
  <Skeleton variant="text" width="40%" />
</Stack>
```

---

## Hooks Específicos do MUI

### useMuiSnackbar

```typescript
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

function Component() {
  const { showSuccess, showError, showInfo } = useMuiSnackbar();

  const handleSave = async () => {
    try {
      await saveData();
      showSuccess('Salvo com sucesso');
    } catch (error) {
      showError('Falha ao salvar');
    }
  };

  return <Button onClick={handleSave}>Salvar</Button>;
}
```

---

## Ícones

```typescript
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Button, IconButton } from '@mui/material';

<Button startIcon={<AddIcon />}>Adicionar</Button>
<IconButton onClick={handleDelete}><DeleteIcon /></IconButton>
```

---

## Melhores Práticas

### 1. Digite Suas Props sx

```typescript
import type { SxProps, Theme } from '@mui/material';

// ✅ Bom
const styles: Record<string, SxProps<Theme>> = {
  container: { p: 2 },
};

// ❌ Evitar
const styles = {
  container: { p: 2 }, // Sem segurança de tipo
};
```

### 2. Use Tokens de Tema

```typescript
// ✅ Bom: Use tokens de tema
<Box sx={{ color: 'primary.main', p: 2 }} />

// ❌ Evitar: Valores codificados
<Box sx={{ color: '#1976d2', padding: '16px' }} />
```

### 3. Espaçamento Consistente

```typescript
// ✅ Bom: Use escala de espaçamento
<Box sx={{ p: 2, mb: 3, mt: 1 }} />

// ❌ Evitar: Valores de pixel aleatórios
<Box sx={{ padding: '17px', marginBottom: '25px' }} />
```

---

## Recursos Adicionais

Para padrões mais detalhados, veja:
- [styling-guide.md](resources/styling-guide.md) - Padrões de estilização avançada
- [component-library.md](resources/component-library.md) - Exemplos de componentes
- [theme-customization.md](resources/theme-customization.md) - Configuração de tema