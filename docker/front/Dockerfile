FROM node:24-alpine AS node

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

CMD ["tail", "-f", "/dev/null"]


FROM nginx:alpine AS nginx

COPY docker/front/nginx.conf /etc/nginx/conf.d/default.conf

COPY docker/front/fullchain.pem /etc/nginx/conf.d/fullchain.pem
COPY docker/front/privkey.pem /etc/nginx/conf.d/privkey.pem

COPY --from=node /app/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]