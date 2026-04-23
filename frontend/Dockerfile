# Build stage
FROM node:20-slim AS builder

WORKDIR /app

COPY package.json .
RUN npm install --production

# Final stage
FROM node:20-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1001 appuser

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY app.js .
COPY views ./views

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"

CMD ["node", "app.js"]
