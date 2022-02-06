import numpy as np
import tensorflow as tf


def load_model():
    return tf.keras.models.load_model("../best_model/gene-nn")


def parse_input(inp: str):
    aminoacids = ["A", "R", "N", "D", "C", "E", "Q", "G", "H",
                  "I", "L", "K", "M", "F", "P", "S", "T", "W",
                  "Y", "V"]
    lines = inp.splitlines()
    if inp.startswith(">"):
        lines = lines[1:]
    lines = "".join(lines)
    X = np.array([[lines.count(aa) for aa in aminoacids]])
    # print(X)
    return X
