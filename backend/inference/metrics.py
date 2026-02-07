def acc_fn(y_preds, y_true):
    return len(y_preds[y_preds == y_true]) / len(y_preds)