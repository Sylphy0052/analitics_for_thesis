from src.parser import parse_rtt
import matplotlib.pyplot as plt
from matplotlib import ticker
import os
from enum import Enum

# グラフを描く関数

COLOR_LIST = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'r', 'g', 'b', 'm', 'c', 'y', 'k']
STYLE_LIST = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':']

class Target(Enum):
    Mean = 1
    Median = 2
    Jitter = 3 # Standard deviation
    CollisionNum = 4
    DecomposingNum = 5
    LastDuplication = 6
    LastMolecularNumber = 7
    FailureRate = 8
    CumProb = 9
    FailureRate5 = 10

class Parameter(Enum):
    Distance = 1
    Duplication = 2
    MessageNum = 3
    RTO = 4
    StepLength = 5
    MoleculeType = 6
    Decomposing = 7
    AdjustNum = 8
    IsFEC = 9
    FEC_Rate = 10

def draw_rtt(data):
    # RTT fileを読み込んでなかったら
    # if not data.is_rtt():
    if not data.rtt_data:
        fname = "./result/batch_" + data.dat_data.output_file_name
        data.rtt_data = parse_rtt(fname)

    dir_path = "./rtt_fig/"
    if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
    fig_name = dir_path + data.dat_data.output_file_name + ".png"
    if os.path.isfile(fig_name):
        print("{} is exist.".format(fig_name))
        return
    print("Draw {} in {}".format(fig_name.split('/')[2], dir_path.split('/')[1]))

    X, Y1, Y2 = data.rtt_data.create_plot_data()

    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(X, Y1, color=COLOR_LIST[0], label="Probability", linestyle=STYLE_LIST[0])
    ax2 = ax1.twinx()
    ln2 = ax2.plot(X, Y2, color=COLOR_LIST[1], label="Cumulative Probability", linestyle=STYLE_LIST[1])

    ax1.set_xlabel("RTT (s)")
    ax1.set_ylabel("Probability of RTT")
    ax2.set_ylabel("Cumulative Probability of RTT")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1+h2, l1+l2, loc="right")

    plt.grid(True)

    plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.gca().ticklabel_format(style="sci",  axis="x",scilimits=(0,0))

    plt.savefig(fig_name, dpi=90, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')

def draw_two_line_graph(X, Y1, Y2, labels, ax_labels, location, fig_name):
    plt.plot(X, Y1, color=COLOR_LIST[0], label=labels[0], linestype=STYLE_LIST[0])
    plt.plot(X, Y2, color=COLOR_LIST[1], label=labels[1], linestyle=STYLE_LIST[1])

    plt.xlabel(ax_labels[0])
    plt.ylabel(ax_labels[1])
    plt.legend(loc=location)

    plt.grid(True)
    plt.xticks(X)

    if max(X) > 10 ** 6:
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.gca().ticklabel_format(style="sci",  axis="x",scilimits=(0,0))
    if max(Y1) > 10 ** 6 or max(Y2) > 10 ** 6:
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.gca().ticklabel_format(style="sci",  axis="y",scilimits=(0,0))

    plt.savefig(fig_name, dpi=90, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')

def draw_many_line_graph(X, Y, labels, ax_labels, location, fig_name):
    for i in range(len(Y)):
        if not len(Y[i]) == len(X):
            continue
        if -1 in Y[i]:
            continue
        plt.plot(X, Y[i], color=COLOR_LIST[i], label=labels[i], linestyle=STYLE_LIST[i])

    plt.xlabel(ax_labels[0])
    plt.ylabel(ax_labels[1])
    plt.legend(loc=location)

    plt.grid(True)
    plt.xticks(X)

    if max(X) > 10 ** 6:
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.gca().ticklabel_format(style="sci",  axis="x",scilimits=(0,0))

    if max([max(i) for i in Y]) > 10 ** 6:
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        plt.gca().ticklabel_format(style="sci",  axis="y",scilimits=(0,0))

    plt.savefig(fig_name, dpi=90, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')

def draw_many_line_graph_for_cumprob(X, Y, labels, ax_labels, location, fig_name):
    tmp_X = []
    for x in X:
        if len(tmp_X) < len(x):
            tmp_X = x

    for i in range(len(Y)):
        if not len(Y[i]) == len(tmp_X):
            while len(Y[i]) != len(tmp_X):
                Y[i].append(100.0)
            # print("Error not equal length Y[i] and X")
            # continue
        if -1 in Y[i]:
            print("Error in Y[i]")
            continue
        plt.plot(tmp_X, Y[i], color=COLOR_LIST[i], label=labels[i], linestyle=STYLE_LIST[i])

    plt.xlabel(ax_labels[0])
    plt.ylabel(ax_labels[1])
    plt.legend(loc=location)

    plt.grid(True)

    step = int(tmp_X[-1] / 10)


    plt.xticks([i for i in range(0, tmp_X[-1], int(tmp_X[-1] / 10))])
    # plt.xticks(X)

    # if max(X) > 10 ** 6:
        # plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        # plt.gca().ticklabel_format(style="sci",  axis="x",scilimits=(0,0))

    plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.gca().ticklabel_format(style="sci",  axis="x",scilimits=(0,0))
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # if max([max(i) for i in Y]) > 10 ** 6:
    #     plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    #     plt.gca().ticklabel_format(style="sci",  axis="y",scilimits=(0,0))

    plt.savefig(fig_name, dpi=90, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')
