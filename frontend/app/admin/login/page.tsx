'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, Mail, Eye, EyeOff, Shield } from 'lucide-react';

export default function AdminLogin() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      const response = await fetch(`${apiUrl}/auth/admin/login/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Login failed');
        setLoading(false);
        return;
      }

      // Store token and user data
      localStorage.setItem('admin_token', data.token);
      localStorage.setItem('admin_user', JSON.stringify(data.user));

      // Redirect to dashboard
      router.push('/admin/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      setError('Network error. Please check if the backend is running on port 8000.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Compact Login Card */}
      <div className="w-full max-w-sm">
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          {/* Header */}
          <div className="flex items-center justify-center mb-4">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <Shield className="w-5 h-5 text-white" />
            </div>
          </div>
          <h1 className="text-lg font-bold text-center mb-1  text-purple-900">Admin Portal</h1>
          <p className="text-xs text-gray-500 text-center mb-4">
            Sign in to access the dashboard
          </p>

          {/* Error Message */}
          {error && (
            <div className="mb-3 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-600">
              {error}
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleLogin} className="space-y-3">
            {/* Email Input */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-purple-900" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-9 pr-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent  text-purple-900"
                  placeholder="admin@example.com"
                />
              </div>
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-purple-900" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-9 pr-10 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent  text-purple-900"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-medium rounded-md hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          {/* Back to Home */}
          <div className="mt-4 pt-3 border-t border-gray-200">
            <button
              onClick={() => router.push('/')}
              className="w-full text-xs text-gray-600 hover:text-gray-900 transition-colors"
            >
              ← Back to Home
            </button>
          </div>
        </div>

        {/* Footer Note */}
        <p className="text-center text-xs text-gray-500 mt-4">
          Authorized personnel only. All actions are logged.
        </p>
      </div>
    </div>
  );
}
