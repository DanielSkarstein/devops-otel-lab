from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Give the service a name so it is easy to recognise in the collector output
resource = Resource.create({"service.name": "a8-checkout-demo"})
provider = TracerProvider(resource=resource)

# Send spans to the collector over OTLP (gRPC, port 4317) instead of the console
exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout"):                 # parent
    with tracer.start_as_current_span("charge-card") as span:  # child
        span.set_attribute("payment.amount", 499)
        print("paid")

# Flush remaining spans to the collector before the program exits
provider.shutdown()