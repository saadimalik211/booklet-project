# Frontend – React + Tailwind CSS Architecture

## Overview
Modern web interface built with React and Tailwind CSS for managing customers, books, pages, and triggering PDF generation. Provides an intuitive workflow from setup to download.

- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS (utility-first)
- **State Management**: React Context + hooks (or Zustand for complex state)
- **HTTP Client**: Axios or fetch with React Query/SWR
- **Build Tool**: Vite or Create React App
- **Deployment**: Static hosting (Vercel, Netlify, or containerized)

---

## Technology Stack

### React
- **Component-based architecture** for reusable UI elements
- **JSX** for declarative UI development
- **Hooks** for state management and side effects
- **Context API** for global state (auth, theme)
- **TypeScript** for type safety and better DX

### Tailwind CSS
- **Utility-first approach** - no custom CSS needed
- **Responsive design** built-in with mobile-first approach
- **Design system** with consistent spacing, colors, typography
- **Purge unused styles** for optimal bundle size
- **Dark mode support** (optional)

### Additional Libraries
- **React Router** for navigation and routing
- **React Hook Form** for form handling and validation
- **React Query/SWR** for server state management
- **Axios** for HTTP requests
- **React Dropzone** for file uploads
- **React Hot Toast** for notifications

---

## Core Components

### Layout Components
```tsx
// App.tsx - Main application wrapper
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/books" element={<Books />} />
              <Route path="/generate" element={<GenerateBook />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

// Header.tsx - Navigation and user menu
function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-900">PDF Booklet Maker</h1>
        <nav className="flex space-x-6">
          <Link to="/" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
          <Link to="/customers" className="text-gray-600 hover:text-gray-900">Customers</Link>
          <Link to="/books" className="text-gray-600 hover:text-gray-900">Books</Link>
          <Link to="/generate" className="text-gray-600 hover:text-gray-900">Generate</Link>
        </nav>
      </div>
    </header>
  );
}
```

### Form Components
```tsx
// CustomerForm.tsx - Create/edit customer
function CustomerForm({ customer, onSubmit }) {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: customer
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Name</label>
        <input
          {...register("name", { required: "Name is required" })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          {...register("email", { 
            required: "Email is required",
            pattern: { value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/, message: "Invalid email" }
          })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
      >
        {customer ? 'Update Customer' : 'Create Customer'}
      </button>
    </form>
  );
}
```

### File Upload Components
```tsx
// FileUpload.tsx - Drag and drop file upload
function FileUpload({ onFileSelect, accept, maxSize = 10 * 1024 * 1024 }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: onFileSelect,
    accept: accept,
    maxSize: maxSize,
    multiple: false
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
        isDragActive 
          ? 'border-blue-400 bg-blue-50' 
          : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input {...getInputProps()} />
      <div className="space-y-2">
        <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none">
          <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p className="text-gray-600">
          {isDragActive ? 'Drop files here' : 'Drag & drop files here, or click to select'}
        </p>
        <p className="text-sm text-gray-500">
          Max size: {Math.round(maxSize / 1024 / 1024)}MB
        </p>
      </div>
    </div>
  );
}
```

