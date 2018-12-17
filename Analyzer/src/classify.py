from enum import Enum
from src.draw_graph import Target
from src.formatter import dict_to_plot_data, dict_to_plot_data_for_cumprob
import sys

def classify_dict(data_dict, x_param, target_type, label_params):
    depth = 1
    return_dict = data_dict

    flg = True
    for param in label_params:
        return_dict = classify_dict_by_param(return_dict, param, depth, flg)
        flg = False
        depth += 1

    return dict_to_plot_data(return_dict, x_param, target_type, label_params)

def classify_dict_for_cumprob(data_dict, params, classify_params):
    depth = 1
    return_dict = data_dict

    flg = True
    for param in classify_params:
        return_dict = classify_dict_by_param(return_dict, param, depth, flg)
        flg = False
        depth += 1

    return dict_to_plot_data_for_cumprob(return_dict, params, classify_params)

def classify_dict_by_data(data_dict, params):
    depth = 1
    return_dict = data_dict

    flg = True
    for param in params:
        return_dict = classify_dict_by_param(return_dict, param, depth, flg)
        flg = False
        depth += 1

    return return_dict

# 再起関数
# 深さMaxならパラメータで分ける
# そうでなければ一段深く
def classify_dict_by_param(datas, param, depth, flg):
    return_dict = {}
    if flg:
        for data in datas.values():
            # dict分け
            classify_value = data.get_value(param)
            # まだ追加してなかったら配列初期化
            if not classify_value in return_dict.keys():
                return_dict[classify_value] = []
            return_dict[classify_value].append(data)
        return return_dict
    else:
        if depth == 1:
            for data in datas:
                # dict分け
                classify_value = data.get_value(param)
                # まだ追加してなかったら配列初期化
                if not classify_value in return_dict.keys():
                    return_dict[classify_value] = []
                return_dict[classify_value].append(data)
            return return_dict
        else:
            current_depth = depth - 1
            for key, dict in datas.items():
                return_dict[key] = classify_dict_by_param(dict, param, current_depth, flg)
            return return_dict
