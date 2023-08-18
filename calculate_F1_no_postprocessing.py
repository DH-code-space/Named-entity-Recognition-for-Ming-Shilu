import pandas as pd
import itertools
import matplotlib.pyplot as plt
import numpy as np
import json


def plot_confusion_matrix(cm, classes, total_count, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / np.array(total_count)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)

    fmt = '.4f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()


gt_path = 'testing_data_gt.json'
# predict_path = 'testing_data_gpt3.5output.txt'
predict_path = 'testing_data_gpt4output.txt'

with open(gt_path, 'rt', encoding='utf-8-sig') as fi1, open(predict_path, 'rt', encoding='utf-8') as fi2:
    gt_data = json.load(fi1)
    gt = [line["span"] for line in gt_data]
    predict = fi2.read().strip().replace("'", '"').split("\n")
    predict = [json.loads(line) for line in predict]
    confusion_matrix = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    total_person_gt, total_loc_gt, total_wei_gt, total_org_gt, total_official_gt = 0, 0, 0, 0, 0
    total_person_predict, total_loc_predict, total_wei_predict, total_org_predict, total_official_predict = 0, 0, 0, 0, 0

    counter = 0

    for line_gt, line_predict in zip(gt, predict):
        counter += 1
        gt_len, predict_len, correct_len = 0, 0, 0

        line_predict['LOC'], line_predict['WEI'], line_predict['ORG'] = [], [], []
        if line_predict['LOCWEIORG'][0] != "None":
            for entity in line_predict['LOCWEIORG']:
                entity = entity.split("(")
                if len(entity) == 1:
                    line_predict['OFFICIAL'].append(entity[0])
                elif entity[1][:-1] == "LOC":
                    line_predict['LOC'].append(entity[0])
                elif entity[1][:-1] == "WEI":
                    line_predict['WEI'].append(entity[0])
                elif entity[1][:-1] == "ORG":
                    line_predict['ORG'].append(entity[0])
                elif entity[1][:-1] == "PERSON":
                    line_predict['PERSON'].append(entity[0])
                elif entity[1][:-1] == "OFFICIAL":
                    line_predict['OFFICIAL'].append(entity[0])
    
        if len(line_predict['LOC']) == 0:
            line_predict['LOC'].append("None")
        if len(line_predict['WEI']) == 0:
            line_predict['WEI'].append("None")
        if len(line_predict['ORG']) == 0:
            line_predict['ORG'].append("None")
        
        if line_predict['PERSON'][0] != "None":
            person_after_processing = []
            for entity in line_predict['PERSON']:
                entity = entity.split("(")
                if len(entity) == 1:
                    person_after_processing.append(entity[0])
                elif entity[1][:-1] == "LOC":
                    line_predict['LOC'].append(entity[0])
                elif entity[1][:-1] == "WEI":
                    line_predict['WEI'].append(entity[0])
                elif entity[1][:-1] == "ORG":
                    line_predict['ORG'].append(entity[0])
                elif entity[1][:-1]  == "OFFICIAL":
                    line_predict['OFFICIAL'].append(entity[0])
            line_predict['PERSON'] = person_after_processing

        line_gt['PERSON'] = list(set(line_gt['PERSON']))
        line_gt['LOC'] = list(set(line_gt['LOC']))
        line_gt['WEI'] = list(set(line_gt['WEI']))
        line_gt['ORG'] = list(set(line_gt['ORG']))
        line_gt['OFFICIAL'] = list(set(line_gt['OFFICIAL']))

        line_predict['PERSON'] = list(set(line_predict['PERSON']))
        line_predict['LOC'] = list(set(line_predict['LOC']))
        line_predict['WEI'] = list(set(line_predict['WEI']))
        line_predict['ORG'] = list(set(line_predict['ORG']))
        line_predict['OFFICIAL'] = list(set(line_predict['OFFICIAL']))

        if line_gt['PERSON'][0] != "None":
            gt_len += len(line_gt['PERSON'])
            total_person_gt += len(line_gt['PERSON'])
        if line_gt['LOC'][0] != "None":
            gt_len += len(line_gt['LOC'])
            total_loc_gt += len(line_gt['LOC'])
        if line_gt['WEI'][0] != "None":
            gt_len += len(line_gt['WEI'])
            total_wei_gt += len(line_gt['WEI'])
        if line_gt['ORG'][0] != "None":
            gt_len += len(line_gt['ORG'])
            total_org_gt += len(line_gt['ORG'])
        if line_gt['OFFICIAL'][0] != "None":
            gt_len += len(line_gt['OFFICIAL'])
            total_official_gt += len(line_gt['OFFICIAL'])
        
        if line_predict['PERSON'][0] != "None":
            predict_len += len(line_predict['PERSON'])
            total_person_predict += len(line_predict['PERSON'])
        if line_predict['LOC'][0] != "None":
            predict_len += len(line_predict['LOC'])
            total_loc_predict += len(line_predict['LOC'])
        if line_predict['WEI'][0] != "None":
            predict_len += len(line_predict['WEI'])
            total_wei_predict += len(line_predict['WEI'])
        if line_predict['ORG'][0] != "None":
            predict_len += len(line_predict['ORG'])
            total_org_predict += len(line_predict['ORG'])
        if line_predict['OFFICIAL'][0] != "None":
            predict_len += len(line_predict['OFFICIAL'])
            total_official_predict += len(line_predict['OFFICIAL'])

        if line_predict['PERSON'][0] != "None":
            for entity in line_predict['PERSON']:
                if entity in line_gt['PERSON']:
                    correct_len += 1
                    confusion_matrix[0][0] += 1
                else:
                    if entity in line_gt['LOC']:
                        confusion_matrix[1][0] += 1
                    elif entity in line_gt['WEI']:
                        confusion_matrix[2][0] += 1
                    elif entity in line_gt['ORG']:
                        confusion_matrix[3][0] += 1
                    elif entity in line_gt['OFFICIAL']:
                        confusion_matrix[4][0] += 1
        
        if line_predict['LOC'][0] != "None":
            for entity in line_predict['LOC']:
                if entity in line_gt['LOC']:
                    correct_len += 1
                    confusion_matrix[1][1] += 1
                else:
                    if entity in line_gt['PERSON']:
                        confusion_matrix[0][1] += 1
                    elif entity in line_gt['WEI']:
                        confusion_matrix[2][1] += 1
                    elif entity in line_gt['ORG']:
                        confusion_matrix[3][1] += 1
                    elif entity in line_gt['OFFICIAL']:
                        confusion_matrix[4][1] += 1
        
        if line_predict['WEI'][0] != "None":
            for entity in line_predict['WEI']:
                if entity in line_gt['WEI']:
                    correct_len += 1
                    confusion_matrix[2][2] += 1
                else:
                    if entity in line_gt['PERSON']:
                        confusion_matrix[0][2] += 1
                    elif entity in line_gt['LOC']:
                        confusion_matrix[1][2] += 1
                    elif entity in line_gt['ORG']:
                        confusion_matrix[3][2] += 1
                    elif entity in line_gt['OFFICIAL']:
                        confusion_matrix[4][2] += 1

        if line_predict['ORG'][0] != "None":
            for entity in line_predict['ORG']:
                if entity in line_gt['ORG']:
                    correct_len += 1
                    confusion_matrix[3][3] += 1
                else:
                    if entity in line_gt['PERSON']:
                        confusion_matrix[0][3] += 1
                    elif entity in line_gt['LOC']:
                        confusion_matrix[1][3] += 1
                    elif entity in line_gt['WEI']:
                        confusion_matrix[2][3] += 1
                    elif entity in line_gt['OFFICIAL']:
                        confusion_matrix[4][3] += 1
        
        if line_predict['OFFICIAL'][0] != "None":
            for entity in line_predict['OFFICIAL']:
                if entity in line_gt['OFFICIAL']:
                    correct_len += 1
                    confusion_matrix[4][4] += 1
                else:
                    if entity in line_gt['PERSON']:
                        confusion_matrix[0][4] += 1
                    elif entity in line_gt['LOC']:
                        confusion_matrix[1][4] += 1
                    elif entity in line_gt['WEI']:
                        confusion_matrix[2][4] += 1
                    elif entity in line_gt['ORG']:
                        confusion_matrix[3][4] += 1

        precision = correct_len / predict_len
        recall = correct_len / gt_len
        if precision == 0 or recall == 0:
            print("%3d  precision: %.4f  recall: %.4f  F1: 0.0000  support: %2d" % (counter, precision, recall, gt_len))
        else:
            microF1 = 2 * precision * recall / (precision + recall)
            print("%3d  precision: %.4f  recall: %.4f  F1: %.4f  support: %2d" % (counter, precision, recall, microF1, gt_len))
    
    print("-------------------------------------------------------------------------------")

    person_precision = confusion_matrix[0][0] / total_person_predict
    person_recall = confusion_matrix[0][0] / total_person_gt
    person_f1 = 2 * person_precision * person_recall / (person_precision + person_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("PER:", person_precision, person_recall, person_f1, total_person_gt))

    loc_precision = confusion_matrix[1][1] / total_loc_predict
    loc_recall = confusion_matrix[1][1] / total_loc_gt
    loc_f1 = 2 * loc_precision * loc_recall / (loc_precision + loc_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("LOC:", loc_precision, loc_recall, loc_f1, total_loc_gt))

    wei_precision = confusion_matrix[2][2] / total_wei_predict
    wei_recall = confusion_matrix[2][2] / total_wei_gt
    wei_f1 = 2 * wei_precision * wei_recall / (wei_precision + wei_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("WEI:", wei_precision, wei_recall, wei_f1, total_wei_gt))

    org_precision = confusion_matrix[3][3] / total_org_predict
    org_recall = confusion_matrix[3][3] / total_org_gt
    org_f1 = 2 * org_precision * org_recall / (org_precision + org_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("ORG:", org_precision, org_recall, org_f1, total_org_gt))

    official_precision = confusion_matrix[4][4] / total_official_predict
    official_recall = confusion_matrix[4][4] / total_official_gt
    official_f1 = 2 * official_precision * official_recall / (official_precision + official_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("OFF:", official_precision, official_recall, official_f1, total_official_gt))

    micro_precision = (confusion_matrix[0][0] + confusion_matrix[1][1] + confusion_matrix[2][2] + confusion_matrix[3][3] + confusion_matrix[4][4]) \
        / (total_person_predict + total_loc_predict + total_wei_predict + total_org_predict + total_official_predict)
    micro_recall = (confusion_matrix[0][0] + confusion_matrix[1][1] + confusion_matrix[2][2] + confusion_matrix[3][3] + confusion_matrix[4][4]) \
        / (total_person_gt + total_loc_gt + total_wei_gt + total_org_gt + total_official_gt)
    micro_f1 = 2 * micro_precision * micro_recall / (micro_precision + micro_recall)
    print("%6s precision: %.4f  recall: %.4f  F1: %.4f  support: %4d" % ("MICRO:", micro_precision, micro_recall, micro_f1, total_person_gt + total_loc_gt + total_wei_gt + total_org_gt + total_official_gt))

    print("-------------------------------------------------------------------------------")

    plot_confusion_matrix(
        np.array(confusion_matrix),
        classes=["PERSON", "LOC", "WEI", "ORG", "OFFICIAL"],
        total_count=[total_person_gt, total_loc_gt, total_wei_gt, total_org_gt, total_official_gt],
        normalize=True,
        title="Confusion matrix"
    )

    plt.show()

    plot_confusion_matrix(
        np.array(confusion_matrix),
        classes=["PERSON", "LOC", "WEI", "ORG", "OFFICIAL"],
        total_count=[total_person_gt, total_loc_gt, total_wei_gt, total_org_gt, total_official_gt],
        normalize=False,
        title="Confusion matrix"
    )

    plt.show()