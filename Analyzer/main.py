#!/usr/local/bin/python3
## sample main program
from src.analyzer import Analyzer, DatType

# Analyzerクラスを呼び出すだけ
def main():
    analyzer = Analyzer()
    analyzer.draw_rtt_graph(DatType.Normal)
    analyzer.write_info_csv()
    print("Complete!")

if __name__ == '__main__':
    main()
