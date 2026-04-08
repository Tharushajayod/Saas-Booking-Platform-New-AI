# Optimized Frontend Dockerfile for Next.js with improved build handling
FROM node:18-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy application code
COPY . .

# Ensure public directory exists
RUN mkdir -p /app/public

# Build the application with verbose output
RUN npm run build || (echo "Build failed, checking logs..."; cat package.json; echo "Node version:"; node --version; npm --version; exit 1)

# Verify build artifacts exist
RUN ls -la /app/.next || (echo ".next folder not found!"; exit 1)

# Production stage
FROM node:18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init curl

# Copy only necessary files from builder
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start Next.js in production mode
CMD ["npm", "start"]

# Simple healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1
