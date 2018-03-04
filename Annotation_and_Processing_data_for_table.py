
# coding: utf-8

# In[368]:


import pickle
import numpy as np
import pandas as pd
#import tables
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

#print(DT)
#print(len(a))
#print(len(a[0]))
#print(len(a[0][0]))

in_txt = open('list_of_list_of_dicts.files.txt')
file_string = in_txt.read()
file_list = file_string.split('\n')
#print(len(file_list))
#print(len(file_list[0]))
#print(len(file_list[0][0]))

nameFile = np.loadtxt('list_of_list_of_dicts.files.txt' , delimiter='\n' , dtype=np.str)
#print(nameFile)

"""
обозначения:
n - нормальная среда
AD7 - лекарство
CS - дикого типа
agn - мутант
"""
#
# общее количество песен
# количество синусных песен
# количество импульных песен

#print(nameFile[0:25]) #agn AD7
#print(nameFile[25:45]) #agn n
#print(nameFile[45:58]) #CS AD7
#print(nameFile[58:81]) #CS n

#среднее для станд
#среднее для син и стд по файлу/ по каталогу


# In[521]:


def Muha_analysis_v1( currentDT , start , end ):
    numDTtest1 = len(currentDT[start:end]); i = 0
    countImpulsSongsTest=0 #общее количество имп песен
    countSinSongsTest=1 #общее колчиество синусных песен
    allTimeImpulsSongs=0 #общее время импульсных песен
    allTimeSinSongs=0 #общее время синусных песен
    allEnergyImpul=0 #общее значение энергии для импульсных песен
    allNumPeriods=0 #общее значение энергеии для синусных песен
    while( i < numDTtest1 ):
        for obs in currentDT[start:end][i]:
            # импульнсые песни
            try:
                if (len(obs) == 10):
                    if (obs['number_of_pulses'] >= 4):
                        # общее количество импульсных песен
                        countImpulsSongsTest += 1
                        # средняя продолжительность импульсных песен
                        allTimeImpulsSongs += obs['number_of_pulses']
                        # среднее значение энрегии
                        allEnergyImpul += np.absolute(obs['energies_mean'])
            # синусные песни
                elif (len(obs) == 5):
                    #print(obs['song_duration'])
                    # общее количество синусных песен                    
                    countSinSongsTest += 1                  
                    # средняя продолжительность синусных песен
                    allTimeSinSongs += obs['song_duration']
                    # средняя энергия
                    allNumPeriods += obs['n_periods']
            except TypeError: 
                #print(obs)
                error = 1
                #print('error')
        i+=1 
        
    meanTimeImpulsSongs = allTimeImpulsSongs/countImpulsSongsTest
    meanTimeSinSongs = allTimeSinSongs/countSinSongsTest
    meanEnergyImpul = allEnergyImpul/countImpulsSongsTest
    meanNumPeriods = allNumPeriods/countSinSongsTest
    res = {'1 Количество импульсных песен':  "%.8g" % countImpulsSongsTest ,
           '3 Количество синусных песен': int(countSinSongsTest),
           '2 Среднее количество импульсов в песне' : round(meanTimeImpulsSongs,1) ,
           '4 Среднее время синусных песен (с)' : round(meanTimeSinSongs,1),
           '5 Средняя энергия сигнала': round(meanEnergyImpul,1),
           '6 Среднее количество периодов' : round(meanNumPeriods,1),
           '7 Доля песен в 300 с записи (%)' : round(100*(allTimeImpulsSongs*0.0125 + allTimeSinSongs)/300,1)
          }
    return(res)


# In[520]:


countImpulsSongsTest = 1.0
"%.8g" % countImpulsSongsTest


# In[522]:


with open('list_of_list_of_dicts.pickle','rb') as f:
    a=pickle.load(f , encoding='latin1')
# датафрейм с данными размеченными от Геннадия
DT = pd.DataFrame(a)
#DT[0][5]
print(Muha_analysis_v1(DT , 0 , 25))
print(Muha_analysis_v1(DT , 25 , 45))
print(Muha_analysis_v1(DT , 45 , 58))
print(Muha_analysis_v1(DT , 58 , 81))


# In[547]:


