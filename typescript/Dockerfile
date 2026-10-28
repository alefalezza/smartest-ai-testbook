FROM node:24.22.1-bookworm-slim

WORKDIR /workspace

COPY package*.json ./

RUN npm ci

# EXPOSE 3000

CMD ["npm", "run", "dev"]
