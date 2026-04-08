'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  phone: string
  email_verified: boolean
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')

    if (!token) {
      // No token, redirect to login
      router.push('/login')
      return
    }

    // Parse stored user
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (e) {
        setError('Invalid user data')
      }
    }

    setLoading(false)
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
        <div className="text-white">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error || !user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
          <p className="text-red-600 mb-4">{error || 'User not found'}</p>
          <Link href="/login" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 inline-block">
            Back to Login
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">SaaS Booking Platform</h1>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Card */}
        <div className="bg-white rounded-lg shadow mb-8 p-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Welcome, {user.first_name}! 👋</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border-l-4 border-blue-600 pl-4">
              <h3 className="text-gray-600 text-sm font-medium">Email</h3>
              <p className="text-lg font-semibold text-gray-900">{user.email}</p>
            </div>
            <div className="border-l-4 border-green-600 pl-4">
              <h3 className="text-gray-600 text-sm font-medium">Full Name</h3>
              <p className="text-lg font-semibold text-gray-900">{user.first_name} {user.last_name}</p>
            </div>
            <div className="border-l-4 border-purple-600 pl-4">
              <h3 className="text-gray-600 text-sm font-medium">Phone</h3>
              <p className="text-lg font-semibold text-gray-900">{user.phone || 'Not provided'}</p>
            </div>
            <div className="border-l-4 border-yellow-600 pl-4">
              <h3 className="text-gray-600 text-sm font-medium">Email Verified</h3>
              <p className="text-lg font-semibold">
                <span className={user.email_verified ? 'text-green-600' : 'text-yellow-600'}>
                  {user.email_verified ? '✓ Verified' : '⏳ Pending'}
                </span>
              </p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <div className="text-3xl mb-3">🏠</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">My Properties</h3>
            <p className="text-gray-600 mb-4">Manage your guest houses and villas</p>
            <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
              View Properties
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <div className="text-3xl mb-3">📅</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Bookings</h3>
            <p className="text-gray-600 mb-4">Track guest reservations</p>
            <button className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
              View Bookings
            </button>
          </div>

          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <div className="text-3xl mb-3">💰</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Payments</h3>
            <p className="text-gray-600 mb-4">Monitor your earnings</p>
            <button className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700">
              View Payments
            </button>
          </div>
        </div>

        {/* Getting Started */}
        <div className="bg-white rounded-lg shadow p-8">
          <h3 className="text-xl font-bold mb-4 text-gray-900">🚀 Getting Started</h3>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 text-green-600 flex items-center justify-center">✓</div>
              <div className="ml-3">
                <h4 className="text-lg font-semibold text-gray-900">Account Created</h4>
                <p className="text-gray-600">Your account has been successfully created</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 text-gray-400 flex items-center justify-center">→</div>
              <div className="ml-3">
                <h4 className="text-lg font-semibold text-gray-900">Add Your First Property</h4>
                <p className="text-gray-600">Create a property listing for your guest house or villa</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 text-gray-400 flex items-center justify-center">→</div>
              <div className="ml-3">
                <h4 className="text-lg font-semibold text-gray-900">Set Availability & Pricing</h4>
                <p className="text-gray-600">Define your rates and available dates</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="flex-shrink-0 h-6 w-6 text-gray-400 flex items-center justify-center">→</div>
              <div className="ml-3">
                <h4 className="text-lg font-semibold text-gray-900">Start Receiving Bookings</h4>
                <p className="text-gray-600">Guests can now book your properties directly</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-600">
          <p>Need help? <Link href="#" className="text-blue-600 hover:underline">Contact Support</Link></p>
        </div>
      </div>
    </div>
  )
}
