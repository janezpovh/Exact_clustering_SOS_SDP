library("foreign")
library(rJava)
library(RWeka)
library(farff)
setwd("~/MATLAB/jpcode/Exact_clustering_SOS_SDP")
readARFF()


REAL_data=1
ARTIFICIAL_data=0

Table_summary = data.frame(name=character(),type=character(),n=integer(),m=integer(),K=integer())
counter=1
if (REAL_data){
  all_files = dir("./clustering-benchmark/src/main/resources/datasets/real-world/")
  eliminate_datasets=c("yeast.arff","german.arff","vowel.arff","water-treatment.arff") #german, vowel in non-numeric, yeasr has mistake that I can overcome
  for (data_file in all_files){
    if (max(data_file == eliminate_datasets)){
      next
    }
    data_file_txt=sub(".arff",".txt",data_file)  
    data_file_clust=sub(".txt","_with_clust_labels.txt",data_file_txt)  
    
    #data_input=read.arff(paste0("./clustering-benchmark/src/main/resources/datasets/real-world/",data_file))
    data_input=na.omit(readARFF(paste0("./clustering-benchmark/src/main/resources/datasets/real-world/",data_file)))
    data_input<-as.data.frame(data_input)
    which_class = which(tolower(colnames(data_input)) == "class")
    
    write(file = paste0("./input_data_for_exact_solver/real_data/",data_file_txt),c(nrow(data_input),ncol(data_input)-1))
    write.table(file = paste0("./input_data_for_exact_solver/real_data/",data_file_txt),data_input[,-which_class],row.names = FALSE,col.names = FALSE,append = TRUE,quote = FALSE)
    write.table(file = paste0("./input_data_for_exact_solver/real_data/",data_file_clust),data_input,row.names = FALSE,col.names = TRUE)
    Table_summary[counter,]=c(data_file,"real",nrow(data_input),ncol(data_input),length(levels(data_input[,which_class])))
    counter=counter+1
    }
}

# ARTIFICIAL_data
if (ARTIFICIAL_data){
  all_files = dir("./clustering-benchmark/src/main/resources/datasets/artificial/")
  eliminate_datasets=c("birch-rg1.arff","birch-rg3.arff","birch-rg3.arff")  # birch-rg1 has no labels
  for (data_file in all_files){
    if (max(data_file == eliminate_datasets)){
      next
    }
    data_file_txt=sub(".arff",".txt",data_file)  
    data_file_clust=sub(".txt","_with_clust_labels.txt",data_file_txt)  
    
    data_input=na.omit(readARFF(paste0("./clustering-benchmark/src/main/resources/datasets/artificial/",data_file)))
    data_input<-as.data.frame(data_input)
    which_class = which(tolower(colnames(data_input)) == "class")
    
    write(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_txt),c(nrow(data_input),ncol(data_input)-1))
    write.table(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_txt),data_input[,-which_class],row.names = FALSE,col.names = FALSE,append = TRUE,quote = FALSE)
    write.table(file = paste0("./input_data_for_exact_solver/artificial_data/",data_file_clust),data_input,row.names = FALSE,col.names = TRUE)
    Table_summary[counter,]=c(data_file,"artificial",nrow(data_input),ncol(data_input),length(levels(data_input[,which_class])))
    counter=counter+1
  }
}
write.table(Table_summary,file="C:/Users/janez/Documents/MATLAB/jpcode/Exact_clustering_SOS_SDP/input_data_for_exact_solver/Table_summary.txt",row.names = FALSE,col.names = TRUE,quote = FALSE)
