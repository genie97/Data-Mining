import operator

predict = open("output.txt", "r", encoding="utf-8")
answer = open("answer.txt", "r", encoding="utf-8")

predicts = list()
answers = list()

lines = predict.readlines()

for line in lines:
    percents = list()
    cate_prts = line.split("\t")
    for cate_perc in cate_prts:
        percents.append(cate_perc)
    index, value = max(enumerate(percents), key=operator.itemgetter(1))
    predicts.append(index)  # max값을 가지는 인덱스 저장
predict.close()

lines = answer.readlines()
for line in lines:
    answers.append(int(line))  # answer에서 읽어온 카테고리 넘버 저장
answer.close()

match = 0
for index in range(len(predicts)):
    if predicts[index] == answers[index]:
        match += 1

# pool matrix 구하는 곳 (전체 데이터를 T/F 상태로 나누는 것)
TP = list(0 for _ in range(9))
FP = list(0 for _ in range(9))
FN = list(0 for _ in range(9))

for index in range(len(predicts)):
    if predicts[index] == answers[index]:
        TP[predicts[index]] += 1
    else:
        FP[predicts[index]] += 1
        FN[answers[index]] += 1

total_TP = 0
total_FP = 0
total_FN = 0

for index in range(9):
    total_TP += TP[index]
    total_FP += FP[index]
    total_FN += FN[index]

# 각 카테고리에 대해서 각각 T/F 나누기
precisions = list(0 for _ in range(9))
recalls = list(0 for _ in range(9))

for index in range(9):
    if TP[index] == 0:
        precisions[index] = 0
        recalls[index] = 0
    else:
        precisions[index] = TP[index] / (TP[index] + FP[index])
        recalls[index] = TP[index] / (TP[index] + FN[index])
avg_precision = 0
avg_recall = 0
for index in range(9):
    avg_precision += precisions[index]
    avg_recall += recalls[index]
avg_precision /= 9
avg_recall /= 9

total_precision = total_TP / (total_TP + total_FP)
total_recall = total_TP / (total_TP + total_FN)
Micro_F1 = 2 * total_precision * total_recall / (total_precision + total_recall)
Macro_F1 = 2 * avg_precision * avg_recall / (avg_precision + avg_recall)

print(">> Performance\n- Macro_F1: %f\n\n- Total Precision: %f\n- Total Recall: %f\n- Micro_F1: %f" % (Macro_F1, total_precision, total_recall, Micro_F1))
print("- Accuracy: " + str(match / len(predicts)))

# precision: 원래 A인 카테고리 수 / A라고 예측한 총 결과 수
# Recall: A라고 예측한 수 / 카테고리가 A인 총 수
# Macro-averaging F1: 각 카테고리의 precision과 recall을 계산
# Micro-averaging F1: T,F Pooled matrix를 구해서 recall과 precision계산
