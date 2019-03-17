import matplotlib.pyplot as plt
from matplotlib import ticker
from enum import IntEnum

COLOR_LIST = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'r', 'g', 'b', 'm', 'c', 'y', 'k']
LABELS = ["30", "50", "70", "90"]
X = [10, 20, 30, 50, 100]
XLABEL = ["1→10", "10→20", "20→30", "30→50", "50→100"]
YLABEL = ["Comparative Mean Performance", "Comparative Median Performance", "Comparative Jitter Performance"]

class Target(IntEnum):
    MEAN = 0
    MEDIAN = 1
    JITTER = 2

def draw_graph(Y, target_type):
    fig_name = "./figs/"
    if target_type == 0:
        fig_name = fig_name + "pass_compare_mean.png"
    elif target_type == 1:
        fig_name = fig_name + "pass_compare_median.png"
    elif target_type == 2:
        fig_name = fig_name + "pass_compare_jitter.png"
    index = 0
    for y in Y:
        plt.plot(X, y, color=COLOR_LIST[index], label="Distance: " + LABELS[index])
        index += 1
    plt.xlabel("The number of Duplication")
    plt.ylabel(YLABEL[int(target_type)])
    plt.legend(loc="best")
    plt.grid(True)
    plt.xticks(X, XLABEL)
    plt.savefig(fig_name, dpi=90, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')

def main():
    Y_mean = []
    Y_median = []
    Y_jitter = []
    file_name = './data.txt'
    with open(file_name) as f:
        y_mean = []
        y_median = []
        y_jitter = []

        for line in f:
            if line == "\n":
                Y_mean.append(y_mean)
                Y_median.append(y_median)
                Y_jitter.append(y_jitter)

                y_mean = []
                y_median = []
                y_jitter = []
            else:
                datas = line.split(',')
                y_mean.append(float(datas[0].strip()))
                y_median.append(float(datas[1].strip()))
                y_jitter.append(float(datas[2].strip()))
        Y_mean.append(y_mean)
        Y_median.append(y_median)
        Y_jitter.append(y_jitter)

    draw_graph(Y_mean, Target.MEAN)
    draw_graph(Y_median, Target.MEDIAN)
    draw_graph(Y_jitter, Target.JITTER)

if __name__ == '__main__':
    main()
