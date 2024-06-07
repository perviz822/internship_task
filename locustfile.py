from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def simple_get(self):
        self.client.get("/")


command = 'locust -f locustfile.py --host=http://example.com --csv=example_log --csv-full-history --headless -u 100 -r 10 -t 1m'