def Muha_analysis_v2( currentDT , start , end ):
    numDTtest1 = len(currentDT[start:end]); i = 0
    countImpulsSongsTest=0 #общее количество имп песен
    countSinSongsTest=1 #общее колчиество синусных песен
    allTimeImpulsSongs=0 #общее время импульсных песен
    allTimeSinSongs=0 #общее время синусных песен
    allEnergyImpul=0 #общее значение энергии для импульсных песен
    allNumPeriods=0 #общее значение энергеии для синусных песен
    while( i < numDTtest1 ):
        for obs in currentDT[start:end][i]:
            # импульнсые песни
            try:
                if (len(obs) == 10):
                    if (obs['number_of_pulses'] > 1):
                        # общее количество импульсных песен
                        countImpulsSongsTest += 1
                        # средняя продолжительность импульсных песен
                        allTimeImpulsSongs += obs['number_of_pulses']
                        # среднее значение энрегии
                        allEnergyImpul += np.absolute(obs['energies_mean'])
            # синусные песни
                elif (len(obs) == 5):
                    #print(obs['song_duration'])
                    # общее количество синусных песен                    
                    countSinSongsTest += 1                  
                    # средняя продолжительность синусных песен
                    allTimeSinSongs += obs['song_duration']
                    # средняя энергия
                    allNumPeriods += obs['n_periods']
            except TypeError: 
                #print(obs)
                error = 1
                #print('error')
        i+=1 
        
    meanTimeImpulsSongs = allTimeImpulsSongs/countImpulsSongsTest
    meanTimeSinSongs = allTimeSinSongs/countSinSongsTest
    meanEnergyImpul = allEnergyImpul/countImpulsSongsTest
    meanNumPeriods = allNumPeriods/countSinSongsTest
    res = {'1 Количество импульсных песен':  "%.8g" % countImpulsSongsTest ,
           '3 Количество синусных песен': int(countSinSongsTest),
           '2 Среднее количество импульсов в песне' : round(meanTimeImpulsSongs,1) ,
           '4 Среднее время синусных песен (с)' : round(meanTimeSinSongs,1),
           '5 Средняя энергия сигнала': round(meanEnergyImpul,1),
           '6 Среднее количество периодов' : round(meanNumPeriods,1),
           '7 Доля песен в 300 с записи (%)' : round(100*(allTimeImpulsSongs*0.0125 + allTimeSinSongs)/300,1)
          }
    return(res)

with open('new_list_of_list_of_dicts.pickle','rb') as f_new:
    new_a=pickle.load(f_new , encoding='latin1')

# датафрейм с данными
DT_new = pd.DataFrame(new_a)

print(Muha_analysis_v2(DT_new , 0 , 25))
print(Muha_analysis_v2(DT_new , 25 , 45))
print(Muha_analysis_v2(DT_new , 45 , 58))
print(Muha_analysis_v2(DT_new , 58 , 81))


# In[561]:


def Muha_analysis_v3( currentDT , start , end ):
    numDTtest1 = len(currentDT[start:end]); i = 0
    countImpulsSongsTest=0 #общее количество имп песен
    countSinSongsTest=1 #общее колчиество синусных песен
    allTimeImpulsSongs=0 #общее время импульсных песен
    allTimeSinSongs=0 #общее время синусных песен
    allEnergyImpul=0 #общее значение энергии для импульсных песен
    allNumPeriods=0 #общее значение энергеии для синусных песен
    while( i < numDTtest1 ):
        for obs in currentDT[start:end][i]:
            # импульнсые песни
            try:
                if (len(obs) == 10):
                    if (obs['number_of_pulses'] >= 4):
                        # общее количество импульсных песен
                        countImpulsSongsTest += 1
                        # средняя продолжительность импульсных песен
                        allTimeImpulsSongs += obs['number_of_pulses']
                        # среднее значение энрегии
                        allEnergyImpul += np.absolute(obs['energies_mean'])
                # синусные песни
                elif (len(obs) == 5):
                    if( obs['song_duration'] > 0.115 ):                  
                        #print(obs['song_duration'])
                        # общее количество синусных песен                    
                        countSinSongsTest += 1                  
                        # средняя продолжительность синусных песен
                        allTimeSinSongs += obs['song_duration']
                        # средняя энергия
                        allNumPeriods += obs['n_periods']
            except TypeError: 
                #print(obs)
                error = 1
                #print('error')
        i+=1 
        
    meanTimeImpulsSongs = allTimeImpulsSongs/countImpulsSongsTest
    meanTimeSinSongs = allTimeSinSongs/countSinSongsTest
    meanEnergyImpul = allEnergyImpul/countImpulsSongsTest
    meanNumPeriods = allNumPeriods/countSinSongsTest
    res = {'1 Количество импульсных песен':  "%.8g" % countImpulsSongsTest ,
           '3 Количество синусных песен': int(countSinSongsTest),
           '2 Среднее количество импульсов в песне' : round(meanTimeImpulsSongs,1) ,
           '4 Среднее время синусных песен (с)' : round(meanTimeSinSongs,1),
           '5 Средняя энергия сигнала': round(meanEnergyImpul,1),
           '6 Среднее количество периодов' : round(meanNumPeriods,1),
           '7 Доля песен в 300 с записи (%)' : round(100*(allTimeImpulsSongs*0.0125 + allTimeSinSongs)/300,1)
          }
    return(res)

