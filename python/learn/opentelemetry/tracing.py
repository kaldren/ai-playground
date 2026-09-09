"""A minimal OpenTelemetry span example."""

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example"):
    print("Work performed inside a span")
