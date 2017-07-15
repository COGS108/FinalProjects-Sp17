import pandas as pd
import sys,argparse,csv

#convert the csv file of storm drain beat areas into a dataframe
df = pd.read_csv('st_beats.csv')
#remove data points that have an unknown beat number
df = df[df.Beat != -1]
#get number of storm drains in each beat area
df_counts = df['Beat'].value_counts()

#read in the csv file of beat number and beat names
myDict = {}
f=open('beat_names.csv', 'r')
reader=csv.reader(f)
#map beat number to beat name in a dictionary
for line in reader:
	if(line[0].isdigit()):	
		myDict[line[0]]=line[1]
f.close()

#create a list of beat names in the order that the beat numbers appear 
list_names = []
for entry in df_counts.index:
	list_names.append(myDict[str(entry)])

#create a list of the moneatary values of each beat area
myList = []
for i in df_counts.values:
	myList.append(i*(-3371))

#create a new dataframe with the beat numbers corresponding to value
new_df = pd.DataFrame({'Beat':df_counts.index, 'Count':df_counts.values, 'Value':myList, 'Name':list_names})
print(new_df)
#write the dataframe to a csv file
new_df.to_csv('env_value.csv',sep=',')

