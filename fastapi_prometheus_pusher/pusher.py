import os
import re
from typing import Callable, List

from fastapi import FastAPI

from .tasks import repeat_every
from . import metrics
from .middleware import (
    PrometheusFastApiPusherMiddleware,
)


class PrometheusFastApiPusher:
    def __init__(
        self,
        should_group_status_codes: bool = True,
        should_ignore_untemplated: bool = False,
        should_group_untemplated: bool = True,
        should_round_latency_decimals: bool = False,
        should_instrument_requests_inprogress: bool = False,
        excluded_handlers: List[str] = None,
        round_latency_decimals: int = 4,
        inprogress_name: str = "http_requests_inprogress",
        inprogress_labels: bool = False,
    ):
        self.should_group_status_codes = should_group_status_codes
        self.should_ignore_untemplated = should_ignore_untemplated
        self.should_group_untemplated = should_group_untemplated
        self.should_round_latency_decimals = should_round_latency_decimals
        self.should_instrument_requests_inprogress = should_instrument_requests_inprogress

        self.round_latency_decimals = round_latency_decimals
        self.inprogress_name = inprogress_name
        self.inprogress_labels = inprogress_labels

        if excluded_handlers is None:
            excluded_handlers = []

        self.excluded_handlers = [re.compile(
            path) for path in excluded_handlers]

        self.instrumentations: List[Callable[[metrics.Info], None]] = []

    def start(
        self,
        app: FastAPI,
        prometheus_host: str,
        job_name: str,
        repeat_seconds: int = 60
    ):
        app.add_middleware(
            PrometheusFastApiPusherMiddleware,
            should_group_status_codes=self.should_group_status_codes,
            should_ignore_untemplated=self.should_ignore_untemplated,
            should_group_untemplated=self.should_group_untemplated,
            should_round_latency_decimals=self.should_round_latency_decimals,
            should_instrument_requests_inprogress=self.should_instrument_requests_inprogress,
            round_latency_decimals=self.round_latency_decimals,
            inprogress_name=self.inprogress_name,
            inprogress_labels=self.inprogress_labels,
            instrumentations=self.instrumentations,
            excluded_handlers=self.excluded_handlers,
        )
        from prometheus_client import (
            REGISTRY,
            CollectorRegistry,
            multiprocess,
            push_to_gateway,
        )

        if "prometheus_multiproc_dir" in os.environ:
            pmd = os.environ["prometheus_multiproc_dir"]
            if os.path.isdir(pmd):
                registry = CollectorRegistry()
                multiprocess.MultiProcessCollector(registry)
            else:
                raise ValueError(
                    f"Env var prometheus_multiproc_dir='{pmd}' not a directory."
                )
        else:
            registry = REGISTRY

        @app.on_event("startup")
        @repeat_every(seconds=repeat_seconds)
        def metrics() -> None:
            push_to_gateway(prometheus_host, job=job_name, registry=registry)

        return self

    def add(self, instrumentation_function: Callable[[metrics.Info], None]):
        self.instrumentations.append(instrumentation_function)
        return self
