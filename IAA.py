# Filename: IAA.py
# Description: Calculates the Inner Annotation Agreement Fleiss Kappa
# from the annotations of three annotators annotating evidence types
# Date: 3-04-2022
# Author: F.R.P. Stolk

""" Packages """
import csv
import json
import ast
import collections
import pandas as pd
import statsmodels

def read_csv(csv_file):
    """ reads csv and puts it in a list"""
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        x = 0
        labels = []
        dlabels = {}
        for line in csv_reader:
            if x > 0:
                if line[5] == "Continue":
                    line[5] = labels[x-2][2]
                labels.append((line[0],line[2], line[5], line[7]))
                dlabels[line[2]] = line[5]
            x +=1

    return labels, dlabels


def calculate_kappa(robin, marieke, friso,rd,md,fd):
    """ calculates kappa """
    x = 0
    y = 0
    r = 0
    testimony = 0
    statisticsstudy = 0
    commonground = 0
    anecdote = 0
    definition = 0
    assumption = 0
    other = 0
    continue_ = 0
    none = 0
    dis = []
    l = {}
    Pi = 0
    agreement_r_f = 0
    agreement_r_m = 0
    agreement_f_m = 0
    final_set = []
    for k in rd.keys():
        try:
            # finds the goldenstandard
            if rd[k] == "":
                rd[k] = "None"
            if fd[k] == "":
                fd[k] == "None"
            if md[k] == "":
                md[k] = "None"
            if '{"choices":' in rd[k]:
                new = json.loads(rd[k])
                rd[k] = new["choices"][0]
            if '{"choices":' in md[k]:
                new = json.loads(str(md[k]))
                md[k] = new["choices"][0]
            if '{"choices":' in fd[k]:
                new = json.loads(fd[k])
                fd[k] = new["choices"][0]  
            if rd[k] == md[k] and md[k] == fd[k]:
                final_set.append((k,rd[k]))
                Pi += 1
                x +=1
            elif rd[k] == md[k] or rd[k] == fd[k] or md[k] == fd[k]:
                if rd[k] == md[k]:
                    final_set.append((k, rd[k]))
                if rd[k] == fd[k]:
                    final_set.append((k, rd[k]))
                if md[k] == fd[k]:
                    final_set.append((k, fd[k]))
                cal = 1/(3*2)* (1+ 2*2 -3)
                Pi += cal
                r +=1
            else:
                Pi += 0
                sentence = [k, rd[k], md[k], fd[k]]
                dis.append(sentence)
                y +=1
            if rd[k] in l.keys():
                l[rd[k]] = l[rd[k]] +1
            else:
                l[rd[k]] = 1
            if md[k] in l.keys():
                l[md[k]] = l[md[k]] + 1
            else:
                l[md[k]] = 1
            if fd[k] in l.keys():
                l[fd[k]] = l[fd[k]] + 1
            else:
                l[fd[k]] = 1
        except KeyError:
            print("keyerror")
    l.pop("")
    l["None"] = l["None"] + 1

    # calculate agreement with final set for annotators
    a_r = 0
    d_r = 0
    a_f = 0
    d_f = 0
    a_m = 0
    d_m = 0
    for l in final_set:
        if l[1] == rd[l[0]]:
            a_r +=1
        else:
            d_r +=1
        if l[1] == fd[l[0]]:
            a_f +=1
        else:
            d_f +=1
        if l[1] == md[l[0]]:
            a_m+=1
        else:
            d_m +=1


    # Finds the agreement per label


    print(a_r)
    print(d_r)
    print(a_f)
    print(d_f)
    print(a_m)
    print(d_m)




    # print(final_set)
    # print(x)
    # print(r)
    # print(y)
    # print(l)
    # print(Pi)
    return dis, final_set


def claculate_labels_kappa(rd,md,fd,l):
    rd = collections.OrderedDict(sorted(rd.items()))
    fd = collections.OrderedDict(sorted(fd.items()))
    md = collections.OrderedDict(sorted(md.items()))
    df = pd.DataFrame()
    # df.columns = ["Testimony", "Statistics/Study", "Common Ground", "Assumption", "Definition", "Anecdote", "Continue", "Other", "None"]
    x = 0
    # print(statsmodels.stats.inter_rater.fleiss_kappa(rd.values(), md.values(), fd.values()))


def main():
    robin, rd = read_csv("robin.csv")
    marieke, md = read_csv("marieke.csv")
    friso, fd = read_csv("friso.csv")
    dis, l = calculate_kappa(robin, marieke, friso, rd,md,fd)
    claculate_labels_kappa(rd,md,fd,l)
    f = open('./dis.csv', 'w')
    writer = csv.writer(f)
    for d in dis:
        writer.writerow(d)
    f.close()
    f = open("./data.csv", "w")
    writer = csv.writer(f)
    rd = collections.OrderedDict(sorted(rd.items()))
    fd = collections.OrderedDict(sorted(fd.items()))
    md = collections.OrderedDict(sorted(md.items()))
    for r,m,f in zip(rd.values(), fd.values(), md.values()):
        writer.writerow([r,m,f])

    f = open("./goldstandard.csv", "w")
    writer = csv.writer(f)
    for k in l:
        writer.writerow([k[0], k[1]])



    

if __name__ == '__main__':
    main()