---
name: Error Boundaries in React
description: Implementing error boundaries for graceful error handling and improved user experience in React applications.
---

# Error Boundaries in React

## Overview

Error Boundaries are React components that catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI instead of crashing the entire application. They catch errors during rendering, in lifecycle methods, and in constructors of the whole tree below them.

## What are Error Boundaries

Error Boundaries are a React feature introduced in React 16 that allows you to:

1. **Catch errors** in component trees
2. **Display fallback UI** when errors occur
3. **Log errors** for debugging
4. **Recover from errors** gracefully

**What Error Boundaries DO Catch:**
- Rendering errors
- Errors in lifecycle methods
- Errors in constructors

**What Error Boundaries DO NOT Catch:**
- Event handlers
- Asynchronous code (setTimeout, promises)
- Server-side rendering errors
- Errors thrown in error boundary itself

## componentDidCatch and getDerivedStateFromError

### getDerivedStateFromError

Used to update state in response to an error. Called during render phase.

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    // Update state so the next render shows the fallback UI
    return { hasError: true, error };
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### componentDidCatch

Called after an error has been thrown by a descendant component. Used for side effects like logging.

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null, errorInfo: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log the error to an error reporting service
    logErrorToService(error, errorInfo);
    
    // Store error info for display
    this.setState({ errorInfo });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI error={this.state.error} info={this.state.errorInfo} />;
    }
    return this.props.children;
  }
}

function logErrorToService(error, errorInfo) {
  // Send to Sentry, LogRocket, etc.
  Sentry.captureException(error, {
    contexts: {
      react: {
        componentStack: errorInfo.componentStack,
      },
    },
  });
}
```

### Complete Example

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  
  static getDerivedStateFromError(error) {
    // Update state to render fallback UI
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log error details
    console.error('Error caught by boundary:', error, errorInfo);
    
    // Send to error tracking service
    this.logError(error, errorInfo);
    
    // Store error info
    this.setState({
      error,
      errorInfo,
    });
  }
  
  logError(error, errorInfo) {
    // Example: Send to Sentry
    if (typeof Sentry !== 'undefined') {
      Sentry.withScope((scope) => {
        scope.setExtra('componentStack', errorInfo.componentStack);
        Sentry.captureException(error);
      });
    }
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback({
        error: this.state.error,
        errorInfo: this.state.errorInfo,
        resetError: this.resetError.bind(this),
      });
    }
    
    return this.props.children;
  }
  
  resetError() {
    this.setState({ hasError: false, error: null, errorInfo: null });
  }
}

// Usage
<ErrorBoundary
  fallback={({ error, resetError }) => (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error?.message}</p>
      <button onClick={resetError}>Try Again</button>
    </div>
  )}
>
  <MyComponent />
</ErrorBoundary>
```

## Error Boundary Limitations

### What Error Boundaries Don't Catch

```jsx
class MyComponent extends React.Component {
  handleClick() {
    // Event handlers are NOT caught
    try {
      throw new Error('Event handler error');
    } catch (error) {
      // Must handle manually
      console.error(error);
    }
  }
  
  async componentDidMount() {
    // Async errors are NOT caught
    try {
      const data = await fetchData();  // Error here won't be caught
    } catch (error) {
      // Must handle manually
      console.error(error);
    }
    
    // setTimeout errors are NOT caught
    setTimeout(() => {
      throw new Error('Timeout error');  // Won't be caught
    }, 1000);
  }
  
  render() {
    return <button onClick={this.handleClick}>Click me</button>;
  }
}
```

### Handling Non-Catchable Errors

```jsx
// For async errors, wrap in try-catch
class MyComponent extends React.Component {
  state = { data: null, error: null };
  
  async componentDidMount() {
    try {
      const data = await fetchData();
      this.setState({ data });
    } catch (error) {
      this.setState({ error });
      // Log error
      logError(error);
    }
  }
  
  render() {
    if (this.state.error) {
      return <ErrorUI error={this.state.error} />;
    }
    if (!this.state.data) {
      return <LoadingUI />;
    }
    return <DataUI data={this.state.data} />;
  }
}
```

