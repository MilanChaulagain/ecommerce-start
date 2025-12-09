'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function AuthCallbackPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Completing authentication...');

  useEffect(() => {
    const success = searchParams.get('success');
    const error = searchParams.get('error');
    const errorMessage = searchParams.get('message');
    const token = searchParams.get('token');

    if (success === 'true' && token) {
      // Store token in localStorage
      localStorage.setItem('jwt_token', token);
      
      setStatus('success');
      setMessage('Login successful! Redirecting...');
      
      // Notify opener window (popup)
      if (window.opener) {
        window.opener.postMessage(
          { type: 'oauth_success', token },
          window.location.origin
        );
        
        // Close popup after a short delay
        setTimeout(() => {
          window.close();
        }, 1000);
      } else {
        // Not a popup, redirect to home
        setTimeout(() => {
          router.push('/');
        }, 2000);
      }
    } else if (error) {
      setStatus('error');
      setMessage(errorMessage || 'Authentication failed. Please try again.');
      
      // Notify opener window
      if (window.opener) {
        window.opener.postMessage(
          { type: 'oauth_error', message: errorMessage || error },
          window.location.origin
        );
        
        setTimeout(() => {
          window.close();
        }, 3000);
      } else {
        setTimeout(() => {
          router.push('/');
        }, 3000);
      }
    }
  }, [searchParams, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
        {status === 'loading' && (
          <>
            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Processing...</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-green-600 mb-2">Success!</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-red-600 mb-2">Error</h2>
            <p className="text-gray-600 mb-4">{message}</p>
            <button
              onClick={() => router.push('/')}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Return Home
            </button>
          </>
        )}
      </div>
    </div>
  );
}
