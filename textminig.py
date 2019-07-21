from pathlib import Path
from collections import Counter, OrderedDict#Counting library
import codecs#encoding library

p = Path('./Input_Data').glob('**/*.txt')  # read text fil under all directory
word_list = []

for index in p:
    f = codecs.open(index, 'r', 'utf-8')
    lines = f.readlines() # read sentences in a file
    f.close()
    for line in lines:
        line = line.replace('\n', '').split('\t')#split "tab"
        for noun in line:
            words = noun.split('+') # split "+"
            for word in words:
                if '/NNG' in word or '/NNP' in word:#put word included NNG/NNP in list
                   word_list.append(word)
result = Counter(word_list)
sort_result = sorted(result.items(), key=lambda x:(-x[1], x[0]))
sort_result = sort_result[:5022]
dict_result = OrderedDict(sort_result)
out_f = open('Output.txt', mode='wt', encoding='utf-8')

for index, key in enumerate(dict_result):
    out_f.write(f"{key}\t{dict_result[key]}\n")

out_f.close()
