import pandas as pd
import os

def split_states_and_country(filename, index):
    clean_folder = os.getcwd()
    clean_folder +=  os.sep + "clean"
    
    clean_folder_states = clean_folder+os.sep+"states"
    clean_folder_brazil = clean_folder+os.sep+"brazil"

    df = pd.read_csv(filename, sep=";")
    df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
    df_brazil = df[df["regiao"] == "Brasil"]
    df_states.to_csv(os.path.join(clean_folder_states, str(index)+"_df_states.csv"), index=False )
    df_brazil.to_csv(os.path.join(clean_folder_brazil, str(index)+"_df_brazil.csv"), index=False )

def clean_dataset_into_multiple_files():
    unclean_folder = os.getcwd()
    unclean_folder += os.sep + "unclean"
    
    i=0
    for filename in os.listdir(unclean_folder):
        if filename.endswith(".csv"):
            split_states_and_country(os.path.join(unclean_folder, filename),i)
        i+=1    

def merge_files(file_folder,result_folder,result_filename):
    file_list = []

    i=0
    for filename in os.listdir(file_folder):
        if filename.endswith(".csv") and filename[0:1]==str(i):
            file_list+= [filename]
        i+=1   
    
    combined_csv = pd.concat( [ pd.read_csv( os.path.join(file_folder,f)) for f in file_list ] )
    combined_csv.to_csv( os.path.join(result_folder,result_filename), index=False )    

def clean_dataset_into_single_file():
    clean_folder = os.getcwd()
    clean_folder += os.sep + "clean"
    
    clean_folder_states = clean_folder+os.sep+"states"
    clean_folder_brazil = clean_folder+os.sep+"brazil"

    merge_files(clean_folder_states,clean_folder,"states_result.csv")
    merge_files(clean_folder_brazil,clean_folder,"brazil_result.csv")

clean_dataset_into_multiple_files()
clean_dataset_into_single_file()
