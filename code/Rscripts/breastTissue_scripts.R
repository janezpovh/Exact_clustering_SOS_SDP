BreastTissue_with_clust_labels <- read.csv("~/MATLAB/jpcode/Exact_clustering_SOS_SDP/input_data_for_exact_solver/real_data/BreastTissue_with_clust_labels.txt")
View(BreastTissue_with_clust_labels)

write.table(BreastTissue_with_clust_labels[,1:9],file = "C:/Users/janez/Documents/MATLAB/jpcode/Exact_clustering_SOS_SDP/input_data_for_exact_solver/real_data/BreastTissue.txt",col.names = FALSE,row.names = FALSE)
