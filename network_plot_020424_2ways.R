# https://christophergandrud.github.io/networkD3/
library(networkD3)
library(igraph)

setwd("Z:/shani.vaknine/Documents/Research/Frasch_project/RNA_analysis/new_comb_110822/newer_070922/Targets/miRDB_targets/new_filter_171223/network_plot_030124")
#prepare tRF-gene matrix
tRF_info <- read.csv("Z:/shani.vaknine/Documents/Research/Frasch_project/RNA_analysis/new_comb_110822/newer_070922/Targets/miRDB_targets/new_filter_171223/UCS/tragets_df_full_cholinergic_info_miRDB_80_UCS_new_filter.csv")
tRF_info_cholinergic <- tRF_info[which(tRF_info$CholinotRF == "CholinotRF" & tRF_info$Cholinergic_gene == "Cholinergic"),]
write.csv(table(tRF_info_cholinergic$tRF,tRF_info_cholinergic$aminoAcid_Origin_combo),"tRF_info_cholinergic.csv")

# miRs
miRs_info <- read.csv("Z:/shani.vaknine/Documents/Research/Frasch_project/RNA_analysis/new_comb_110822/newer_070922/Targets/miRDB_targets/new_filter_171223/miRs/UCS_CholinomiR_df_80_miRDB_cutoff5.csv")
miR_info_cholinergic <- miRs_info[which(miRs_info$CholinomiR == "Cholino-miR"),]

CholinomiR_df <- data.frame(RNA_name = character(),Gene = character())
for(m in unique(miR_info_cholinergic$miRNA.Name)){
  #m =  unique(miR_info_cholinergic$miRNA.Name)[1]
  CholinomiR_df_temp <- data.frame(RNA_name = m,
                                   Gene = strsplit(miR_info_cholinergic$cholinergic_genes[which(miR_info_cholinergic$miRNA.Name == m)], ", "))
  colnames(CholinomiR_df_temp)[2] <- "Gene"
  CholinomiR_df <- rbind(CholinomiR_df,CholinomiR_df_temp)
}

CholinotRF_df <- tRF_info_cholinergic[,which(colnames(tRF_info_cholinergic) %in% c("tRF","Gene"))]
colnames(CholinotRF_df)[1] <- "RNA_name"

colnames(CholinomiR_df) <- c("Gene","RNA_name")
CholinoRNA_df <- rbind(CholinotRF_df,CholinomiR_df)


net_data <- CholinoRNA_df


net_data_info <- as.data.frame(unique(c(unique(net_data$RNA_name),unique(net_data$Gene))))
colnames(net_data_info) <- "source_name"

net_data_info$ID <- ifelse(grepl("tRF", net_data_info$source_name), "tRF", ifelse(grepl("hsa", net_data_info$source_name), "miR","Gene"))
net_data_info$source_num <- 0:(length(net_data_info$ID)-1)

length(net_data_info$source_name) == length(unique(net_data_info$source_name))
net_data$source = sapply(net_data$RNA_name,function(x){net_data_info$source_num[which(net_data_info$source_name == x)]})
net_data$target = sapply(net_data$Gene,function(x){net_data_info$source_num[which(net_data_info$source_name == x)]})


###

library(dplyr)
net_data$value <- rep(1,length(net_data$RNA_name))
net_data$group <- ifelse(grepl("tRF", net_data$RNA_name), "tRF",  "Gene")

p <- sankeyNetwork(Links = net_data, Nodes = net_data_info,
             Source = "source", Target = "target",
             NodeID = "source_name",Value = "value",
             NodeGroup="ID",LinkGroup="group",iterations = 0)

p

# write.csv(net_data,"net_data.csv")
# net_data <- read.csv("net_data_corrected.csv")
tRF_genes <- unique(net_data$Gene[!grepl("hsa", net_data$Gene)]);length(tRF_genes) #51
miR_genes <- unique(net_data$RNA_name[!grepl("tRF", net_data$RNA_name)]);length(miR_genes) #31

intersect(tRF_genes,miR_genes);length(intersect(tRF_genes,miR_genes)) #26

diff <- setdiff(tRF_genes,miR_genes);length(setdiff(tRF_genes,miR_genes)) #25
diff_tRF <- tRF_genes[which(tRF_genes %in% diff)]; length(diff_tRF)
colnames(net_data)
add_rows <- data.frame(RNA_name = diff_tRF, Gene = rep("",length(diff_tRF)),
                       source = sapply(diff_tRF,function(x){net_data_info$source_num[which(net_data_info$source_name %in% x)]}),  
                       target = rep(115,length(diff_tRF)), value = 0, group = "Gene")
net_data <- rbind(net_data,add_rows)

# write.csv(net_data_info,"net_data_info.csv")
net_data_info <- rbind(net_data_info,data.frame(source_name="",
                                                ID = "miR",
                                                source_num=115))

p <- sankeyNetwork(Links = net_data, Nodes = net_data_info,
                   Source = "source", Target = "target",
                   NodeID = "source_name",Value = "value",
                   NodeGroup="ID",LinkGroup="group",iterations = 0)

p

# save the widget
library(htmlwidgets)
saveWidget(p, file=paste0( getwd(), "/sankeyNetwork_2way_020424.html"))
library(webshot)
# webshot::install_phantomjs()
webshot(url = paste0(getwd(), "/sankeyNetwork_2way_020424.html"), file = "sankeyNetwork_2way_020424.pdf")


