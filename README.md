# valauto-api

A minimal [FastAPI](https://fastapi.tiangolo.com/) service that exposes a
simple model through an HTTP endpoint and is ready to run with Docker Compose.

## Endpoints

| Method | Path        | Description                                      |
|--------|-------------|--------------------------------------------------|
| GET    | `/evaluate` | Runs the simple model and returns an `int`.      |
| GET    | `/health`   | Liveness probe, returns `{"status": "ok"}`.      |
| GET    | `/docs`     | Auto-generated Swagger UI.                       |


## Create environment variables
```bash
cp .env.example .env
```

## Run with Docker Compose

```bash
docker compose up --build
```

## Build front
```bash
docker exec -it valauto-api-front npm run build
```

## Do czystości kodu 
```bash
docker exec -it valauto-api-front npx eslint .
```