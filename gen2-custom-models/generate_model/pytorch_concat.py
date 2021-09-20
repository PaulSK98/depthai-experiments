#! /usr/bin/env python3

from pathlib import Path
import torch
from torch import nn

class CatImgs(nn.Module):
    def forward(self, img1, img2, img3):
        return torch.cat((img1, img2, img3), 3)

# Define the expected input shape (dummy input)
shape = (1, 3, 300, 300)
X = torch.ones(shape, dtype=torch.float32)

path = Path("out/")
path.mkdir(parents=True, exist_ok=True)
output_file = "out/concat.onnx"

print(f"Writing to {output_file}")
torch.onnx.export(
    CatImgs(),
    (X, X, X),
    output_file,
    opset_version=12,
    do_constant_folding=True,
    input_names = ['img1', 'img2', 'img3'], # Optional
    output_names = ['output'], # Optional
)
