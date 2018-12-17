from enum import Enum
import pandas as pd
import sys

# Passive or Active
class MoleculeType(Enum):
    PASSIVE = 1
    ACTIVE = 2

# データを格納するクラス
class Data:
    def __init__(self):
        self.dat_data = None
        self.rtt_data = None
        self.adjust_data = None
        self.collision_data = None
        self.retransmission_data = None

        self.column_array = ["File Name", "Mean", "Median", "Var", "Std", "Min", "Max"]

    def get_value(self, target_type):
        from src.draw_graph import Target, Parameter
        # Target
        # if type(target_type) is Target:
        if self.rtt_data is None:
            from src.parser import parse_rtt
            fname = "./result/batch_" + self.dat_data.output_file_name
            self.rtt_data = parse_rtt(fname)

        if isinstance(target_type, Target):
            if target_type is Target.Mean:
                return self.rtt_data.mean
            elif target_type is Target.Median:
                return self.rtt_data.median
            elif target_type is Target.Jitter:
                return self.rtt_data.std
            elif target_type is Target.CollisionNum:
                if self.collision_data is None:
                    from src.parser import parse_coll
                    fname = "./result/collision_batch_" + self.dat_data.output_file_name
                    self.collision_data = parse_coll(fname)
                return self.collision_data.collision_num
            elif target_type is Target.DecomposingNum:
                if self.collision_data is None:
                    from src.parser import parse_coll
                    fname = "./result/collision_batch_" + self.dat_data.output_file_name
                    self.collision_data = parse_coll(fname)
                return self.collision_data.decomposing_num
            elif target_type is Target.LastDuplication:
                if self.adjust_data is None:
                    from src.parser import parse_adjust
                    fname = "./result/adjust_batch_" + self.dat_data.output_file_name
                    import os
                    if not os.path.exists(fname):
                        return -1
                    self.adjust_data = parse_adjust(fname)
                return self.adjust_data.last_num
            elif target_type is Target.LastMolecularNumber:
                if self.collision_data is None:
                    from src.parser import parse_coll
                    fname = "./result/collision_batch_" + self.dat_data.output_file_name
                    self.collision_data = parse_coll(fname)
                if self.collision_data.last_num == -1:
                    self.collision_data.calc_last_num(self)
                return self.collision_data.last_num
            # 再考の余地あり
            # ~回以上で失敗にする
            elif target_type is Target.FailureRate:
                if self.retransmission_data is None:
                    from src.parser import parse_retransmission
                    fname = "./result/retransmission_batch_" + self.dat_data.output_file_name
                    self.retransmission_data = parse_retransmission(fname)
                return len([i for i in self.retransmission_data.failure_flg if i == "F"]) / self.rtt_data.count

            elif target_type is Target.CumProb:
                _, _, Y =  self.rtt_data.create_plot_data()
                return Y

            elif target_type is Target.FailureRate5:
                if self.retransmission_data is None:
                    from src.parser import parse_retransmission
                    fname = "./result/retransmission_batch_" + self.dat_data.output_file_name
                    self.retransmission_data = parse_retransmission(fname)
                retransmit_time = [i for i in self.retransmission_data.retransmit_arr if i >= 5]
                return len(retransmit_time)

        # Parameter
        elif isinstance(target_type, Parameter):
            if target_type is Parameter.Distance:
                return self.dat_data.distance
            elif target_type is Parameter.Duplication:
                return self.dat_data.duplication
            elif target_type is Parameter.AdjustNum:
                return self.dat_data.adjust_num
            elif target_type is Parameter.MessageNum:
                return self.dat_data.message_num
            elif target_type is Parameter.Decomposing:
                return self.dat_data.decomposing
            else:
                print("isinstance in data not defined {}...".format(target_type.name))
                sys.exit(1)

    def get_xrange(self):
        X, _, _ =  self.rtt_data.create_plot_data()
        return X

    def get_column(self):
        return self.column_array

    def to_array(self):
        if self.rtt_data is None:
            from src.parser import parse_rtt
            self.rtt_data = parse_rtt("./result/batch_" + self.dat_data.output_file_name)
        fname = self.dat_data.dat_file_name.split('/')[1]
        mean = self.rtt_data.mean
        median = self.rtt_data.median
        var = self.rtt_data.var
        std = self.rtt_data.std
        minimum = self.rtt_data.minimum
        maximum = self.rtt_data.maximum

        return_array = [fname, mean, median, var, std, minimum, maximum]

        # Adjust
        # if not self.adjust_data is None:
        if not self.dat_data.adjust_num == 0:
            if self.adjust_data is None:
                from src.parser import parse_adjust
                fname = "./result/adjust_batch_" + self.dat_data.output_file_name
                import os
                if not os.path.exists(fname):
                    return -1
                self.adjust_data = parse_adjust(fname)
            self.column_array.append("Last Duplication Number")
            return_array.append(self.adjust_data.last_num)

        # Decomposing
        # if not self.dat_data.decomposing == 0:
        #     if self.collision_data is None:
        #         from src.parser import parse_coll
        #         fname = "./result/collision_batch_" + self.dat_data.output_file_name
        #         self.collision_data = parse_coll(fname)
        #     self.column_array.append("Decomposing Number")
        #     return_array.append(self.collision_data.decomposing_num)
        #
        #     if self.collision_data.last_num == -1:
        #         self.collision_data.calc_last_num(self)
        #     self.column_array.append("Molecular Num in Environment")
        #     return_array.append(self.collision_data.last_num)
        if self.collision_data is None:
            from src.parser import parse_coll
            fname = "./result/collision_batch_" + self.dat_data.output_file_name
            self.collision_data = parse_coll(fname)
        self.column_array.append("Decomposing Number")
        return_array.append(self.collision_data.decomposing_num)

        if self.collision_data.last_num == -1:
            self.collision_data.calc_last_num(self)
        self.column_array.append("Molecular Num in Environment")
        return_array.append(self.collision_data.last_num)

        return return_array


