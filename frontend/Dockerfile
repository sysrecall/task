# Stage 1: Build
FROM node:24-alpine AS builder
WORKDIR /usr/src/app

# Accept build-time environment variable
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

# Stage 2: Production
FROM node:24-alpine AS final
WORKDIR /usr/src/app

# Set production environment
ENV NODE_ENV=production

# Copy app and node_modules from builder
COPY --from=builder /usr/src/app/package*.json ./
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/.next ./.next
COPY --from=builder /usr/src/app/public ./public

# Expose the port Next.js will run on
EXPOSE 3000

# Run the app
CMD ["npm", "run", "start"]
