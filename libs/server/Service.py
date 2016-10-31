# Deals with interservice communication
import collections
import time
import sys
import json
import traceback
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor

import tornado.web
from tornado.httpclient import HTTPClient
import tornado.websocket


ServiceDescription = collections.namedtuple("ServiceDescription",
                                            ["service_name", "port"])


class Service(metaclass=ABCMeta):
    def __init__(self, service_description, dependencies, port=None):
        print("Service %s starting" % service_description.service_name)
        self.service_description = service_description

        # Status of each dependency
        self.dependencies = dependencies

        executor = ThreadPoolExecutor(max_workers=1)
        self.ready_future = executor.submit(self.check_dependencies)

        # Inject our service into each route
        routes = list(map(lambda x: x + ({"service": self},),
                          self.get_routes()))
        app = tornado.web.Application([
            (r"/status", StatusHandler, {"service": self})
        ] + routes)
        if not port:
            port = self.service_description.port
        app.listen(port)

        self.ioloop = tornado.ioloop.IOLoop.current()
        self.ioloop.add_future(
            self.ready_future,
            lambda x: self.shutdown() if x.result() is False else "")
        print("Service %s bound to port %d" %
              (service_description.service_name, port))
        self.ioloop.start()

    def shutdown(self):
        print("Service %s stopping" % self.service_description.service_name,
              file=sys.stderr)
        self.ioloop.add_callback(self.ioloop.stop)

    @abstractmethod
    def get_routes(self):
        pass

    def get_status(self):
        return "ready" if self.ready_future.done() else "started"

    def check_dependency(self, service_description):
        """\
        return vals:
        True - service discovered and
        False - service discovered but there was a problem
        None - service not discovered
        """
        try:
            http_client = HTTPClient()
            response = http_client.fetch("http://localhost:%d/status" %
                                         service_description.port)
            print("Connected to service %s" % service_description.service_name)
            print(response)
            return True
        except Exception as e:
            print("Error connecting to service %s: %s" %
                  (service_description.service_name,
                   str(e)), file=sys.stderr)
            if type(e) is ConnectionRefusedError:
                return None
            else:
                print("Error was %s" % str(type(e)), file=sys.stderr)
                print("Giving up", file=sys.stderr)
                return False

    def check_dependencies(self, timeout=60):
        """\
        Returns whether all dependencies can be connected to
        """
        try:
            start = time.time()
            now = time.time()
            dependencies = list(self.dependencies)
            if len(dependencies) > 0:
                with ThreadPoolExecutor(
                        max_workers=len(self.dependencies)) as executor:
                    while (now - start < timeout and len(dependencies) > 0):
                        dependency_statuses = list(map(
                            lambda x: executor.submit(
                                self.check_dependency, x),
                            dependencies))
                        remaining_dependencies = []
                        for i in range(len(dependencies)):
                            if (dependency_statuses[i].result(timeout=2)
                                    is not True):
                                remaining_dependencies.append(dependencies[i])
                        dependencies = remaining_dependencies
                        time.sleep(2)
                        now = time.time()
            if len(dependencies) > 0:
                print("Could not connect to dependencies:\n%s" %
                      " ".join(list(map(lambda x: x.service_name,
                                        dependencies))))
                return False
            else:
                print("Service %s ready" %
                      self.service_description.service_name)
                return True
        except Exception as e:
            traceback.print_exc()
            return False


class ServiceHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, service):
        self.service = service

    def check_origin(self, origin):
        return True

    def open(self):
        print("New socket connection")

    def on_close(self):
        print("Connection closed")

    def process(self, query):
        raise NotImplementedError("You must implement process() on %s" %
                                  self.__class__.name)

    def on_message(self, message):
        self.write_message(self.process(json.loads(message)))


class StatusHandler(tornado.web.RequestHandler):
    def initialize(self, service):
        self.service = service

    def get(self):
        self.write({
            "service_name": self.service.service_description.service_name,
            "status": self.service.get_status()
        })
