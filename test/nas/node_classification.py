"""
Test file for nas on node classification

AUTOGL_BACKEND=pyg python test/nas/node_classification.py
AUTOGL_BACKEND=dgl python test/nas/node_classification.py
"""

import os
import logging

logging.basicConfig(level=logging.INFO)

from autogl.backend import DependentBackend

if DependentBackend.is_dgl():
    from autogl.module.model.dgl import BaseModel
    from dgl.data import CoraGraphDataset
elif DependentBackend.is_pyg():
    from torch_geometric.datasets import Planetoid
    from autogl.module.model.pyg import BaseModel

import torch
import torch.nn.functional as F
from autogl.module.nas.space.single_path import SinglePathNodeClassificationSpace
from autogl.module.nas.space.graph_nas import GraphNasNodeClassificationSpace
from autogl.module.nas.space.graph_nas_macro import GraphNasMacroNodeClassificationSpace
from autogl.module.nas.estimator.one_shot import OneShotEstimator
from autogl.module.nas.backend import bk_feat, bk_label
from autogl.module.nas.algorithm import Darts, RL, GraphNasRL, Enas, RandomSearch
import numpy as np
from autogl.solver.utils import set_seed

set_seed(202106)

def test_model(model, data=None, check_children=False):
    """
    Test model interface.

    Interface
    ---------
    - model.from_hyper_parameter()
    - model.model.forward()
    - model.to()
    - model.initialize()
    """
    assert isinstance(model, BaseModel)
    assert hasattr(model, "to")
    assert hasattr(model, "initialize")
    model.initialize()
    model.to("cuda")
    if data is not None:
        data = data.to("cuda")

    assert hasattr(model, "model")
    __model = model.model
    assert isinstance(__model, torch.nn.Module)

    if data is not None:
        __model.forward(data)

    # FIXME: we can only perform tests when hyper_parameter_space is []
    if len(model.hyper_parameter_space) == 0:
        model_2 = model.from_hyper_parameter({})
        if check_children:
            test_model(model_2, data)


if __name__ == "__main__":

    print("Testing backend: {}".format("dgl" if DependentBackend.is_dgl() else "pyg"))

    if DependentBackend.is_dgl():
        dataset = CoraGraphDataset()
    else:
        dataset = Planetoid(os.path.expanduser("~/.cache-autogl"), "Cora")

    data = dataset[0]

    di = bk_feat(data).shape[1]
    do = len(np.unique(bk_label(data)))

    print("Random search + graphnas ")
    space = GraphNasNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = RandomSearch(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("Random search + singlepath ")
    space = SinglePathNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = RandomSearch(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("rl + graphnas ")
    space = GraphNasNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = RL(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("graphnasrl + graphnas ")
    space = GraphNasNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = GraphNasRL(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("enas + graphnas ")
    space = GraphNasNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = Enas(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("darts + graphnas ")
    space = GraphNasNodeClassificationSpace(con_ops=['concat']).cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = Darts(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)
    
    print("darts + singlepath ")
    space = SinglePathNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = Darts(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("Random search + graphnas macro")
    space = GraphNasMacroNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = RandomSearch(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)

    print("RL + graphnas macro")
    space = GraphNasMacroNodeClassificationSpace().cuda()
    space.instantiate(input_dim=di, output_dim=do)
    esti = OneShotEstimator()
    algo = RL(num_epochs=10)
    model = algo.search(space, dataset, esti)
    test_model(model, data, True)
