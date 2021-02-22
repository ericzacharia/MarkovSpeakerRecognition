"""
MPCS 51042 S'20: Markov models and hash tables

Eric Zacharia
"""
import sys
import markov
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    if len(sys.argv) != 6 and len(sys.argv) != 7:
        print('Incorrect number of arguments!')
    else:
        if len(sys.argv) == 6:
            speaker_a = sys.argv[1]
            speaker_b = sys.argv[2]
            unknown_speech = sys.argv[3]
            k = int(sys.argv[4])
        else:  # len(sys.argv) == 7
            speaker_a = sys.argv[2]
            speaker_b = sys.argv[3]
            unknown_speech = sys.argv[4]
            k = int(sys.argv[5])
        with open(speaker_a, 'r') as spa:
            temp = spa.read()
            spa = ''
            for line in temp:
                spa += line + ' '
            with open(speaker_b, 'r') as spb:
                temp = spb.read()
                spb = ''
                for line in temp:
                    spb += line + ' '
                with open(unknown_speech, 'r') as spc:
                    temp = spc.read()
                    spc = ''
                    for line in temp:
                        spc += line + ' '

        if sys.argv[1] == 'p':  # Performance Measurement Mode
            runs = int(sys.argv[6])
            rt = pd.DataFrame()  # 'Implementation': , 'K': , 'Run': , 'Time':
            row = 0
            for i in range(k):
                for j in range(runs):
                    start = time.perf_counter()
                    dict_time = markov.identify_speaker(spa, spb, spc, k, 0)
                    end = time.perf_counter()
                    elapsed_time = float(f'{end - start: 0.3f}')
                    rt.loc[row, 'Implementation'] = 'Hashtable'
                    rt.loc[row, 'K'] = int(i + 1)
                    rt.loc[row, 'Run'] = int(j + 1)
                    rt.loc[row, f'Average Time (Runs={runs})'] = elapsed_time
                    row += 1

            for i in range(k):
                for j in range(runs):
                    start = time.perf_counter()
                    dict_time = markov.identify_speaker(spa, spb, spc, k, 1)
                    end = time.perf_counter()
                    elapsed_time = float(f'{end - start: 0.3f}')
                    rt.loc[row, 'Implementation'] = 'dict'
                    rt.loc[row, 'K'] = int(i + 1)
                    rt.loc[row, 'Run'] = int(j + 1)
                    rt.loc[row, f'Average Time (Runs={runs})'] = elapsed_time
                    row += 1

            print(rt)
            sns.set(style="whitegrid")
            '''
            The data frame is plotted after grouping rows together, primarily by implementation, secondarily by K, by
            taking the average run time, using the .groupby().mean() method. The .reset_index() method resets the column 
            titles in the rearranged data frame to match the original data frame column titles, sans the Number of Runs
            column since it was discarded after averaging Run Time rows, for the purpose of graphing with seaborn.
            '''
            ax = sns.pointplot(x='K', y=f'Average Time (Runs={runs})', hue='Implementation', linestyle='-', marker='o',
                               data=rt.groupby(['Implementation', 'K'])[f'Average Time (Runs={runs})'].mean()
                               .reset_index())
            ax.set_title('Hashtable vs Python dict')
            ax.grid(True)
            plt.show()
            plt.savefig("execution_graph.png")

        else:  # Normal Mode
            state = int(sys.argv[5])
            spa_prob, spb_prob, conclusion = markov.identify_speaker(spa, spb, spc, k, state)
            print(f'Speaker A: {spa_prob}')
            print(f'Speaker B: {spb_prob}')
            print()
            print(f'Conclusion: Speaker {conclusion} is most likely')
