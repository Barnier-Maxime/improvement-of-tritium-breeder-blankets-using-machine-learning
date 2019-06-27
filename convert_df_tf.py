import numpy as np
import pandas as pd
import tensorflow as tf

def convert_df_in_tf(filename, material):
    df=pd.read_json(filename)
    df_filtered = df.loc[(df['breeder_material_name']==material)]
    tf.enable_eager_execution()
    dataset = (  
         tf.data.Dataset.from_tensor_slices(  
                    (  
                      tf.cast(list(df_filtered['enrichment_value']), tf.float32),  
                      tf.cast(df_filtered['std_dev'].values,tf.float32), 
                      tf.cast(df_filtered['value'].values, tf.float32)  
                    )  
                )  
            ) 
    for enrichment_value, std_dev, value in dataset : 
        print(f'enrichment_value:{enrichment_value} Std_dev:{std_dev} TBR:{value}') 
    
    return(dataset)
   

if __name__== '__main__':
    convert_df_in_tf('results_point_source/simulation_results_4_layers_halton_first_wall.json','Li2TiO3')

    