### Book Generation Components
```tsx
// GenerateBook.tsx - Main generation workflow
function GenerateBook() {
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [selectedBook, setSelectedBook] = useState(null);
  const [spreadsheet, setSpreadsheet] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);

  const { data: customers } = useQuery(['customers'], fetchCustomers);
  const { data: books } = useQuery(['books'], fetchBooks);
  const { mutate: generateBook, isLoading } = useMutation(generateBookAPI);

  const handleGenerate = () => {
    const formData = new FormData();
    formData.append('customer_id', selectedCustomer.id);
    formData.append('book_id', selectedBook.id);
    if (spreadsheet) {
      formData.append('spreadsheet', spreadsheet);
    }

    generateBook(formData, {
      onSuccess: (data) => {
        setJobId(data.job_id);
        toast.success('Book generation started!');
      },
      onError: () => {
        toast.error('Failed to start generation');
      }
    });
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Generate PDF Book</h2>
        
        {/* Customer Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Customer
          </label>
          <select
            value={selectedCustomer?.id || ''}
            onChange={(e) => setSelectedCustomer(customers?.find(c => c.id === e.target.value))}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="">Choose a customer...</option>
            {customers?.map(customer => (
              <option key={customer.id} value={customer.id}>
                {customer.name}
              </option>
            ))}
          </select>
        </div>

        {/* Book Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Book Template
          </label>
          <select
            value={selectedBook?.id || ''}
            onChange={(e) => setSelectedBook(books?.find(b => b.id === e.target.value))}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="">Choose a book template...</option>
            {books?.map(book => (
              <option key={book.id} value={book.id}>
                {book.name}
              </option>
            ))}
          </select>
        </div>

        {/* Spreadsheet Upload (if needed) */}
        {selectedBook?.hasExcelPages && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Spreadsheet
            </label>
            <FileUpload
              onFileSelect={(files) => setSpreadsheet(files[0])}
              accept={{ 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'] }}
            />
          </div>
        )}

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          disabled={!selectedCustomer || !selectedBook || isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium py-3 px-4 rounded-md transition duration-200"
        >
          {isLoading ? 'Generating...' : 'Generate PDF Book'}
        </button>
      </div>

      {/* Job Status */}
      {jobId && <JobStatus jobId={jobId} />}
    </div>
  );
}

// JobStatus.tsx - Monitor generation progress
function JobStatus({ jobId }) {
  const { data: job } = useQuery(
    ['job', jobId],
    () => fetchJobStatus(jobId),
    { refetchInterval: 2000 }
  );

  if (!job) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Generation Status</h3>
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Status:</span>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            job.status === 'done' ? 'bg-green-100 text-green-800' :
            job.status === 'error' ? 'bg-red-100 text-red-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {job.status}
          </span>
        </div>

        {job.status === 'done' && job.output_file_id && (
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Download:</span>
            <a
              href={`/api/downloads/${job.output_file_id}`}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
            >
              Download PDF
            </a>
          </div>
        )}

        {job.status === 'error' && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-800">{job.error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## State Management

### Global State (Context)
```tsx
// AuthContext.tsx
const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (credentials) => {
    const response = await api.post('/auth/login', credentials);
    setUser(response.data.user);
    localStorage.setItem('token', response.data.access_token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// useAuth hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### Server State (React Query)
```tsx
// api.ts - API client setup
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// hooks/useCustomers.ts
export function useCustomers() {
  return useQuery(['customers'], () => 
    api.get('/customers').then(res => res.data)
  );
}

export function useCreateCustomer() {
  const queryClient = useQueryClient();
  
  return useMutation(
    (customerData) => api.post('/customers', customerData).then(res => res.data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['customers']);
        toast.success('Customer created successfully!');
      },
      onError: () => {
        toast.error('Failed to create customer');
      }
    }
  );
}
```

---

## UI Patterns & Design System

### Color Palette
```css
/* Tailwind config colors */
colors: {
  primary: {
    50: '#eff6ff',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
  },
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    500: '#6b7280',
    700: '#374151',
    900: '#111827',
  },
  success: {
    50: '#f0fdf4',
    500: '#22c55e',
    600: '#16a34a',
  },
  error: {
    50: '#fef2f2',
    500: '#ef4444',
    600: '#dc2626',
  }
}
```

### Component Variants
```tsx
// Button variants
const buttonVariants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white",
  secondary: "bg-gray-200 hover:bg-gray-300 text-gray-900",
  danger: "bg-red-600 hover:bg-red-700 text-white",
  success: "bg-green-600 hover:bg-green-700 text-white",
};

// Card component
function Card({ children, className = "" }) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-6 ${className}`}>
      {children}
    </div>
  );
}

