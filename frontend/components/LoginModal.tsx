'use client';

import { useState, useEffect, useRef } from 'react';
import { X } from 'lucide-react';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
  buttonRef?: React.RefObject<HTMLButtonElement>;
}

export default function LoginModal({ isOpen, onClose, buttonRef }: LoginModalProps) {
  const [isLoading, setIsLoading] = useState<string | null>(null);
  const modalRef = useRef<HTMLDivElement>(null);

  // Close modal when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSocialLogin = async (provider: 'facebook' | 'instagram' | 'tiktok') => {
    setIsLoading(provider);
    
    try {
      // Get OAuth authorization URL from Django backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/${provider}/authorize/`, {
        method: 'GET',
        credentials: 'include',
      });

      const data = await response.json();
      
      if (data.authorization_url) {
        // Open OAuth provider in popup window
        const width = 600;
        const height = 700;
        const left = window.screen.width / 2 - width / 2;
        const top = window.screen.height / 2 - height / 2;
        
        const popup = window.open(
          data.authorization_url,
          `${provider}_oauth`,
          `width=${width},height=${height},left=${left},top=${top},toolbar=0,scrollbars=1,status=1,resizable=1,location=1,menuBar=0`
        );

        // Listen for OAuth callback
        const checkPopup = setInterval(() => {
          try {
            if (popup && popup.closed) {
              clearInterval(checkPopup);
              setIsLoading(null);
              // Check authentication status
              checkAuthStatus();
            }
          } catch (error) {
            // Handle cross-origin errors
            console.log('Waiting for OAuth callback...');
          }
        }, 500);

        // Listen for message from popup
        const messageHandler = (event: MessageEvent) => {
          if (event.origin !== window.location.origin) return;
          
          if (event.data.type === 'oauth_success') {
            clearInterval(checkPopup);
            if (popup) popup.close();
            setIsLoading(null);
            onClose();
            // Reload or update user state
            window.location.reload();
          } else if (event.data.type === 'oauth_error') {
            clearInterval(checkPopup);
            if (popup) popup.close();
            setIsLoading(null);
            alert(`Login failed: ${event.data.message}`);
          }
        };

        window.addEventListener('message', messageHandler);
        
        // Cleanup
        setTimeout(() => {
          window.removeEventListener('message', messageHandler);
        }, 300000); // 5 minutes timeout
      }
    } catch (error) {
      console.error('OAuth error:', error);
      setIsLoading(null);
      alert('Failed to initialize login. Please try again.');
    }
  };

  const checkAuthStatus = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/user/`, {
        credentials: 'include',
      });
      
      if (response.ok) {
        const userData = await response.json();
        console.log('User authenticated:', userData);
        onClose();
        window.location.reload();
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    }
  };

  return (
    <>
      {/* Dropdown Modal - appears below button */}
      <div className="fixed top-14 right-4 md:right-8 z-50 w-80s">
        <div 
          ref={modalRef}
          className="bg-white rounded-lg shadow-2xl border border-gray-200 animate-fade-in-down"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
              Login
            </h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Social Login Buttons */}
          <div className="p-4 space-y-2">
            {/* Facebook Login */}
            <button
              onClick={() => handleSocialLogin('facebook')}
              disabled={isLoading !== null}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm bg-[#1877F2] hover:bg-[#1664D8] text-white rounded-md font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading === 'facebook' ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              )}
              <span className="text-sm">{isLoading === 'facebook' ? 'Connecting...' : 'Facebook'}</span>
            </button>

            {/* Instagram Login */}
            <button
              onClick={() => handleSocialLogin('instagram')}
              disabled={isLoading !== null}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm bg-gradient-to-r from-[#833AB4] via-[#E1306C] to-[#F56040] hover:opacity-90 text-white rounded-md font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading === 'instagram' ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              )}
              <span className="text-sm">{isLoading === 'instagram' ? 'Connecting...' : 'Instagram'}</span>
            </button>

            {/* TikTok Login */}
            <button
              onClick={() => handleSocialLogin('tiktok')}
              disabled={isLoading !== null}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm bg-black hover:bg-gray-800 text-white rounded-md font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading === 'tiktok' ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/>
                </svg>
              )}
              <span className="text-sm">{isLoading === 'tiktok' ? 'Connecting...' : 'TikTok'}</span>
            </button>

            {/* Divider */}
            <div className="relative my-3">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200"></div>
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="px-2 bg-white text-gray-500">or</span>
              </div>
            </div>

            {/* Email Login Option */}
            <button className="w-full px-4 py-2.5 text-sm border border-gray-300 text-gray-700 rounded-md font-medium hover:bg-gray-50 transition-all">
              Continue with Email
            </button>
          </div>

          {/* Terms */}
          <div className="px-4 pb-4">
            <p className="text-xs text-gray-500 text-center">
              By continuing, you agree to our{' '}
              <a href="/terms" className="text-blue-600 hover:underline">Terms</a>
              {' '}and{' '}
              <a href="/privacy" className="text-blue-600 hover:underline">Privacy Policy</a>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
