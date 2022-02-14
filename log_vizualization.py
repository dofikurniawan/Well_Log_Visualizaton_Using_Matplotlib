#import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#load log_header
#you need to specify the rows where information about log_header stored
# in this project log_header in rows 28,33 > inpython index it means 27,32 
with open('data/WELL-2_logs.las','r') as header:
    data=header.readlines()
    log_name=[]
    for i in range (27,32):
        log_name.append((data[i].split()[0]))        
#load data log
# you need to skiprows until rows where the value begins
# in this log the value begin in rows 34 
log=np.loadtxt('data/WELL-2_logs.las',skiprows=33)
#make log's datafrmae
data_log=pd.DataFrame(log,columns=log_name)
#dealing with error data (-999.25) by replace it values to nan
data_log=data_log.replace(-999.2500,np.nan)
#drop nan values
data_log.dropna(axis=0,inplace=True)
#convert DT to log vp by devided 1000000
data_log['VP']=1000000/data_log['DT']
data_log.drop(columns='DT',inplace=True)
#Plotting Log Suing Subplots style
fig,ax=plt.subplots(nrows=1,ncols=4,sharey=True,figsize=(12,10))
for i in range (len(data_log.columns)-1):
    #plot depth vs log_name
    ax[i].plot(data_log.iloc[:,i+1].values,data_log['DEPTH'].values,linewidth=0.25,color='red')
    #inverse depth value
    ax[i].set_ylim(max(data_log['DEPTH']),min(data_log['DEPTH']))
    #add grid
    ax[i].minorticks_on()
    ax[i].grid(which='major', linestyle='-', linewidth='0.5', color='black')
    ax[i].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    #add log_name
    ax[i].set_title(f'{data_log.columns[i+1]}')
    #define thresshold value to determine sand and shale
    # <=50 sand and >= shale 
    if i==1:
        y1=data_log.GR
        y2=0*y1+50
        ax[1].fill_betweenx(data_log['DEPTH'],y1,y2,where=(y1<=y2),color='gold')
        ax[1].fill_betweenx(data_log['DEPTH'],y1,y2,where=(y1>y2),color='lime')
plt.subplots_adjust(wspace=0.5)           
fig.suptitle('Well-2')
plt.savefig('Plot_WELL-2_logs.png')       