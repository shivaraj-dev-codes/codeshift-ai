FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY --from=0 /app/package.json /app/package-lock.json* ./
COPY --from=0 /app/node_modules ./node_modules
COPY --from=0 /app/.next ./.next
COPY --from=0 /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
