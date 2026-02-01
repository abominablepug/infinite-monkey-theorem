FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npx svelte-kit sync 
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json
RUN npm install --omit=dev

ENV PORT=5173
ENV HOST=0.0.0.0

EXPOSE 5173

CMD ["node", "build/index.js"]
