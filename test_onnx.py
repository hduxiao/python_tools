import onnx
import onnxruntime as ort
import numpy as np

model_file = "C:\\Users\\NERO\\Desktop\\FTVSR\\FTVSR_1155_op19_ReduceMax.onnx"
onnx_model = onnx.load_model(model_file)
onnx.checker.check_model(onnx_model)

# Create ONNX Runtime inference session.
# https://onnxruntime.ai/docs/get-started/with-python.html
ort_sess = ort.InferenceSession(model_file, providers=["CPUExecutionProvider"])

input_nodes = ort_sess.get_inputs()
input_names = [node.name for node in input_nodes]
input_shapes = [node.shape for node in input_nodes]
input_types = [node.type for node in input_nodes]
output_nodes = ort_sess.get_outputs()
output_names = [node.name for node in output_nodes]
output_shapes = [node.shape for node in output_nodes]
output_types = [node.type for node in output_nodes]

# Read test input and output files.
width = 200
height = 192
frames = np.random.rand(1, 4, 3, height, width).astype('float32')

# Run unit test.
output_tensors = ort_sess.run(output_names=output_names, input_feed={input_names[0]: frames}, run_options=None)
print(output_tensors[1].shape)
