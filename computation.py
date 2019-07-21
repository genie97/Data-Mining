import re, os, glob, math
from collections import OrderedDict, Counter

root_dir = './Corpus'
word_dic = dict()
word_list = list()
s_word_dic = dict()
pos_dic = dict()
word_count_dic = dict()

folder = ['Input_Data', 'Test_Data', 'Val_Data']
Folder_name = ['./Input_Data/', './Test_Feature_Data/', './Val_Data/']
cate_name = ['child/', 'culture/', 'economy/', 'education/', 'health/', 'life/', 'person/', 'policy/', 'society/']


def makeWordDict():
    files = sorted(glob.glob("./Corpus/Input_Data/*/*.txt", recursive=True))
    for file_name in files:
        with open(file_name, "r", encoding="utf-8") as f:
            lines = ''.join(f.readlines()).replace('\n', '\t')
        pattern = re.compile('(?![\t+])[가-힣]+/(NNP|NNG)', re.MULTILINE)
        for m in pattern.finditer(lines):
            word = lines[m.start():m.end()]
            word_list.append(word)
            if word not in word_dic:
                word_dic[word] = 1
            else:
                word_dic[word] += 1
    s_word_dic.update(OrderedDict(sorted(word_dic.items(), key=lambda x: (-x[1], x[0]))[:5022]))
    output_file = open("./Output1.txt", mode="wt", encoding="utf-8")

    for index, key in enumerate(s_word_dic):
        output_file.write(f"{key}\t{s_word_dic[key]}\n")

    output_file.close()


def get_tf_idf():
    for data_dir in os.listdir(root_dir):
        for categories in os.listdir(os.path.join(root_dir, data_dir)):
            for file_name in glob.glob(os.path.join(root_dir, data_dir, categories) + '/*.txt'):
                with open(file_name, "r", encoding="utf-8") as f:
                    lines = ''.join(f.readlines()).replace('\n', '\t')
                pattern = re.compile('(?![\t+])[가-힣]+/(NNP|NNG)', re.MULTILINE)
                temp_list = list()
                for m in pattern.finditer(lines):
                    word = lines[m.start():m.end()]
                    temp_list.append(word)
                total = len(temp_list)
                TF_IDF = s_word_dic.fromkeys(s_word_dic, 0)
                document = OrderedDict(sorted(Counter(temp_list).items(), key=lambda x: (-x[1], x[0])))
                # 한 파일 내에 있는 단어 수 / 한 문서에 있는 명사 수
                for key in document.keys():
                    if key in TF_IDF.keys():
                        TF_IDF[key] = document[key] / total * math.log10(1607 / (word_count_dic[key] + 1))
                written = '\t'.join("%f" % val for val in OrderedDict(sorted(TF_IDF.items())).values())
                out_path = os.path.join('./result', data_dir, categories)
                os.makedirs(out_path, exist_ok=True)
                with open(os.path.join(out_path, os.path.basename(file_name)), 'w+') as f:
                    f.write(f"{written}")


# 전체 딕셔너리 만들기 key: 경로 value: 해당 경로에 존재하는 단어 dictionary
def make_doc_freq():
    for category in os.listdir(os.path.join(root_dir, 'Input_Data')):
        for file_name in glob.glob(os.path.join(root_dir, 'Input_Data', category) + '/*.txt'):
            with open(file_name, "r", encoding="utf-8") as f:
                lines = ''.join(f.readlines()).replace('\n', '\t')
            pattern = re.compile('(?![\t+])[가-힣]+/(NNP|NNG)', re.MULTILINE)
            temp_list = list()
            for m in pattern.finditer(lines):
                word = lines[m.start():m.end()]
                temp_list.append(word)
            pos_dic[file_name] = OrderedDict(sorted(Counter(temp_list).items(), key=lambda x: (-x[1], x[0])))

        for key, value in pos_dic.items():
            for word in value.keys():
                if word in word_count_dic:
                    word_count_dic[word] = +1
                else:
                    word_count_dic[word] = 1

    # for key in pos_dic.keys():
    #      print(f"{key}\t{pos_dic[key]}")


def main():
    makeWordDict()
    make_doc_freq()
    get_tf_idf()


if __name__ == "__main__":
    main()
