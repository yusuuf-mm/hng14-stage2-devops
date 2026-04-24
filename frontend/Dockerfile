# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install --production

# Final stage
FROM node:20-alpine
WORKDIR /app

# Create non-root user
RUN adduser -D -u 1001 appuser

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy app code
COPY app.js .
COPY views/ ./views/

# Switch to non-root user
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"

CMD ["node", "app.js"]
