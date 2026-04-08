import { create } from 'zustand'

interface AuthStore {
  isAuthenticated: boolean
  user: any | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: any) => void
  setToken: (token: string) => void
}

export const useAuthStore = create<AuthStore>((set) => ({
  isAuthenticated: false,
  user: null,
  token: null,
  
  login: async (email: string, password: string) => {
    // Login logic will be implemented
    set({ isAuthenticated: true })
  },
  
  logout: () => {
    set({ isAuthenticated: false, user: null, token: null })
  },
  
  setUser: (user) => set({ user }),
  setToken: (token) => set({ token }),
}))

interface BookingStore {
  bookings: any[]
  loading: boolean
  setBookings: (bookings: any[]) => void
  setLoading: (loading: boolean) => void
}

export const useBookingStore = create<BookingStore>((set) => ({
  bookings: [],
  loading: false,
  setBookings: (bookings) => set({ bookings }),
  setLoading: (loading) => set({ loading }),
}))
