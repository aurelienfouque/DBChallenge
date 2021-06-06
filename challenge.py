#!/usr/bin/env python
# coding: utf-8

# # Data engineering challenge

# In[3]:


# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# # Discover the data
# 
# Comma instead of dot -> Solved by 'decimal='.
# 
# Characters not recognised -> Solved by renaming.
# 
# Duplicates -> solved by replacing.

# In[6]:


# read .csv file
ku = pd.read_csv('Kuendigungen_2017.csv', sep=';', decimal=',')
ku.columns.values[4] = 'Jahre_Firmenzugehoerigkeit'
ku.columns.values[9] = 'hat_gekuendigt_2017'
ku = ku.replace('Produkt-Management', 'Produktmanagement')


# In[5]:


# print data frame
ku


# # Not everyone answered the survey (14987 < 14999)
# # Nan: not a number

# In[7]:


# quick view of the data
ku.describe()


# In[8]:


# one example of what is wrong and where
incomp = ku['Zufriedenheit_MA_Befragung']
loc_odd, = np.where(incomp.isnull())
# print('size:', loc_odd.size, '\n')
# print(loc_odd, '\n')
incomp[150:160]


# # We can notice clusters in the representation

# In[9]:


# attempt to see reason why people resign

kur = ku.loc[np.random.choice(ku.index, 1000, replace=False)]
visu = sns.PairGrid(kur, diag_sharey=False, corner=True,
   vars=['Zufriedenheit_MA_Befragung',
         'Performance_letztesJahr',
         'Arbeitsstunden_Monat_Schnitt',
        ], hue='hat_gekuendigt_2017')
        
#'Bereich'
#'Gehaltsgruppe'       
#'Befoerderung_letzte3Jahre'
#'Hatte_Betriebsunfall'
#'Jahre_Firmenzugehoerigkeit'
#'Anzahl_Projekte_letztesJahr'

visu.map_diag(sns.kdeplot, alpha=0.5, fill=True)
visu.map_offdiag(sns.scatterplot, alpha=0.5)
visu.add_legend()
visu.savefig('cor.pdf')


# In[10]:


# number of people who resigned from where
item = ku.columns.tolist()
resignedOrNotWhere = ku.groupby([item[-1], item[-3]])
resignedWhere = resignedOrNotWhere.size()[1]
resigned = ku.groupby(item[-1]).size()
total = resigned.sum()
peopleByDomain = ku.groupby(item[-3]).size()
total =resignedOrNotWhere.size().sum()


# In[11]:


pd.DataFrame([resigned.values, 100*resigned/total],
   columns=['geblieben', 'gekündigt'],
   index=['Zahl', '%']).T


# In[13]:


resignedTab = pd.DataFrame([resignedWhere,
                            peopleByDomain, 
                            100*resignedWhere/peopleByDomain],
                            index=['gekündigt', 'Personen', '%']).T
resignedTab.sort_values(by=['%'])


# In[14]:


plt.xticks(rotation=45, ha='right')
resignedPlot = resignedTab.sort_values(by=['%'])['%']
plt.bar(resignedPlot.index, height=resignedPlot)
plt.grid(True)
plt.savefig('gek.pdf')


# In[15]:


# numbers of working hours per person

hoursByDomain = ku.groupby([item[-3]]).sum()[item[3]]
tabHoursPeople = pd.DataFrame([hoursByDomain,
                                peopleByDomain,
                                hoursByDomain/peopleByDomain], 
                              index=['Sum_St_Pro_Mo', 'Personen', 'St./P.']).T
tabHoursPeople


# In[16]:



plotHoursPeople = tabHoursPeople.sort_values(by=['St./P.'])['St./P.']
plt.xticks(rotation=45, ha='right')
plt.ylim(190, 204)
plt.bar(plotHoursPeople.index, height=plotHoursPeople)
plt.grid(True)
plt.savefig('work.pdf')

