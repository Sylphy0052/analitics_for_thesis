from src.draw_graph import Target

def get_label(param, val):
    label = ""
    if param.name == "RTO":
        if val is True:
            label = "No SW-ARQ"
        else:
            label = "SW-ARQ"
    else:
        label = "{} {}".format(param.name, val)
    return label

def add_label(param, val):
    label = ""
    if param.name == "RTO":
        if val is True:
            label = " - No SW-ARQ"
        else:
            label = " - SW-ARQ"
    else:
        label = " - {} {}".format(param.name, val)
    return label

def dict_to_plot_data(data_dict, x_param, target_type, label_params):
    X = []
    Y = []
    labels = []

    for key, datas in data_dict.items():
        label = get_label(label_params[0], key)

        if isinstance(datas, dict):
            for k, vs in datas.items():
                tmp_label = label
                tmp_label += add_label(label_params[1], k)
                y = []
                for v in vs:
                    x = v.get_value(x_param)
                    if not x in X:
                        X.append(x)
                    y.append(v.get_value(target_type))
                Y.append(y)
                labels.append(tmp_label)
        else:
            y = []
            for data in datas:
                x = data.get_value(x_param)
                if not x in X:
                    X.append(x)
                y.append(data.get_value(target_type))
            Y.append(y)
            labels.append(label)

    return X, Y, labels

def dict_to_plot_data_for_cumprob(data_dict, params, classify_params):
    X = []
    Y = []
    labels = []

    for key, datas in data_dict.items():
        label = get_label(classify_params[0], key)

        if isinstance(datas, dict):
            import sys
            print("A")
            sys.exit(1)
            for k, vs in datas.items():
                tmp_label = label
                tmp_label += add_label(label_params[1], k)
                y = []
                for v in vs:
                    x = v.get_value(x_param)
                    if not x in X:
                        X.append(x)
                    y.append(v.get_value(target_type))
                Y.append(y)
                labels.append(tmp_label)
        else:
            for data in datas:
                tmp_label = label
                X.append(data.get_xrange())
                Y.append(data.get_value(Target.CumProb))
                for param in params:
                    tmp_label += add_label(param, data.get_value(param))
                labels.append(tmp_label)

    return X, Y, labels