## Placement Strategies

### Granular vs Global

**Granular (Feature-Level):**

```jsx
function App() {
  return (
    <div>
      <ErrorBoundary fallback={<ProfileError />}>
        <ProfileSection />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<FeedError />}>
        <FeedSection />
      </ErrorBoundary>
      
      <ErrorBoundary fallback={<SettingsError />}>
        <SettingsSection />
      </ErrorBoundary>
    </div>
  );
}
```

**Global (App-Level):**

```jsx
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}
```

### Hybrid Approach

```jsx
function App() {
  return (
    // Global boundary for catastrophic errors
    <ErrorBoundary fallback={<GlobalError />}>
      <div className="app-layout">
        <Header />
        
        <main>
          {/* Feature-specific boundaries */}
          <ErrorBoundary fallback={<DashboardError />}>
            <Dashboard />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ProjectsError />}>
            <Projects />
          </ErrorBoundary>
        </main>
        
        <Footer />
      </div>
    </ErrorBoundary>
  );
}
```

## Fallback UI Patterns

### Simple Fallback

```jsx
function SimpleFallback({ error, resetError }) {
  return (
    <div className="error-boundary">
      <h2>Something went wrong</h2>
      <p>We're sorry for the inconvenience.</p>
      {error && <p className="error-message">{error.message}</p>}
      <button onClick={resetError}>Try Again</button>
    </div>
  );
}
```

### Detailed Fallback

```jsx
function DetailedFallback({ error, errorInfo, resetError }) {
  return (
    <div className="error-boundary detailed">
      <div className="error-icon">⚠️</div>
      <h2>Oops! Something went wrong</h2>
      
      <div className="error-details">
        <h3>Error Message</h3>
        <p>{error?.message || 'Unknown error'}</p>
        
        {errorInfo && (
          <details>
            <summary>Technical Details</summary>
            <pre>{errorInfo.componentStack}</pre>
          </details>
        )}
      </div>
      
      <div className="error-actions">
        <button onClick={resetError} className="btn-primary">
          Try Again
        </button>
        <button onClick={() => window.location.href = '/'} className="btn-secondary">
          Go Home
        </button>
        <button onClick={() => window.location.reload()} className="btn-tertiary">
          Reload Page
        </button>
      </div>
      
      <p className="error-contact">
        Need help? <a href="/support">Contact Support</a>
      </p>
    </div>
  );
}
```

### Themed Fallback

```jsx
function ThemedFallback({ error, resetError }) {
  const theme = useTheme();
  
  return (
    <div className={`error-boundary ${theme}`}>
      <div className="error-container">
        <div className="error-illustration">
          {theme === 'dark' ? (
            <DarkErrorIllustration />
          ) : (
            <LightErrorIllustration />
          )}
        </div>
        
        <h2>Something went wrong</h2>
        <p>{error?.message}</p>
        
        <button onClick={resetError} className="btn">
          Try Again
        </button>
      </div>
    </div>
  );
}
```

## Error Reporting Integration

### Sentry Integration

```jsx
import * as Sentry from '@sentry/react';

class SentryErrorBoundary extends React.Component {
  state = { eventId: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    // Send error to Sentry
    Sentry.withScope((scope) => {
      scope.setExtra('componentStack', errorInfo.componentStack);
      scope.setTag('errorBoundary', 'true');
      
      const eventId = Sentry.captureException(error);
      this.setState({ eventId });
    });
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <FallbackUI
          eventId={this.state.eventId}
          resetError={() => window.location.reload()}
        />
      );
    }
    
    return this.props.children;
  }
}

// Initialize Sentry
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: process.env.APP_VERSION,
});
```

### LogRocket Integration

