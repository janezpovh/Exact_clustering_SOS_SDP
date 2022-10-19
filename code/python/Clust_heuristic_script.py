import numpy as np
import csv
from sklearn.metrics import *
from sklearn.cluster import *
from os import listdir
from os.path import isfile,join
import pandas as pd
import sys
import inspect

def read_sample_labels(filepath):
    file = open(filepath,'r')
    X =[]
    labels=[]
    for fline in file.read().split('\n'):
        y = [x for x in fline.split()]
        # x = np.concatenate(x,np.asarray(y))
        if "class" in fline:
        	class_idx = y.index("\"class\"")
        elif "Class" in fline:
        	class_idx = y.index("\"Class\"")
        if len(y)==2:
            n,d =y[0],y[1]
        elif len(y) and "class" not in fline and "Class" not in fline:
            try:
                X.append([float(x.strip('"')) for x in y[:-1]])
                labels.append(y[class_idx].lstrip('\"').rstrip('\"'))
                d = len(y)-1
            except IndexError:
                breakpoint()
    n = len(X)
    return n,d,np.vstack(X),labels


def clustering_heu_method(results_folder,data_folder,dataname,heu):
    data_sample_path=data_folder+dataname+'_with_clust_labels.txt'
    results_path=results_folder+dataname+'_'+heu.__name__+'_clust_labels.csv'
    n,d,X,labels_true = read_sample_labels(data_sample_path)

    cluster_table=pd.DataFrame()
    cluster_table['true_label']=labels_true
    true_k = len(set(labels_true))

    k_list=range(max(2,true_k-2),true_k+3)

    # breakpoint()

    for k in k_list:
        # breakpoint()
        labels=heu(X,k)[1]
        cluster_table['{}'.format(k)]=labels

    # breakpoint()
    cluster_table.to_csv(results_path)
    # with open(results_path,"w") as outfile:
    #     writer =csv.writer(outfile)
    #     key_list=list(cluster_dict.keys())
    #     writer.writerow(cluster_dict.keys())
    #     writer.writerow([cluster_dict[x] for x in key_list])

def main():
    data_folder='/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/input_data_for_exact_solver/artificial_data/'
    results_folder='/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/Results/Results_clustering/Other_Clustering/'
    dataname_real_list=['dermatology','ecoli','glass','haberman','heart-statlog','iono','iris','sonar','tae',
    'thy','wine','wisc','zoo']
    dataname_artficial_list=['3-spiral','3MC','blobs','flame','gaussians1','insect',
    'jain','lsun','pathbased','zelnik1','zelnik2','zelnik6']
    # dataname_list = [f.split(".")[0] for f in listdir(data_folder)
	# if isfile(join(data_folder, f)) and "_with_clust_labels" not in f]
    heu_list=[k_means]

    for data in dataname_artficial_list:
        for heu in heu_list:
            clustering_heu_method(results_folder,data_folder,data,heu)


if __name__=='__main__':
    main()
