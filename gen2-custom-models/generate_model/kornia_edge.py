#! /usr/bin/env python3

from pathlib import Path
import torch
from torch import nn
import kornia
import onnx
from onnxsim import simplify

name = 'edge'

class Model(nn.Module):
    def forward(self, image):
        return kornia.filters.laplacian(image, kernel_size=3, border_type='reflect', normalized=True)

# Define the expected input shape (dummy input)
shape = (1, 3, 300, 300)
model = Model()
X = torch.ones(shape, dtype=torch.float32)

path = Path("out/")
path.mkdir(parents=True, exist_ok=True)
onnx_path = str(path / (name + '.onnx'))

print(f"Writing to {onnx_path}")
torch.onnx.export(
    model,
    X,
    onnx_path,
    opset_version=12,
    do_constant_folding=True,
)

# Use onnx-simplifier to simplify the onnx model
onnx_model = onnx.load(onnx_path)
model_simp, check = simplify(onnx_model)
onnx.save(model_simp, str(path / (name + '_simplified.onnx')))

# Use model optimizer to convert onnx->IR (bin/xml)

# Use blobconverter to convert IR->blob