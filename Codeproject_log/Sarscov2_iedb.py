import pandas as  pd
import datetime
# !pip install iedb
from Bio import SeqIO
import re,sys
import iedb
num=sys.argv[1]
savename=sys.argv[2]
starttime = datetime.datetime.now()
frames=[]
# allelename=["HLA-A*01:01","HLA-A*02:01","HLA-A*02:06","HLA-A*03:01","HLA-A*11:01","HLA-A*23:01","HLA-A*24:02","HLA-A*25:01","HLA-A*26:01","HLA-A*29:02","HLA-A*30:01"
# ,"HLA-A*31:01","HLA-A*32:01","HLA-A*33:03","HLA-A*68:01","HLA-A*68:02","HLA-A*74:01"]
allelename=["HLA-A*02:01","HLA-A*02:06","HLA-A*23:01","HLA-A*24:02","HLA-A*30:01"]
seq=SeqIO.parse("/home/maolp/data3/Project/Sarscov2_iedb/zhucds_nsp_pep.fa", "fasta")
for line in seq:
    name=line.id.split("&&")[1]
    # # print(name)
    # if re.findall("surface",line.id):
    #     # print(line.id)
    #     print(name)

    #     print(line.seq.rstrip())
        

    #     # print(iedb.predict_antigen_sequence(line.seq))
    #     print("-----------------------------------------------------")
    for al in allelename:
        print(al)
        for i in range(num,num+1):
            print(i)
            tcell_res = mhci_res =  iedb.query_mhci_binding(method="recommended", sequence=str(line.seq), allele=al, length=i)
            tcell_res["name"]=name
            frames.append(tcell_res)
            

result_sp = pd.concat(frames)
result_sp.to_csv("/home/maolp/data3/Project/Sarscov2_iedb/zhucds_father_spike_pep_result.csv",index=True)


### new version

import pandas as  pd
import datetime
# !pip install iedb
from Bio import SeqIO
import re,sys
import iedb
alldata=["HLA-A*24:02","HLA-A*30:01"]
alldata=["HLA-A*24:02"]
seqfasta2="/home/maolp/data3/Project/Sarscov2_iedb/zhucds_nsp_pep.fa"
savedata="/home/maolp/data3/Project/Sarscov2_iedb/refzhu_"
def seq_iedb(num,savefile=savedata,seqfasta=seqfasta2,allelename=alldata):
    # num=8
    # savename="Father"
    tcell_res=pd.DataFrame()
    starttime = datetime.datetime.now()
    frames=[]
    # allelename=["HLA-A*01:01","HLA-A*02:01","HLA-A*02:06","HLA-A*03:01","HLA-A*11:01","HLA-A*23:01","HLA-A*24:02","HLA-A*25:01","HLA-A*26:01","HLA-A*29:02","HLA-A*30:01"
    # ,"HLA-A*31:01","HLA-A*32:01","HLA-A*33:03","HLA-A*68:01","HLA-A*68:02","HLA-A*74:01"]

    seq=SeqIO.parse(seqfasta, "fasta")
    for line in seq:
        name=line.id.split("&&")[1]
        # # print(name)
        if re.findall("ORF1ab_polyprotein",line.id):
            pass
        else:
            # print(line.id)
            print(name)

            print(line.seq.rstrip())
                

            #     # print(iedb.predict_antigen_sequence(line.seq))
            #     print("-----------------------------------------------------")
            for al in allelename:
                print(al)
                for i in range(num,num+1):
                    print(i)
                    tcell_res =  iedb.query_mhci_binding(method="recommended", sequence=str(line.seq), allele=al, length=i)
                    tcell_res["name"]=name
                    frames.append(tcell_res)
                    

    result_sp = pd.concat(frames)

    result_sp.to_csv(savefile+str(num)+"_pep_result.csv",index=True)
    endtime = datetime.datetime.now()
    print("time:",endtime - starttime)
    return  result_sp
