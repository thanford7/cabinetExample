# syntax=docker/dockerfile:1

FROM nginx:1.25
COPY local.conf /etc/nginx/conf.d/local.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]