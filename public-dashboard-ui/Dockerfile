# Stage 1: Build the Vite + React app
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency manifests first (layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Accept build args for Vite env vars (baked in at build time)
ARG VITE_INFLUX_URL=http://influxdb:8086
ARG VITE_INFLUX_TOKEN=my-super-secret-auth-token
ARG VITE_INFLUX_ORG=kabir-das-org
ARG VITE_INFLUX_BUCKET=flood_monitoring
ARG VITE_BASE_PATH=/

# Set them as env vars so Vite picks them up
ENV VITE_INFLUX_URL=$VITE_INFLUX_URL
ENV VITE_INFLUX_TOKEN=$VITE_INFLUX_TOKEN
ENV VITE_INFLUX_ORG=$VITE_INFLUX_ORG
ENV VITE_INFLUX_BUCKET=$VITE_INFLUX_BUCKET
ENV VITE_BASE_PATH=$VITE_BASE_PATH

# Build production bundle
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
