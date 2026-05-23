FROM node:18-alpine

WORKDIR /app

# Copy package files first for caching
COPY package.json package-lock.json* ./

RUN npm install --legacy-peer-deps

# Copy source files
COPY . .

# Build React app
RUN npm run build

# Install serve to serve build folder
RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
