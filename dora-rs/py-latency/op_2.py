#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from typing import Callable

import numpy as np
import pyarrow as pa
from dora import DoraStatus
from helper import record_results

pa.array([])

NAME = "dora Operator"


class Operator:
    """
    Template docstring
    """

    def __init__(self) -> None:
        self.size_index = 0
        self.i = 0
        self.current_size = 8
        self.n = 0
        self.latencies = []

    def on_event(
        self,
        dora_event: dict,
        send_output: Callable[[str, bytes], None],
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            return self.on_input(dora_event, send_output)
        return DoraStatus.CONTINUE

    def on_input(
        self,
        dora_input: dict,
        _send_output: Callable[[str, bytes], None],
    ):
        """

        Args:
            dora_input (dict): Input dict containing an `id`, `data` and `metadata`.
            send_output (Callable[[str, bytes], None]): Send output to the dataflow

        Returns:
            DoraStatus:
                CONTINUE means that the operator will
                    keep listening for further inputs.
                STOP means that the operator stop listening for inputs.

        """
        data = dora_input["value"]
        length = len(data) * 8

        # frame = np.frombuffer(data, dtype="uint8")
        # frame = cv2.imdecode(frame, -1)
        t_received = time.perf_counter_ns()
        if length != self.current_size:
            if self.n > 0:
                record_results(NAME, self.current_size, self.latencies)
            self.current_size = length
            self.n = 0
            self.latencies = []

        ## Arrow Test: Using PyBytes
        # t_send = np.frombuffer(dora_input["data"][:8], np.uint64)

        ## Arrow Test: Using Arrow
        t_send = data[0].as_py()
        self.latencies.append((t_received - t_send) / 1000)
        self.n += 1

        return DoraStatus.CONTINUE
