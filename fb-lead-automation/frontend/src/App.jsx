import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AdsPage from './pages/AdsPage';
import MessagesPage from './pages/MessagesPage';
import LeadsPage from './pages/LeadsPage';
import { MessageSquare, Users, Smartphone } from 'lucide-react';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          {/* Navigation Bar */}
          <nav className="bg-white border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center gap-8">
                  <div className="flex items-center gap-2">
                    <div className="p-2 bg-blue-600 rounded-lg">
                      <Smartphone className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-bold text-gray-900">
                      FB Lead Automation
                    </span>
                  </div>
                  <div className="flex gap-4">
                    <NavLink to="/ads" icon={<MessageSquare className="w-4 h-4" />}>
                      Ads
                    </NavLink>
                    <NavLink to="/leads" icon={<Users className="w-4 h-4" />}>
                      Leads
                    </NavLink>
                  </div>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <Routes>
            <Route path="/" element={<Navigate to="/ads" replace />} />
            <Route path="/ads" element={<AdsPage />} />
            <Route path="/messages/edit" element={<MessagesPage />} />
            <Route path="/leads" element={<LeadsPage />} />
          </Routes>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

// NavLink Component
function NavLink({ to, icon, children }) {
  return (
    <Link
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-2 px-3 py-2 rounded-lg transition ${
          window.location.pathname === to
            ? 'bg-blue-50 text-blue-700 font-medium'
            : 'text-gray-700 hover:bg-gray-100'
        }`
      }
    >
      {icon}
      {children}
    </Link>
  );
}

export default App;
