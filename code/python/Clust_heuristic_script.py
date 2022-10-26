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


def clustering_metrics_true_labels(data_folder,clustering_folder,evaluation_folder,dataname):
    data_label_path = data_folder + dataname + '_with_clust_labels.txt'
    clustering_path = clustering_folder + dataname +'_k_means_clust_labels.csv'
    eval_path = evaluation_folder + dataname+'_k_means_clust_eval_with_true_label.csv'

    if isfile(clustering_path) and ~isfile(eval_path):
        labels_pred_table=pd.read_csv(clustering_path)
        klist = labels_pred_table.columns[2:]
        # breakpoint()
        n,d,X,labels_true = read_sample_labels(data_label_path)

        true_k = len(set(labels_true))

        metric_scores_summary=pd.DataFrame()
        metric_scores_summary['k']= np.append(klist,true_k)

        metrics_list_extrin= [normalized_mutual_info_score,
        mutual_info_score,homogeneity_score,fowlkes_mallows_score,
        # cluster.contingency_matrix, cluster.pair_confusion_matrix, v_measure_score,
        completeness_score, adjusted_rand_score,adjusted_mutual_info_score]

        metrics_list_intrin = [calinski_harabasz_score,davies_bouldin_score,silhouette_score]

		# if_k_true = []
        for func in metrics_list_extrin:
            metric_scores =[]
            for k in klist:

                labels_pred = labels_pred_table[k]
                print("Preidcted labesl view:.{}\n".format(labels_pred[:10]))
                print("True labesl view:.{}\n".format(labels_true[:10]))
                # print("Diff counts:{}\n".format(sum( x!=int(y) for x, y in zip(labels_pred,labels_true))))
                metric_scores.append(func(labels_true,labels_pred))

        #  add row for the ground true label
            metric_scores.append(func(labels_true,labels_true))

            metric_scores_summary[func.__name__]=metric_scores

        for func in metrics_list_intrin:
            metric_scores =[]

            for k in klist:

            	labels_pred = labels_pred_table[k]
            	# print(labels_pred)
            	# print(labels_true)
            	metric_scores.append(func(X,labels_pred))

        #  add row for the ground true label
            metric_scores.append(func(X,labels_true))
            metric_scores_summary[func.__name__]=metric_scores

        metric_scores_summary.to_csv(eval_path)

def combinefile(datafolderpath,filefolderpath,combinedpath):
	data_list = [f.split(".")[0] for f in listdir(datafolderpath)
	if isfile(filefolderpath+f.split(".")[0]+"_k_means_clust_eval_with_true_label.csv") and  "_k_means_clust_labels" not in f ]

	print(data_list)
	# newpd= pd.read_csv(filefolderpath+data_list[0]+"_clust_eval.csv")

	combined_csv = pd.concat([pd.read_csv(filefolderpath+f+"_k_means_clust_eval_with_true_label.csv",index_col=0).assign(dataname=f)
		for f in data_list])

	combined_csv_firstcol= combined_csv.pop('dataname')
	combined_csv.insert(0,'dataname',combined_csv_firstcol)

	summary_csv = combined_csv.sort_values(by=['dataname','k'])




	summary_csv.to_csv(combinedpath, index=False, encoding='utf-8-sig')





def main():
    data_folder='/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/input_data_for_exact_solver/real_data/'
    results_folder='/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/Results/Results_clustering/Other_Clustering/'
    evaluation_folder='/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/Results/Results_quality_of_clusters/other_methods'
    summaryfile = '/Users/shzhao/Documents/GitHub/Exact_clustering_SOS_SDP/Results/Results_quality_of_clusters/other_methods/real_data_summary_all_label_clust_eval.csv'


    dataname_real_list=['dermatology','ecoli','glass','haberman','heart-statlog','iono','iris','sonar','tae',
    'thy','wine','wisc','zoo']
    dataname_artficial_list=['3-spiral','3MC','blobs','flame','gaussians1','insect',
    'jain','lsun','pathbased','zelnik1','zelnik2','zelnik6']
    heu_list=[k_means]

    for data in dataname_real_list:
        # for heu in heu_list:
            # clustering_heu_method(results_folder,data_folder,data,heu)
        clustering_metrics_true_labels(data_folder,results_folder,evaluation_folder,data)
    combinefile(data_folder,evaluation_folder,summaryfile)


if __name__=='__main__':
    main()
