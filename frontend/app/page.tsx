export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            SaaS Booking Platform
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Multi-Tenant Direct Booking Platform for Guest Houses & Villas in Sri Lanka
          </p>
          <div className="flex gap-4 justify-center">
            <a
              href="/login"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Owner Login
            </a>
            <a
              href="/properties"
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
            >
              Browse Properties
            </a>
          </div>
        </div>
      </div>
    </main>
  )
}
