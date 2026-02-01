FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npx svelte-kit sync 
RUN npm run build
