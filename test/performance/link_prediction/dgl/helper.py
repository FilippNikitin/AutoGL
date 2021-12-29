def get_encoder_decoder_hp(model='gin', decoder=None):
    if model == 'gin':
        model_hp = {
            "num_layers": 5,
            "hidden": [64],
            "act": "relu",
            "eps": "False",
            "mlp_layers": 2,
            "neighbor_pooling_type": "sum"
        }
    elif model == 'gat':
        model_hp = {
            # hp from model
            "num_layers": 2,
            "hidden": [8],
            "heads": 8,
            "dropout": 0.0,
            "act": "elu",
        }
    elif model == 'gcn':
        model_hp = {
            "num_layers": 3,
            "hidden": [16, 16],
            "dropout": 0.,
            "act": "relu",
        }
    elif model == 'sage':
        model_hp = {
            'num_layers': 3,
            'hidden': [16, 16],
            'dropout': 0.0,
            'act': 'relu',
            'agg': 'mean'
        }
    elif model == 'topk':
        model_hp = {
            "num_layers": 5,
            "hidden": [64, 64, 64, 64]
        }
        
    return model_hp, {}