### orgenize by gene sub groups and tRF family
net_data$tRF_family <- sapply(net_data$RNA_name,function(x){ifelse(x %in% tRF_info$tRF,tRF_info$aminoAcid_Origin_combo[which(tRF_info$tRF==x)],"miR")}) 

Cholinergic_genes <- read.csv("Cholinergic_genes_updated_020424.csv")
net_data$Gene_sub_group <- sapply(net_data$Gene,function(x){Cholinergic_genes$Cholinergic_sub.group[which(Cholinergic_genes$Gene==x)]}) 
colnames(net_data)

#order by orgenizing net_data_info
net_data_info_tRF <- net_data_info[which(net_data_info$ID == "tRF"),]
net_data_info_tRF$tRF_family <- sapply(net_data_info_tRF$source_name,function(x){unique(tRF_info$aminoAcid_Origin_combo[which(tRF_info$tRF==x)])}) 
net_data_info_tRF_ordered <- net_data_info_tRF[order(net_data_info_tRF$tRF_family, decreasing = F),]
net_data_info_tRF_ordered$source_num <- min(net_data_info_tRF_ordered$source_num):max(net_data_info_tRF_ordered$source_num)
net_data_info_tRF_ordered$tRF_family <- NULL

net_data_info_miR <- net_data_info[which(net_data_info$ID == "miR"),]
net_data_info_miR_ordered <- net_data_info_miR[order(net_data_info_miR$source_name,decreasing = F),]
net_data_info_miR_ordered$source_num <- min(net_data_info_miR_ordered$source_num):max(net_data_info_miR_ordered$source_num)

# net_data_info_Gene <- net_data_info[which(net_data_info$ID == "Gene"),]
# net_data_info_Gene$Gene_sub_group <- sapply(net_data_info_Gene$source_name,function(x){Cholinergic_genes$Cholinergic_sub.group[which(Cholinergic_genes$Gene==x)]})
# net_data_info_Gene_ordered <- net_data_info_Gene[order(net_data_info_Gene$Gene_sub_group,decreasing = F),]
# net_data_info_Gene_ordered$source_num <- min(net_data_info_Gene_ordered$source_num):max(net_data_info_Gene_ordered$source_num)
# write.csv(net_data_info_Gene_ordered,"net_data_info_Gene_ordered2.csv")
net_data_info_Gene_ordered <- read.csv("net_data_info_Gene_ordered2.csv")
net_data_info_Gene_ordered$X <- NULL
net_data_info_Gene_ordered$Gene_sub_group <- NULL

net_data_info_ordered <- rbind(net_data_info_tRF_ordered,net_data_info_miR_ordered,net_data_info_Gene_ordered)
net_data_info_ordered <- net_data_info_ordered[order(net_data_info_ordered$source_num,decreasing = F),]


net_data_ordered <- net_data
net_data_ordered$source <- sapply(net_data_ordered$RNA_name,function(x){net_data_info_ordered$source_num[which(net_data_info_ordered$source_name == x)]})
net_data_ordered$target <- sapply(net_data_ordered$Gene,function(x){net_data_info_ordered$source_num[which(net_data_info_ordered$source_name == x)]})
colnames(net_data_ordered)
# net_data_ordered$Gene_sub_group <- NULL
# 
# write.csv(net_data_ordered,"net_data_ordered.csv")
# write.csv(net_data_info_ordered,"net_data_info_ordered.csv")

p <- sankeyNetwork(Links = net_data_ordered, Nodes = net_data_info_ordered,
                   Source = "source", Target = "target",
                   NodeID = "source_name",Value = "value",fontFamily="Arial",
                   NodeGroup="ID",iterations = 0,LinkGroup = "tRF_family",
                   width = 604,height = 831,fontSize = 10,nodeWidth = 20)

p

saveWidget(p, file=paste0( getwd(), "/sankeyNetwork_genesubgroup_2way_020424.html"))
webshot(url = paste0(getwd(), "/sankeyNetwork_genesubgroup_2way_020424.html"), file = "sankeyNetwork_genesubgroup_2way_020424.pdf",vwidth = 16,vheight = 22)



##ID
p <- sankeyNetwork(Links = net_data_ordered, Nodes = net_data_info_ordered,
                   Source = "source", Target = "target", 
                   NodeID = "source_name",Value = "value",fontFamily="Arial",
                   NodeGroup="ID",iterations = 0,LinkGroup = "group",
                   width = 604,height = 831,fontSize = 10,nodeWidth = 20)

p
saveWidget(p, file=paste0( getwd(), "/sankeyNetwork_ID1_2way_020424.html"))
webshot(url = paste0(getwd(), "/sankeyNetwork_ID1_2way_020424.html"), file = "sankeyNetwork_ID1_2way_020424.pdf",vwidth = 16,vheight = 22)


my_color <- 'd3.scaleOrdinal() .domain(["tRF", "miR"]) .range(["#598DA0","#b3b3b3"])'


p <- sankeyNetwork(Links = net_data_ordered, Nodes = net_data_info_ordered,
                   Source = "source", Target = "target",colourScale=my_color, 
                   NodeID = "source_name",Value = "value",fontFamily="Arial",
                   NodeGroup="ID",iterations = 0,LinkGroup = "group",
                   width = 604,height = 831,fontSize = 10,nodeWidth = 20)

p
saveWidget(p, file=paste0( getwd(), "/sankeyNetwork_ID2_2way_020424.html"))
webshot(url = paste0(getwd(), "/sankeyNetwork_ID2_2way_020424.html"), file = "sankeyNetwork_ID2_2way_020424.pdf",vwidth = 16,vheight = 22)