```jsx
import LogRocket from 'logrocket';

class LogRocketErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    // Log error to LogRocket
    LogRocket.captureException(error, {
      tags: {
        errorBoundary: 'true',
      },
      extra: {
        componentStack: errorInfo.componentStack,
      },
    });
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}

// Initialize LogRocket
LogRocket.init('YOUR_APP_ID', {
  release: process.env.APP_VERSION,
  console: {
    isEnabled: process.env.NODE_ENV === 'development',
  },
});
```

### Custom Error Service

```jsx
class ErrorReportingService {
  static async report(error, errorInfo) {
    const payload = {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo?.componentStack,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    };
    
    try {
      await fetch('/api/errors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch (reportError) {
      console.error('Failed to report error:', reportError);
    }
  }
}

class ReportingErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    ErrorReportingService.report(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

## Retry Mechanisms

### Simple Retry

```jsx
function RetryableComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  
  const handleRetry = () => {
    setError(null);
    setRetryCount(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          <button onClick={handleRetry}>
            Retry ({retryCount})
          </button>
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

### Exponential Backoff Retry

```jsx
function ExponentialRetryComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const [isRetrying, setIsRetrying] = useState(false);
  
  const handleRetry = async () => {
    setIsRetrying(true);
    setError(null);
    
    // Exponential backoff
    const delay = Math.min(1000 * Math.pow(2, retryCount), 30000);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    setRetryCount(prev => prev + 1);
    setIsRetrying(false);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          {isRetrying ? (
            <button disabled>Retrying...</button>
          ) : (
            <button onClick={handleRetry}>
              Retry ({retryCount})
            </button>
          )}
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

### Smart Retry

```jsx
function SmartRetryComponent() {
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;
  
  const shouldRetry = error => {
    // Only retry on specific errors
    const retryableErrors = [
      'NetworkError',
      'TimeoutError',
      'ServiceUnavailable',
    ];
    return retryableErrors.some(type => error?.name?.includes(type));
  };
  
  const handleRetry = () => {
    setError(null);
    setRetryCount(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          
          {shouldRetry(error) && retryCount < maxRetries ? (
            <button onClick={handleRetry}>
              Retry ({retryCount}/{maxRetries})
            </button>
          ) : (
            <p>Please try again later or contact support.</p>
          )}
        </div>
      }
      onError={setError}
    >
      <ChildComponent key={retryCount} />
    </ErrorBoundary>
  );
}
```

## Error Boundaries with React Query/SWR

### React Query Error Boundaries

```jsx
import { useQuery, QueryErrorResetBoundary } from '@tanstack/react-query';

function UserProfile() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['user', 'profile'],
    queryFn: fetchUserProfile,
    retry: 3,
  });
  
  if (isLoading) return <Loading />;
  if (error) return <ErrorUI error={error} />;
  
  return <Profile data={data} />;
}

// With Error Boundary
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <QueryErrorResetBoundary>
        <UserProfile />
      </QueryErrorResetBoundary>
    </ErrorBoundary>
  );
}
```

### SWR Error Boundaries

```jsx
import useSWR from 'swr';

function UserProfile() {
  const { data, error, isLoading } = useSWR('/api/user/profile', fetcher);
  
  if (isLoading) return <Loading />;
  if (error) return <ErrorUI error={error} />;
  
  return <Profile data={data} />;
}

// With Error Boundary
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <SWRConfig value={{ onError: handleError }}>
        <UserProfile />
      </SWRConfig>
    </ErrorBoundary>
  );
}

function handleError(error) {
  // Log error
  console.error('SWR Error:', error);
  
  // Show notification
  toast.error('Failed to load data');
}
```

### Combined Approach

```jsx
function DataComponent() {
  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ['data'],
    queryFn: fetchData,
  });
  
  if (isLoading) return <Loading />;
  
  if (error) {
    // Let error boundary handle it
    throw error;
  }
  
  return <DataView data={data} />;
}