with open('old_new_list_of_list_of_dicts.pickle','rb') as f_old_new:
    old_new_a=pickle.load(f_old_new , encoding='latin1')

# датафрейм с данными
DT_old_new = pd.DataFrame(old_new_a)

print(Muha_analysis_v3(DT_old_new , 0 , 25))
print(Muha_analysis_v3(DT_old_new , 25 , 45))
print(Muha_analysis_v3(DT_old_new , 45 , 58))
print(Muha_analysis_v3(DT_old_new , 58 , 81))


# In[545]:


annotaionRESULT = { 'agn/AD7' : Muha_analysis_v1(DT , 0 , 25) , 'agn/n': Muha_analysis_v1(DT , 25 , 45) , 'CS/AD7': Muha_analysis_v1(DT , 45 , 58) , 'CS/n': Muha_analysis_v1(DT , 58 , 81) }
DFannotaionRESULT = pd.DataFrame(annotaionRESULT )
DFannotaionRESULT
import pickle
with open("resultTable1.pickle", 'wb') as fl:
    pickle.dump(DFannotaionRESULT, fl)


# In[578]:


# обработанные (родные) данные
# из этой таблицы берем строки 1, 2, 5
processingRESULT1 = { 'agn/AD7' : Muha_analysis_v2(DT_new , 0 , 25) , 'agn/n': Muha_analysis_v2(DT_new , 25 , 45) , 'CS/AD7': Muha_analysis_v2(DT_new , 45 , 58) , 'CS/n': Muha_analysis_v2(DT_new , 58 , 81) }
DFprocessingRESULT1 = pd.DataFrame(processingRESULT1)
DFprocessingRESULT1

#import pickle
#with open("resultTable2.pickle", 'wb') as fl1:
 #   pickle.dump(DFprocessingRESULT1, fl1)


# In[577]:


# из этой таблицы берем строки 3, 4, 6
processingRESULT2 = { 'agn/AD7' : Muha_analysis_v3(DT_old_new , 0 , 25) , 'agn/n': Muha_analysis_v3(DT_old_new , 25 , 45) , 'CS/AD7': Muha_analysis_v3(DT_old_new , 45 , 58) , 'CS/n': Muha_analysis_v3(DT_old_new , 58 , 81) }
DFprocessingRESULT2 = pd.DataFrame(processingRESULT2)
DFprocessingRESULT2

#import pickle
#with open("resultTable3.pickle", 'wb') as fl2:
#    pickle.dump(DFprocessingRESULT2, fl2)


# In[587]:


#последняя таблица

with open('resultTable2.pickle','rb') as new:
    newTAB = pickle.load(new , encoding='latin1')
newTAB
#последняя таблица

with open('resultTable3.pickle','rb') as new:
    newTAB2 = pickle.load(new , encoding='latin1')
newTAB2


# In[586]:


newTAB.iloc[[0, 1, 4]]


# In[588]:


newTAB2.iloc[[2, 3, 5]]


# In[650]:


result_pd = pd.concat((newTAB.iloc[[0, 1, 4]], newTAB2.iloc[[2, 3, 5]]))


# In[651]:


result_pd.sort_index()
result_pd


# In[658]:


def MeanTime_v4(vecRes):
    res = {'7 Доля песен в 300 с записи (%)' : vecRes }
    return(res)
processingRESULT3 = { 'agn/AD7' : MeanTime_v4(6.14) , 'agn/n': MeanTime_v4(4.2), 'CS/AD7': MeanTime_v4(1.1) , 'CS/n': MeanTime_v4(3.6) }
DFprocessingRESULT3 = pd.DataFrame(processingRESULT3)
DFprocessingRESULT3


# In[657]:


allTimeImpulsSongs = 132 * 2.7
allTimeSinSongs = 33 * 0.2
res1 = 100*(allTimeImpulsSongs*0.0125 + allTimeSinSongs)/300
res1


# In[660]:


result_pd2 = pd.concat((result_pd , DFprocessingRESULT3 ))
result_pd2

with open("resultTableProcessing.pickle", 'wb') as flProc:
    pickle.dump(result_pd2, flProc)

