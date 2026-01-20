from pycoral.utils import edgetpu

tpu = edgetpu.list_edge_tpus()
if tpu:
    print("Edge TPU devices found:", tpu)
else:
    print("No Edge TPU devices found.")