// Badge component
function Badge({ variant = "default", children }) {
  const variants = {
    default: "bg-gray-100 text-gray-800",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    error: "bg-red-100 text-red-800",
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[variant]}`}>
      {children}
    </span>
  );
}
```

---

## Development Setup

### Project Structure
```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Layout.tsx
│   ├── forms/
│   │   ├── CustomerForm.tsx
│   │   ├── BookForm.tsx
│   │   └── PageForm.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   └── FileUpload.tsx
│   └── features/
│       ├── customers/
│       ├── books/
│       └── generation/
├── hooks/
│   ├── useAuth.ts
│   ├── useCustomers.ts
│   └── useBooks.ts
├── services/
│   └── api.ts
├── context/
│   └── AuthContext.tsx
├── types/
│   └── index.ts
└── utils/
    └── helpers.ts
```

### Package.json Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "react-query": "^3.39.0",
    "react-hook-form": "^7.43.0",
    "react-dropzone": "^14.2.0",
    "axios": "^1.3.0",
    "react-hot-toast": "^2.4.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "@vitejs/plugin-react": "^3.1.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.2.0",
    "typescript": "^4.9.0",
    "vite": "^4.1.0"
  }
}
```

### Tailwind Configuration
```js
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
```

---

## Integration with Backend

### API Integration Points
- **Authentication**: JWT tokens with automatic refresh
- **File Uploads**: Multipart form data with progress tracking
- **Real-time Updates**: Polling for job status updates
- **Error Handling**: Consistent error messages and retry logic

### Environment Configuration
```env
# .env.local
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENVIRONMENT=development
```

### CORS Configuration
Backend must allow requests from frontend origin:
```python
# FastAPI CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance & Optimization

### Code Splitting
```tsx
// Lazy load routes
const Customers = lazy(() => import('./pages/Customers'));
const Books = lazy(() => import('./pages/Books'));

// Suspense wrapper
<Suspense fallback={<LoadingSpinner />}>
  <Route path="/customers" element={<Customers />} />
</Suspense>
```

### Bundle Optimization
- Tree shaking for unused code
- Tailwind CSS purging
- Image optimization and lazy loading
- Service worker for caching (optional)

### React Query Optimizations
```tsx
// Optimistic updates
const updateCustomer = useMutation(
  (customerData) => api.put(`/customers/${customerData.id}`, customerData),
  {
    onMutate: async (newCustomer) => {
      await queryClient.cancelQueries(['customers']);
      const previousCustomers = queryClient.getQueryData(['customers']);
      queryClient.setQueryData(['customers'], old => 
        old.map(c => c.id === newCustomer.id ? newCustomer : c)
      );
      return { previousCustomers };
    },
    onError: (err, newCustomer, context) => {
      queryClient.setQueryData(['customers'], context.previousCustomers);
    },
    onSettled: () => {
      queryClient.invalidateQueries(['customers']);
    },
  }
);
```

---

## Testing Strategy

### Unit Tests (Jest + React Testing Library)
```tsx
// CustomerForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CustomerForm } from './CustomerForm';

test('submits form with customer data', async () => {
  const mockOnSubmit = jest.fn();
  render(<CustomerForm onSubmit={mockOnSubmit} />);

  fireEvent.change(screen.getByLabelText(/name/i), {
    target: { value: 'John Doe' },
  });
  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: 'john@example.com' },
  });
  fireEvent.click(screen.getByRole('button', { name: /create customer/i }));

  await waitFor(() => {
    expect(mockOnSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
    });
  });
});
```

### Integration Tests
- API integration testing
- Form submission workflows
- File upload functionality
- Job status monitoring

### E2E Tests (Cypress)
```tsx
// cypress/integration/generate-book.spec.ts
describe('Book Generation', () => {
  it('should generate a PDF book successfully', () => {
    cy.visit('/generate');
    cy.get('[data-testid=customer-select]').select('Test Customer');
    cy.get('[data-testid=book-select]').select('Renewal Book');
    cy.get('[data-testid=generate-button]').click();
    cy.get('[data-testid=job-status]').should('contain', 'done');
    cy.get('[data-testid=download-link]').should('be.visible');
  });
});
```

---

## Deployment

### Build Process
```bash
# Development
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Deployment Options
- **Vercel**: Zero-config deployment with automatic previews
- **Netlify**: Static hosting with form handling
- **Docker**: Containerized deployment
- **CDN**: Static assets served via CDN

### Environment Variables
```bash
# Production environment
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
REACT_APP_SENTRY_DSN=your-sentry-dsn
```

This frontend architecture provides a modern, maintainable, and scalable foundation for the PDF booklet generator application.
