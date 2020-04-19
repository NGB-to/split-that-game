# VisualizePayLoad.py

from json import load
from glob import glob
import matplotlib.pyplot as plt

SRC_FILES = glob('Log_*.json')

for srcFile in SRC_FILES:
    with open(srcFile, 'r') as inputFile:
        jsonInput = load(inputFile)
        keys = jsonInput['files'].keys()
        fileEntries = [key.strip('\\/') for key in keys]
        plt.rcdefaults()
        plt.rcParams['figure.figsize'] = [70, len(keys) * 0.4]
        fig, ax = plt.subplots()
        cnt = []
        for key in keys:
            cnt.append(jsonInput['files'][key]['cnt'])

        ax.barh(fileEntries, cnt, align='center')
        ax.set_yticks(fileEntries)
        ax.set_yticklabels(fileEntries)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('File calls')
        ax.set_title(f"File usage")

        plt.savefig(f"{jsonInput['basedir']}.png")

