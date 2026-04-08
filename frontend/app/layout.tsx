import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SaaS Booking Platform',
  description: 'Multi-Tenant Direct Booking Platform for Guest Houses & Villas',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}
