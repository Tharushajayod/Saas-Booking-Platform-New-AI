export function formatCurrency(amount: number, currency = 'LKR'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount)
}

export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

export function calculateNights(checkIn: Date | string, checkOut: Date | string): number {
  const start = typeof checkIn === 'string' ? new Date(checkIn) : checkIn
  const end = typeof checkOut === 'string' ? new Date(checkOut) : checkOut
  return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
}

export function generateBookingRef(): string {
  return `BKG-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
}
