import onnx
from onnx import TensorProto

onnx_model = onnx.load_model("C:\\Users\\NERO\\Desktop\\FTVSR\\FTVSR_1155_op19.onnx")
for node in onnx_model.graph.node:
    if node.op_type == 'ReduceMax':
        print(node)
        for idx, cur_attr in enumerate(node.attribute):
            if cur_attr.name == 'axes':
                del node.attribute[idx]                                     
                # 删除原始attribute中的axes
                break
        input_tensor = onnx.helper.make_tensor(name=node.name+'_axes',
                                               data_type=TensorProto.INT64,
                                               dims=[1],
                                               vals=[2])               
        # 创建一个存放axes的tensor
        onnx_model.graph.initializer.append(input_tensor)                   
        # 将新创建的axes tensor添加到onnx模型initializer proto结构中
        node.input.append(input_tensor.name)                                
        # 将axes tensor的name加入到ReduceMean算子的input中
onnx.save_model(onnx_model, "C:\\Users\\NERO\\Desktop\\FTVSR\\FTVSR_1155_op19_ReduceMax.onnx")

