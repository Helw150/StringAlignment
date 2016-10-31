from libs.server.Service import Service
from libs.server.Service import ServiceDescription
import tornado.web
import os

service_descriptions = [ServiceDescription("test_service_1", 9001),
                        ServiceDescription("test_service_2", 9002),
                        ServiceDescription("test_service_3", 9003),
                        ServiceDescription("test_service_4", 9004)]


class TestService(Service):
    def __init__(self, service_number):
        dependencies = list(service_descriptions)
        del dependencies[service_number]
        super().__init__(service_descriptions[service_number], dependencies)

    def get_routes(self):
        return [
            (r"/", HelloHandler)
        ]


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")


if __name__ == "__main__":
    # Working case
    for i in range(4):
        if os.fork() == 0:
            TestService(i)
    # Failing case
    # TestService(0)