function App() {
  return (
    <ErrorBoundary
      fallback={
        <ErrorFallback
          onRetry={() => window.location.reload()}
        />
      }
    >
      <DataComponent />
    </ErrorBoundary>
  );
}
```

## Error Boundaries with Suspense

### Suspense + Error Boundary Pattern

```jsx
import { Suspense } from 'react';

function ResourceComponent() {
  const resource = useResource(resourcePromise);
  
  if (resource.status === 'pending') {
    throw resource.promise;  // Suspense catches this
  }
  
  if (resource.status === 'rejected') {
    throw resource.reason;  // Error Boundary catches this
  }
  
  return <DataView data={resource.result} />;
}

function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <Suspense fallback={<Loading />}>
        <ResourceComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Multiple Suspense Boundaries

```jsx
function App() {
  return (
    <ErrorBoundary fallback={<GlobalError />}>
      <Suspense fallback={<PageLoading />}>
        <Header />
        <main>
          <ErrorBoundary fallback={<ContentError />}>
            <Suspense fallback={<SectionLoading />}>
              <Dashboard />
            </Suspense>
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ContentError />}>
            <Suspense fallback={<SectionLoading />}>
              <Feed />
            </Suspense>
          </ErrorBoundary>
        </main>
        <Footer />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Error Boundaries in Server Components (Next.js)

### Next.js App Router

```jsx
// app/error.js
'use client';

export default function Error({
  error,
  reset,
}) {
  return (
    <div className="error-page">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// app/global-error.js
'use client';

export default function GlobalError({ error }) {
  return (
    <html>
      <body>
        <div className="global-error">
          <h2>Application Error</h2>
          <p>{error.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Application
          </button>
        </div>
      </body>
    </html>
  );
}
```

### Next.js Pages Router

```jsx
// pages/_error.js
class ErrorPage extends React.Component {
  static getInitialProps({ res, err }) {
    const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
    return { statusCode };
  }
  
  render() {
    const { statusCode } = this.props;
    
    return (
      <div className="error-page">
        <h1>{statusCode}</h1>
        <p>Something went wrong</p>
        <Link href="/">Go Home</Link>
      </div>
    );
  }
}

export default ErrorPage;
```

### Component-Level Error Boundary

```jsx
'use client';

class ComponentErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Error in component:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// Usage in Next.js component
export default function MyComponent() {
  return (
    <ComponentErrorBoundary>
      <Content />
    </ComponentErrorBoundary>
  );
}
```

## react-error-boundary Library

### Installation

```bash
npm install react-error-boundary
```

### Basic Usage

```jsx
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={(error, errorInfo) => {
        console.error('Error:', error, errorInfo);
      }}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary}>
        Try Again
      </button>
    </div>
  );
}
```

### withErrorBoundary HOC

```jsx
import { withErrorBoundary } from 'react-error-boundary';

class MyComponent extends React.Component {
  render() {
    return <div>{this.props.children}</div>;
  }
}

export default withErrorBoundary(MyComponent);

// Or with custom fallback
export default withErrorBoundary(MyComponent, {
  FallbackComponent: CustomFallback,
  onError: (error, errorInfo) => {
    logError(error, errorInfo);
  },
});
```

### ErrorBoundaryType

```jsx
import { ErrorBoundary, ErrorBoundaryType } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary
      type={ErrorBoundaryType.Component}
      FallbackComponent={ComponentFallback}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}

function ComponentFallback({ error, resetErrorBoundary }) {
  return <div>Component error: {error.message}</div>;
}
```

## Testing Error Boundaries

### Unit Testing

```jsx
import { render, screen } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary';

describe('ErrorBoundary', () => {
  it('catches errors and renders fallback', () => {
    const ThrowError = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <ThrowError />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Error occurred')).toBeInTheDocument();
  });
  
  it('calls onError callback', () => {
    const onError = jest.fn();
    const ThrowError = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />} onError={onError}>
        <ThrowError />
      </ErrorBoundary>
    );
    
    expect(onError).toHaveBeenCalled();
    expect(onError.mock.calls[0][0]).toBeInstanceOf(Error);
  });
});
```

### Testing with React Testing Library

```jsx
import { render, screen } from '@testing-library/react';

