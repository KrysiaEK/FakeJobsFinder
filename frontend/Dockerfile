FROM node:16.18.1 AS build
ENV NODE_ENV=development NITRO_HOST=${NUXT_HOST:-0.0.0.0} NITRO_PORT=${NUXT_PORT:-3000} NUXT_TELEMETRY_DISABLED=1
COPY . /app
WORKDIR /app
RUN npm install --non-interactive
RUN npm install -g serve
RUN npm run build
EXPOSE 80

FROM build AS run-dev
COPY --from=build /app/build /app/build
CMD ["serve", "-s", "-p", "80", "build"]

FROM build AS run-start
ENV NODE_ENV=production
COPY --from=build /app/build /app/build
CMD ["serve", "-s", "-p", "80", "build"]

FROM build as run-minimal
COPY --from=build /app/build /app/build
CMD ["serve", "-s", "-p", "80", "build"]
