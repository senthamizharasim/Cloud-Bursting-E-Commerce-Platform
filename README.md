# ByteBurst

**A cloud bursting e-commerce platform with distributed tracing.**


ByteBurst runs as containerised microservices on a local Kubernetes cluster (Minikube) and is designed to overflow onto Azure Kubernetes Service (AKS) when local capacity runs out. It is load-tested with Locust and fully traced with OpenTelemetry and Jaeger.

**Status:** Review 2 complete (about 80%). The Horizontal Pod Autoscaler and the Azure AKS burst are the remaining work.

## Architecture

```
Locust / Swagger UI
        |
        v
  order-service  --HTTP-->  catalog-service
   (FastAPI :8002)           (FastAPI :8001)
        |                          |
        +---------> PostgreSQL <---+        (via SQLAlchemy)

  Both services emit OpenTelemetry spans --> Jaeger
```

| Component | Technology | Role |
|---|---|---|
| catalog-service | FastAPI, port 8001 | Serves the product list (`GET /products`) |
| order-service | FastAPI, port 8002 | Accepts orders (`POST /orders`), calls catalog |
| Database | PostgreSQL + SQLAlchemy | Persistent storage |
| Packaging | Docker | One image per service |
| Orchestration | Minikube (Kubernetes) | Runs services as pods |
| Load testing | Locust | Simulated concurrent users |
| Observability | OpenTelemetry + Jaeger | Distributed tracing |

## Why these choices

- **FastAPI:** high performance, native async, automatic Swagger/OpenAPI docs, easy OpenTelemetry instrumentation.
- **PostgreSQL + SQLAlchemy:** ACID transactions for orders, with models written as plain Python classes.
- **Docker + Minikube:** the same images and manifests can later run on AKS.
- **OpenTelemetry + Jaeger:** vendor-neutral tracing that shows where time is spent across services.
- **Locust:** Python-native load tests with a live web dashboard.

## Getting started

### Prerequisites

- Docker
- Minikube and kubectl
- Python 3.10+ (for running services or Locust outside the cluster)

### Run the full stack

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
./deploy.sh
```

`deploy.sh` builds the images, deploys to Minikube, exposes the services via port-forward and verifies the endpoints, so you don't need a separate terminal for each step.

### Try the API

With the stack running, open the Swagger UI for the order service and call `POST /orders` with `product_id` and `quantity` as query parameters:

```bash
curl -X POST "http://127.0.0.1:8002/orders?product_id=1&quantity=5"
curl "http://127.0.0.1:8001/products"
```

Interactive docs: `http://127.0.0.1:8002/docs`

### Run the load test

Start Locust, open its web UI, and point it at `http://127.0.0.1:8001` with 50 users targeting `GET /products`.
<img width="958" height="263" alt="Screenshot 2026-10-09 145517" src="https://github.com/user-attachments/assets/9bfdd695-d587-4ca8-a9da-2f796647e123" />

<img width="932" height="407" alt="Screenshot 2026-10-09 145532" src="https://github.com/user-attachments/assets/a67618ad-a808-4355-a3e1-f3c7d4e5794a" />


### View traces

Open the Jaeger UI, choose `order-service` or `catalog-service`, and click **Find Traces**.

<img width="956" height="429" alt="Screenshot 2026-10-09 150107" src="https://github.com/user-attachments/assets/39bd9bda-40e8-4542-86cb-0fef9430a82a" />
<img width="959" height="320" alt="Screenshot 2026-10-09 150120" src="https://github.com/user-attachments/assets/6865fdd2-c3ff-4f41-a59b-fdc588c42e3a" />
<img width="947" height="400" alt="Screenshot 2026-10-09 150154" src="https://github.com/user-attachments/assets/10d9c9d1-e246-4f5a-a805-f4b08463a032" />
<img width="957" height="411" alt="Screenshot 2026-10-09 150215" src="https://github.com/user-attachments/assets/fc0a62ef-6f98-4b79-8578-014151ee465e" />





## Results so far

Load test: 50 users against `GET /products` on a single deployment.

| Metric | Value |
|---|---|
| Total requests | 46,266 |
| Failures | 0 |
| Throughput | 19.8 req/s |
| Median latency | 570 ms |
| 95th percentile | 2,500 ms |
| 99th percentile | 5,100 ms |

Tracing: one `POST /orders` trace spans both services with 7 spans. The catalog handler takes about 4.2 ms, so most of a slow request is spent in the order service before the catalog call starts. This is under investigation.

Known caveat: the average response size was 2 bytes, which suggests the endpoint returned an empty list during the test. The test will be repeated with seeded data before the HPA comparison.



## Roadmap

- [x] Catalog and order microservices (FastAPI)
- [x] PostgreSQL integration with SQLAlchemy
- [x] Docker and Minikube deployment
- [x] One-command deployment (`deploy.sh`)
- [x] Locust load testing
- [x] Distributed tracing (OpenTelemetry + Jaeger)
- [ ] Horizontal Pod Autoscaler (CPU-based), then re-run Locust and compare p95/p99
- [ ] Azure AKS cloud burst: provision AKS, publish images, deploy the same manifests, route overflow traffic, scale back

## Done by:

- Senthamizharasi M