describe('ErrorBoundary Integration', () => {
  it('renders fallback when child throws error', () => {
    const ThrowComponent = () => {
      throw new Error('Test error');
    };
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <ThrowComponent />
      </ErrorBoundary>
    );
    
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });
  
  it('renders children when no error', () => {
    const SafeComponent = () => <div>Safe content</div>;
    
    render(
      <ErrorBoundary fallback={<FallbackUI />}>
        <SafeComponent />
      </ErrorBoundary>
    );
    
    expect(screen.getByText('Safe content')).toBeInTheDocument();
  });
});
```

## Error Boundary Composition

### Nested Boundaries

```jsx
function App() {
  return (
    // Global boundary
    <ErrorBoundary fallback={<GlobalFallback />}>
      <div className="app">
        <Header />
        
        <main>
          {/* Feature boundaries */}
          <ErrorBoundary fallback={<DashboardFallback />}>
            <Dashboard />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<ProjectsFallback />}>
            <Projects />
          </ErrorBoundary>
          
          <ErrorBoundary fallback={<SettingsFallback />}>
            <Settings />
          </ErrorBoundary>
        </main>
        
        <Footer />
      </div>
    </ErrorBoundary>
  );
}
```

### Boundary Hierarchy

```jsx
// Outer boundary catches everything
<ErrorBoundary fallback={<AppFallback />}>
  <AppLayout>
    {/* Inner boundaries for specific features */}
    <ErrorBoundary fallback={<DashboardFallback />}>
      <Dashboard />
    </ErrorBoundary>
    
    <ErrorBoundary fallback={<ProjectsFallback />}>
      <Projects />
    </ErrorBoundary>
  </AppLayout>
</ErrorBoundary>
```

## Recovering from Errors

### State Reset

```jsx
class RecoverableErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log error
    logError(error, errorInfo);
  }
  
  resetError = () => {
    this.setState({ hasError: false, error: null });
  };
  
  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback
          error={this.state.error}
          onReset={this.resetError}
        />
      );
    }
    return this.props.children;
  }
}
```

### Route Reset

```jsx
function ErrorFallback({ error, onReset }) {
  const navigate = useNavigate();
  
  const handleReset = () => {
    // Reset to home or previous route
    navigate('/');
    onReset();
  };
  
  return (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error?.message}</p>
      <button onClick={handleReset}>Go Home</button>
    </div>
  );
}
```

### Data Refresh

```jsx
function RefreshableErrorBoundary({ children, fallback }) {
  const [error, setError] = useState(null);
  const [retryKey, setRetryKey] = useState(0);
  
  const handleRefresh = () => {
    setError(null);
    setRetryKey(prev => prev + 1);
  };
  
  return (
    <ErrorBoundary
      fallback={
        <div className="error-fallback">
          <h2>Error occurred</h2>
          <p>{error?.message}</p>
          <button onClick={handleRefresh}>Refresh</button>
        </div>
      }
      onError={setError}
    >
      <React.Fragment key={retryKey}>
        {children}
      </React.Fragment>
    </ErrorBoundary>
  );
}
```

## User-Friendly Error Messages

### Contextual Messages

```jsx
function ContextualFallback({ error, component }) {
  const getErrorMessage = () => {
    switch (component) {
      case 'Dashboard':
        return 'We couldn\'t load your dashboard. Please try again.';
      case 'Profile':
        return 'We couldn\'t load your profile. Please try again.';
      case 'Settings':
        return 'We couldn\'t save your settings. Please try again.';
      default:
        return 'Something went wrong. Please try again.';
    }
  };
  
  return (
    <div className="error-fallback">
      <h2>Oops!</h2>
      <p>{getErrorMessage()}</p>
      {error?.message && (
        <details>
          <summary>Technical details</summary>
          <p>{error.message}</p>
        </details>
      )}
    </div>
  );
}
```

### Action-Oriented Messages

```jsx
function ActionFallback({ error, onRetry, onGoHome, onContact }) {
  return (
    <div className="error-fallback">
      <div className="error-icon">⚠️</div>
      <h2>Something went wrong</h2>
      <p>We're sorry for the inconvenience.</p>
      
      <div className="error-actions">
        <button onClick={onRetry} className="btn-primary">
          Try Again
        </button>
        <button onClick={onGoHome} className="btn-secondary">
          Go Home
        </button>
        <button onClick={onContact} className="btn-tertiary">
          Contact Support
        </button>
      </div>
    </div>
  );
}
```

## Error Boundary Best Practices

1. **Placement Strategy**
   - Use global boundary for catastrophic errors
   - Use feature-level boundaries for better UX
   - Place boundaries at logical component boundaries
   - Consider nested boundaries for complex apps

2. **Fallback Design**
   - Provide clear, actionable error messages
   - Include retry mechanisms
   - Offer alternative actions (go home, contact support)
   - Match your app's design language

3. **Error Reporting**
   - Integrate with error tracking services (Sentry, LogRocket)
   - Include context (component stack, user info)
   - Log errors for debugging
   - Set up alerts for critical errors

4. **Recovery Strategies**
   - Implement reset mechanisms
   - Provide data refresh options
   - Consider navigation resets
   - Allow graceful degradation

5. **Testing**
   - Test error boundary with intentional errors
   - Verify fallback UI renders correctly
   - Test error reporting integration
   - Verify recovery mechanisms work

## Common Patterns

### Page-Level Boundaries

```jsx
function PageWrapper({ children, pageName }) {
  return (
    <ErrorBoundary
      fallback={<PageFallback pageName={pageName} />}
      onError={(error) => logPageError(pageName, error)}
    >
      {children}
    </ErrorBoundary>
  );
}