## Parameter ##
"""
# 環境
distance: 距離
duplication: 複製数
message_num: メッセージ数
rto: retransmitWaitTime(タイムアウト待ち時間)

# 分子
step_length: 1stepで移動する距離
diameter: 分子の半径

# オプション
molecule_type: PASSIVE or ACTIVE
decomposing: 0 ~ 3
adjust_num: True(数) or False(0)
is_fec: True or False
fecRequirePacket:必要数
fecRate:レート
packetStepLength: 1stepで移動する距離
packetDiameter: 分子の半径
outputFile: 出力ファイル名
"""
class DatData:
    def __init__(self, fname):
        self.dat_file_name = fname

"""
rtt: 全ての結果を格納
mean: 平均
median: 中央値
var: 分散
std: 標準偏差
num: シミュレーション回数
minimum: 最小値
maximum: 最大値
count: シミュレーション回数
"""
class RTTData:
    def __init__(self):
        self.rtt = []

    def create_plot_data(self):
        X = [0]
        Y1 = [0]
        Y2 = [0]
        count = 0
        prob = 0.0
        cum_prob = 0.0

        # plot_range = self.maximum / 100.0
        plot_range = 1000
        head = 0
        tail= plot_range

        index = 0

        while index < len(self.rtt):
            # 範囲内の時
            if self.rtt[index] < tail:
                count += 1
                index += 1
            # 範囲外になったら
            else:
                prob = float(count) / len(self.rtt) * 100
                cum_prob += prob
                X.append(tail)
                Y1.append(prob)
                Y2.append(cum_prob)
                count = 0
                head += plot_range
                tail += plot_range

        return X, Y1, Y2

"""
last_info_num: 最終infomation moleculeの個数の平均
last_ack_num: 最終ackowledgement moleculeの個数の平均
last_info_num: 最終moleculeの個数の平均
"""
class AdjustData:
    def __init__(self):
        pass

"""
collision_num: 衝突回数
decomposing_num: 消滅させた回数
last_num: 最後に環境に残っていた分子の数
"""
class CollisionData:
    def __init__(self):
        self.last_num = -1

    def calc_last_num(self, data):
        if data.retransmission_data is None:
            from src.parser import parse_retransmission
            fname = "./result/retransmission_batch_" + data.dat_data.output_file_name
            data.retransmission_data = parse_retransmission(fname)

        """
        + 再送信回数 * duplication
        + メッセージ送信回数 * 試行回数 * duplication * 2(info and ack)
        - decomposing_num
        """
        self.last_num = data.dat_data.duplication * data.retransmission_data.retransmit_num
        self.last_num += data.dat_data.message_num * data.dat_data.duplication * data.rtt_data.count * 2
        self.last_num -= self.decomposing_num

"""
retransmit_num: 再送信回数
failure_flg: 失敗(ファイル内)
"""
class RetransmissionData:
    def __init__(self):
        self.failure_flg = []
