from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests # NEW
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor # NEW

from db import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

resource = Resource.create(attributes={"service.name": "order-service"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger-service:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI(title="ByteBurst Order Service")
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument() # Automagically injects Jaeger trace headers!

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/orders")
def create_order(product_id: int, quantity: int, db: Session = Depends(get_db)):
    # Internal cluster call to verify the catalog
    try:
        # catalog-service is the exact name of the Kubernetes Service in catalog.yaml
        response = requests.get("http://catalog-service/products")
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Catalog service unavailable")
        
    db_order = models.Order(product_id=product_id, quantity=quantity, status="pending")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders")
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Order).offset(skip).limit(limit).all()