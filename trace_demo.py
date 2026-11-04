from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# 1. Set up the tracer provider (the "factory" that creates and manages spans)
provider = TracerProvider()

# 2. Attach an exporter: print every finished span to the console
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

# 3. Register the provider globally and get a tracer for this program
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("a8.demo")

# 4. Create a parent span with a child span inside it
with tracer.start_as_current_span("checkout"):            # parent
    with tracer.start_as_current_span("charge-card"):     # child
        print("paid")