// Usage
<PageWrapper pageName="Dashboard">
  <Dashboard />
</PageWrapper>
```

### Component-Level Boundaries

```jsx
function ComponentWrapper({ children, componentName }) {
  return (
    <ErrorBoundary
      fallback={<ComponentFallback componentName={componentName} />}
      onError={(error) => logComponentError(componentName, error)}
    >
      {children}
    </ErrorBoundary>
  );
}

// Usage
<ComponentWrapper componentName="UserProfile">
  <UserProfile />
</ComponentWrapper>
```

### Feature-Level Boundaries

```jsx
function FeatureWrapper({ children, featureName }) {
  return (
    <ErrorBoundary
      fallback={<FeatureFallback featureName={featureName} />}
      onError={(error) => logFeatureError(featureName, error)}
    >
      <Suspense fallback={<FeatureLoading featureName={featureName} />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

// Usage
<FeatureWrapper featureName="Dashboard">
  <Dashboard />
</FeatureWrapper>
```

## Monitoring and Alerting

### Error Rate Monitoring

```jsx
class ErrorRateMonitor {
  constructor() {
    this.errors = [];
    this.startTime = Date.now();
    this.threshold = 10;  // 10 errors per minute
  }
  
  recordError(error) {
    const now = Date.now();
    this.errors.push({ error, timestamp: now });
    
    // Clean old errors (older than 1 minute)
    this.errors = this.errors.filter(e => now - e.timestamp < 60000);
    
    // Check threshold
    if (this.errors.length >= this.threshold) {
      this.alertHighErrorRate();
    }
  }
  
  alertHighErrorRate() {
    console.error('High error rate detected!');
    // Send alert to monitoring service
    sendAlert('High error rate', {
      count: this.errors.length,
      duration: Date.now() - this.startTime,
    });
  }
}

const monitor = new ErrorRateMonitor();

class MonitoredErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    monitor.recordError(error);
    logError(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

## Related Skills

- `02-frontend/react-patterns`
- `02-frontend/nextjs-guide`
- `14-monitoring-observability/error-tracking`
