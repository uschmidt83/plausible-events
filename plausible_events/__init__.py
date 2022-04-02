import threading
import time
from urllib.parse import urlencode

# import miniupnpc
import requests

from .version import __version__

UTM_TERMS = "campaign", "source", "medium", "term", "content"


def _print_debug(debug):
    return (lambda *args: print(*args, flush=True)) if debug else (lambda *args: None)


class Worker(threading.Thread):
    def __init__(self, cond: threading.Condition, queue: list, timeout: float, debug: bool = False):
        super().__init__()
        self.cond = cond
        self.queue = queue
        self.timeout = timeout
        self.print = _print_debug(debug)

    def run(self):
        while True:
            with self.cond:
                if self.cond.wait_for(lambda: len(self.queue) > 0):
                    task = self.queue.pop(0)
            try:
                self.print("worker: run task")
                task()
            except Exception as e:
                self.print(f"worker: exception {repr(e)}")
                with self.cond:
                    self.queue.insert(0, task)
                time.sleep(self.timeout)


class PlausibleEvents:
    """https://plausible.io/docs/events-api"""

    def __init__(
        self,
        domain: str,
        headers: dict = None,
        timeout: float = 5.0,
        api: str = "https://plausible.io/api/event",
        debug: bool = False,
    ):
        self.api = api
        self.domain = domain
        self.cond = threading.Condition()
        self.queue = []
        self.worker = Worker(self.cond, self.queue, timeout, debug)
        self.print = _print_debug(debug)

        def default_headers():
            self.headers = {
                "X-Forwarded-For": self._get_ip(),
            }
            if headers is not None:
                self.headers.update(headers)

        self._enqueue_task(default_headers, False)

    def _enqueue_task(self, task: callable, start_worker: bool = True):
        if start_worker and not self.worker.is_alive():
            self.print("main:   start worker")
            self.worker.start()

        self.print("main:   append task")
        with self.cond:
            self.queue.append(task)
            self.cond.notify()

    # def _get_ip(self):
    #     # https://stackoverflow.com/a/41385033
    #     u = miniupnpc.UPnP()
    #     u.discoverdelay = 200
    #     u.discover()
    #     u.selectigd()
    #     return str(u.externalipaddress())

    def _get_ip(self):
        r = requests.get("https://api.ipify.org")
        r.raise_for_status()
        return r.text.strip()

    def _event(self, name: str, path: str, headers: dict = None, utm: dict = None, props: dict = None):
        if path.startswith("/"):
            path = path[1:]
        _headers = self.headers
        if headers is not None:
            _headers = _headers.copy()
            _headers.update(headers)
        if utm is not None and len(utm) > 0:
            assert all(k in UTM_TERMS for k in utm.keys())
            utm_terms = "?" + urlencode({f"utm_{k}": v for k, v in utm.items()})
        else:
            utm_terms = ""
        if props is None:
            props = {}
        props = {str(k): str(v) for k, v in props.items()}

        r = requests.post(
            self.api,
            headers=_headers,
            json=dict(
                domain=self.domain,
                name=name,
                url=f"app://localhost/{path}{utm_terms}",
                props=props,
            ),
        )
        r.raise_for_status()
        self.print(f"event:  name='{name}', path='{path}', headers={headers}, utm={utm}, props={props}")
        return r

    def pageview(self, path: str, utm: dict = None, headers: dict = None):
        def task():
            self._event(name="pageview", path=path, headers=headers, utm=utm)

        self._enqueue_task(task)

    def event(self, name: str, props: dict = None, path: str = "", utm: dict = None, headers: dict = None):
        def task():
            self._event(name=name, path=path, headers=headers, utm=utm, props=props)

        self._enqueue_task(task)
