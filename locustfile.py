from locust import HttpUser, task, between

class ByteBurstUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def view_catalog(self):
        # Target the catalog service
        self.client.get("http://127.0.0.1:8001/products")

    @task(1)
    def create_order(self):
        # Target the order service
        self.client.post("http://127.0.0.1:8002/orders?product_id=1&quantity=1")