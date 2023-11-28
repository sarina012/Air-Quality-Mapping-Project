import pandas as pd


df1 = pd.read_excel('data_test.xlsx') 

df2 = pd.read_csv('output.csv', sep= ',',skiprows=7)

df2.to_excel('output_ex.xlsx',index=False)

merged_df = pd.concat([df1,df2],axis=1)

merged_df.to_excel('new.xlsx',index=False)