# データをなんやかんやするクラス
from src.common import get_file_list
from src.parser import parse_dat
from src.draw_graph import draw_rtt, draw_many_line_graph, Target, Parameter, draw_many_line_graph_for_cumprob
from src.data import Data
from src.classify import classify_dict, classify_dict_by_param, classify_dict_by_data, classify_dict_for_cumprob
import sys, os
import pandas as pd
from enum import IntEnum

class DatType(IntEnum):
    Normal = 1
    Decomposing = 2
    Adjust = 3

# Mainから生成される
class Analyzer:
    def __init__(self):
        self.data_dict = {}
        # ファイル一覧を取得
        self.all_file_list = get_file_list()
        # Dat fileを解析する
        self.parse_dat_file()

    def parse_dat_file(self):
        self.dat_dict = {}

        count = 0
        for fname in self.all_file_list:
            count += 1
            print("{}/{} Reading... {}".format(count, len(self.all_file_list), fname))
            data = Data()
            dat = parse_dat(fname)
            self.dat_dict[fname] = dat
            data.dat_data = dat
            self.data_dict[fname] = data

    # CSV fileに結果書き込み
    def write_info_csv(self):
        tmp_data = None
        csv_data = []
        for data in self.data_dict.values():
            csv_data.append(data.to_array())
            tmp_data = data
        df = pd.DataFrame(csv_data, columns=tmp_data.get_column())

        df.to_csv("result.csv")

    def draw_rtt_graph(self, dat_type):
        if dat_type == DatType.Normal:
            self.draw_normal_graph()
        elif dat_type == DatType.Decomposing:
            self.draw_decomposing_graph()
        elif dat_type == DatType.Adjust:
            self.draw_adjust_graph()

        for _, data in self.data_dict.items():
            draw_rtt(data)

    def draw_normal_graph(self):
        # ディレクトリ作成
        dir_path = "./result_fig/"
        if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

        # Mean
        fig_name = dir_path + "mean.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Mean, [Parameter.Duplication])
        # location = "upper left"
        location = "best"
        ax_labels = ["Tx Rx distance (um)", "Mean of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Median
        fig_name = dir_path + "median.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Median, [Parameter.Duplication])
        # location = "upper left"
        location = "best"
        ax_labels = ["Tx Rx distance (um)", "Median of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Jitter
        fig_name = dir_path + "jitter.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Jitter, [Parameter.Duplication])
        # location = "upper left"
        location = "best"
        ax_labels = ["Tx Rx distance (um)", "Jitter of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # CollisionNum
        fig_name = dir_path + "numberofcollision.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.CollisionNum, [Parameter.Duplication])
        # location = "upper left"
        location = "best"
        ax_labels = ["Tx Rx distance (um)", "The number of collision"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Failure Rate
        # fig_name = dir_path + "failurerate.png"
        # X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.FailureRate, [Parameter.Duplication])
        # location = "upper left"
        # location = "best"
        # ax_labels = ["Tx Rx distance (um)", "Failure Rate"]
        # draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # CumProb
        current_dict = classify_dict_by_param(self.data_dict, Parameter.Distance, 1, True)

        for k, v in current_dict.items():
            data_dict = {}
            for i in v:
                data_dict[i.dat_data.dat_file_name] = i

            fig_name = dir_path + "distance{}_cumprob.png".format(k)
            X, Y, labels = classify_dict_for_cumprob(data_dict, [Parameter.Duplication], [Parameter.Distance])
            # location = "lower right"
            location = "best"
            ax_labels = ["Steps", "Cumulative Probability(%)"]
            draw_many_line_graph_for_cumprob(X, Y, labels, ax_labels, location, fig_name)

        # Failure Rate is over 5
        fig_name = dir_path + "failurerate5.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.FailureRate5, [Parameter.Duplication])
        # location = "upper left"
        location = "best"
        ax_labels = ["Tx Rx distance (um)", "Failure Rate is over 5"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

    def draw_decompoing_graph(self):
        # ディレクトリ作成
        dir_path = "./result_fig/"
        if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

        current_dict = classify_dict_by_param(self.data_dict, Parameter.MessageNum, 1, True)

        for k, v in current_dict.items():
            data_dict = {}
            for i in v:
                data_dict[i.dat_data.dat_file_name] = i

            # Mean
            fig_name = dir_path + "message{}_mean.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.Mean, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "Mean of RTT (s)"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # Median
            fig_name = dir_path + "message{}_median.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.Median, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "Median of RTT (s)"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # Jitter
            fig_name = dir_path + "message{}_jitter.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.Jitter, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "Jitter of RTT (s)"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # CollisionNum
            fig_name = dir_path + "message{}_numberofcollision.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.CollisionNum, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "The number of collision"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # DecomposingNum
            fig_name = dir_path + "message{}_numberofdecomposing.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.DecomposingNum, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "The number of decomposing"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # DecomposingNum
            fig_name = dir_path + "message{}_lastmolecularnumber.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.LastMolecularNumber, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "The number of last molecule"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

            # Failure Rate
            fig_name = dir_path + "message{}_failurerate.png".format(k)
            X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.FailureRate, [Parameter.Duplication, Parameter.Decomposing])
            location = "upper left"
            ax_labels = ["Tx Rx distance (um)", "Failure Rate"]
            draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        current_dict = classify_dict_by_data(self.data_dict, [Parameter.MessageNum, Parameter.Duplication])

        for k1, v1 in current_dict.items():
            for k2, v2 in v1.items():
                data_dict = {}
                for i in v2:
                    data_dict[i.dat_data.dat_file_name] = i

                # DecomposingNum
                fig_name = dir_path + "duplication{}_message{}_numberofdecomposing.png".format(k2, k1)
                X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.DecomposingNum, [Parameter.Decomposing])
                location = "upper left"
                ax_labels = ["Tx Rx distance (um)", "The number of decomposing"]
                draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

                # DecomposingNum
                fig_name = dir_path + "duplication{}_message{}_lastmolecularnumber.png".format(k2, k1)
                X, Y, labels = classify_dict(data_dict, Parameter.Distance, Target.LastMolecularNumber, [Parameter.Decomposing])
                location = "upper left"
                ax_labels = ["Tx Rx distance (um)", "The number of last molecule"]
                draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

    def draw_adjust_graph(self):
        # ディレクトリ作成
        dir_path = "./result_fig/"
        if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

        # print(self.data_dict)
        # current_dict = classify_dict_by_param(self.data_dict, Parameter.MessageNum, 1, True)
        # print("===")
        # print(current_dict)
        # import sys; sys.exit(1)

        # for k, v in current_dict.items():
        # for k, v in self.data_dict.items():
        #     data_dict = {}
        #     for i in v:
        #         data_dict[i.dat_data.dat_file_name] = i

        # Mean
        fig_name = dir_path + "mean.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Mean, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "Mean of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Median
        fig_name = dir_path + "median.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Median, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "Median of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Jitter
        fig_name = dir_path + "jitter.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.Jitter, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "Jitter of RTT (s)"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # CollisionNum
        fig_name = dir_path + "numberofcollision.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.CollisionNum, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "The number of collision"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # DecomposingNum
        fig_name = dir_path + "lastmolecularnumber.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.LastMolecularNumber, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "The number of last molecule"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # Failure Rate
        fig_name = dir_path + "failurerate.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.FailureRate, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "Failure Rate"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)

        # draw_adjust
        fig_name = dir_path + "last_duplication.png"
        X, Y, labels = classify_dict(self.data_dict, Parameter.Distance, Target.LastDuplication, [Parameter.Duplication, Parameter.AdjustNum])
        location = "upper left"
        ax_labels = ["Tx Rx distance (um)", "Last Number of duplications"]
        draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name)
