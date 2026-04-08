'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Property {
  id: number
  name: string
  city: string
  country: string
  price_per_night: number
  description: string
  is_published: boolean
}

export default function PropertiesPage() {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchProperties()
  }, [])

  const fetchProperties = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/properties/', {
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to fetch properties')
      }

      const data = await response.json()
      setProperties(data.results || data || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load properties')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              SaaS Booking
            </Link>
            <nav className="space-x-4">
              <Link href="/login" className="text-blue-600 hover:underline">
                Owner Login
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Available Properties</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-8">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="text-gray-600 mt-4">Loading properties...</p>
          </div>
        ) : properties.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No properties available yet.</p>
            <p className="text-gray-500 mt-2">Check back soon!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {properties.map((property) => (
              <div
                key={property.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition"
              >
                <div className="bg-gradient-to-r from-blue-400 to-blue-600 h-48 flex items-center justify-center">
                  <span className="text-white text-3xl">🏠</span>
                </div>

                <div className="p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-2">{property.name}</h2>

                  <div className="flex items-center text-gray-600 mb-2">
                    <span className="mr-2">📍</span>
                    <span>
                      {property.city}, {property.country}
                    </span>
                  </div>

                  <p className="text-gray-600 text-sm mb-4">{property.description || 'Beautiful guest house'}</p>

                  <div className="flex justify-between items-center">
                    <div className="text-2xl font-bold text-blue-600">
                      ${property.price_per_night}
                      <span className="text-sm text-gray-600 ml-1">/night</span>
                    </div>
                    <span className={`px-3 py-1 rounded text-sm font-medium ${
                      property.is_published
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {property.is_published ? 'Available' : 'Soon'}
                    </span>
                  </div>

                  <button className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 rounded-lg transition">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
