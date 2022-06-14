library("foreign")
library(rJava)
library(RWeka)
library(farff)
setwd("~/MATLAB/jpcode/clustering")
readARFF()


REAL_data=1
ARTIFICIAL_data=1

if (REAL_data){
  all_files = dir("./clustering-benchmark/src/main/resources/datasets/real-world/")
  eliminate_datasets=c("yeast.arff")
  for (data_file in all_files){
    if (max(data_file == eliminate_datasets)){
      next
    }
    data_file_txt=sub(".arff",".txt",data_file)  
    data_file_clust=sub(".txt","_with_clust_labels.txt",data_file_txt)  
    
    #data_input=read.arff(paste0("./clustering-benchmark/src/main/resources/datasets/real-world/",data_file))
    data_input=readARFF(paste0("./clustering-benchmark/src/main/resources/datasets/real-world/",data_file))
    which_class = which(colnames(data_input) == "class")
    
    write(file = paste0("./input_data_for_exact_solver/real_data/",data_file_txt),c(nrow(data_input),ncol(data_input)-1))
    write.table(file = paste0("./input_data_for_exact_solver/real_data/",data_file_txt),data_input[,-which_class],row.names = FALSE,col.names = FALSE,append = TRUE)
    write.table(file = paste0("./input_data_for_exact_solver/real_data/",data_file_clust),data_input,row.names = FALSE,col.names = TRUE)
  }
}

# ARTIFICIAL_data
if (ARTIFICIAL_data){
  all_files = dir("./clustering-benchmark/src/main/resources/datasets/artificial/")
  eliminate_datasets=c("yeast.arff")
  for (data_file in all_files){
    if (max(data_file == eliminate_datasets)){
      next
    }
    data_file_txt=sub(".arff",".txt",data_file)  
    data_file_clust=sub(".txt","_with_clust_labels.txt",data_file_txt)  
    
    data_input=readARFF(paste0("./clustering-benchmark/src/main/resources/datasets/artificial/",data_file))
    which_class = which(colnames(data_input) == "class")
    
    write(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_txt),c(nrow(data_input),ncol(data_input)-1))
    write.table(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_txt),data_input[,-which_class],row.names = FALSE,col.names = FALSE,append = TRUE)
    write.table(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_clust),data_input,row.names = FALSE,col.names = TRUE)
  }
}
