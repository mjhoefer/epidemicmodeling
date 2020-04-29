#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import censusdata
import numpy as np
import matplotlib.pyplot as plt
#pd.set_option('display.expand_frame_repr', False)
#pd.set_option('display.precision', 2)


# ### For target county find state and county codes to access data in US census


def generate_households(county_id, state_id, debug= False):

    
    # ### Retrieve age distribution of population

    
    GenderAgeRaw = censusdata.download('acs5', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
                                     ["B01001_001E",
                                      "B01001_002E",
                                      "B01001_003E",
                                      "B01001_004E",
                                      "B01001_005E",
                                      "B01001_006E",
                                      "B01001_007E",
                                      "B01001_008E",
                                      "B01001_009E",
                                      "B01001_010E",
                                      "B01001_011E",
                                      "B01001_012E",
                                      "B01001_013E",
                                      "B01001_014E",
                                      "B01001_015E",
                                      "B01001_016E",
                                      "B01001_017E",
                                      "B01001_018E",
                                      "B01001_019E",
                                      "B01001_020E",
                                      "B01001_021E",
                                      "B01001_022E",
                                      "B01001_023E",
                                      "B01001_024E",
                                      "B01001_025E",
                                      "B01001_026E",
                                      "B01001_027E",
                                      "B01001_028E",
                                      "B01001_029E",
                                      "B01001_030E",
                                      "B01001_031E",
                                      "B01001_032E",
                                      "B01001_033E",
                                      "B01001_034E",
                                      "B01001_035E",
                                      "B01001_036E",
                                      "B01001_037E",
                                      "B01001_038E",
                                      "B01001_039E",
                                      "B01001_040E",
                                      "B01001_041E",
                                      "B01001_042E",
                                      "B01001_043E",
                                      "B01001_044E",
                                      "B01001_045E",
                                      "B01001_046E",
                                      "B01001_047E",
                                      "B01001_048E",
                                      "B01001_049E"
                                     ])
    GenderAgeRaw = GenderAgeRaw.rename(columns={
                                      "B01001_001E":"Total",
                                      "B01001_002E":"Total Male",
                                      "B01001_003E":"Male [00-04]",
                                      "B01001_004E":"Male [05-09]",
                                      "B01001_005E":"Male [10-14]",
                                      "B01001_006E":"Male [15-17]",
                                      "B01001_007E":"Male [18-19]",
                                      "B01001_008E":"Male [20-20]",
                                      "B01001_009E":"Male [21-21]",
                                      "B01001_010E":"Male [22-24]",
                                      "B01001_011E":"Male [25-29]",
                                      "B01001_012E":"Male [30-34]",
                                      "B01001_013E":"Male [35-39]",
                                      "B01001_014E":"Male [40-44]",
                                      "B01001_015E":"Male [45-49]",
                                      "B01001_016E":"Male [50-54]",
                                      "B01001_017E":"Male [55-59]",
                                      "B01001_018E":"Male [60-61]",
                                      "B01001_019E":"Male [62-64]",
                                      "B01001_020E":"Male [65-66]",
                                      "B01001_021E":"Male [67-69]",
                                      "B01001_022E":"Male [70-74]",
                                      "B01001_023E":"Male [75-79]",
                                      "B01001_024E":"Male [80-84]",
                                      "B01001_025E":"Male [85-99]",
                                      "B01001_026E":"Total Female",
                                      "B01001_027E":"Female [00-04]",
                                      "B01001_028E":"Female [05-09]",
                                      "B01001_029E":"Female [10-14]",
                                      "B01001_030E":"Female [15-17]",
                                      "B01001_031E":"Female [18-19]",
                                      "B01001_032E":"Female [20-20]",
                                      "B01001_033E":"Female [21-21]",
                                      "B01001_034E":"Female [22-24]",
                                      "B01001_035E":"Female [25-29]",
                                      "B01001_036E":"Female [30-34]",
                                      "B01001_037E":"Female [35-39]",
                                      "B01001_038E":"Female [40-44]",
                                      "B01001_039E":"Female [45-49]",
                                      "B01001_040E":"Female [50-54]",
                                      "B01001_041E":"Female [55-59]",
                                      "B01001_042E":"Female [60-61]",
                                      "B01001_043E":"Female [62-64]",
                                      "B01001_044E":"Female [65-66]",
                                      "B01001_045E":"Female [67-69]",
                                      "B01001_046E":"Female [70-74]",
                                      "B01001_047E":"Female [75-79]",
                                      "B01001_048E":"Female [80-84]",
                                      "B01001_049E":"Female [85-99]"
         
                                })
    
    
    
    
    # ### Normalize age distribution to 5 year increments and aggregate gender
    
    # In[4]:
    
    
    AgeDist = pd.DataFrame()
    AgeDist["Total"] = GenderAgeRaw["Total"]
    AgeDist["00-04"] = GenderAgeRaw["Male [00-04]"] + GenderAgeRaw["Female [00-04]"]
    AgeDist["05-09"] = GenderAgeRaw["Male [05-09]"] + GenderAgeRaw["Female [05-09]"]
    AgeDist["10-14"] = GenderAgeRaw["Male [10-14]"] + GenderAgeRaw["Female [10-14]"]
    AgeDist["15-17"] = GenderAgeRaw["Male [15-17]"] + GenderAgeRaw["Female [15-17]"]
    AgeDist["18-24"] = GenderAgeRaw["Male [20-20]"] + GenderAgeRaw["Female [20-20]"] + GenderAgeRaw["Male [18-19]"] + GenderAgeRaw["Female [18-19]"] + GenderAgeRaw["Male [21-21]"] + GenderAgeRaw["Female [21-21]"]  + GenderAgeRaw["Male [22-24]"] + GenderAgeRaw["Female [22-24]"]
    AgeDist["25-29"] = GenderAgeRaw["Male [25-29]"] + GenderAgeRaw["Female [25-29]"]
    AgeDist["30-34"] = GenderAgeRaw["Male [30-34]"] + GenderAgeRaw["Female [30-34]"]
    AgeDist["35-39"] = GenderAgeRaw["Male [35-39]"] + GenderAgeRaw["Female [35-39]"]
    AgeDist["40-44"] = GenderAgeRaw["Male [40-44]"] + GenderAgeRaw["Female [40-44]"]
    AgeDist["45-49"] = GenderAgeRaw["Male [45-49]"] + GenderAgeRaw["Female [45-49]"]
    AgeDist["50-54"] = GenderAgeRaw["Male [50-54]"] + GenderAgeRaw["Female [50-54]"]
    AgeDist["55-59"] = GenderAgeRaw["Male [55-59]"] + GenderAgeRaw["Female [55-59]"]
    AgeDist["60-64"] = GenderAgeRaw["Male [62-64]"] + GenderAgeRaw["Male [60-61]"] + GenderAgeRaw["Female [62-64]"] + GenderAgeRaw["Female [60-61]"]
    AgeDist["65-69"] = GenderAgeRaw["Male [65-66]"] + GenderAgeRaw["Male [67-69]"] + GenderAgeRaw["Female [65-66]"] + GenderAgeRaw["Female [67-69]"]
    AgeDist["70-74"] = GenderAgeRaw["Male [70-74]"] + GenderAgeRaw["Female [70-74]"]
    AgeDist["75-79"] = GenderAgeRaw["Male [75-79]"] + GenderAgeRaw["Female [75-79]"]
    AgeDist["80-84"] = GenderAgeRaw["Male [80-84]"] + GenderAgeRaw["Female [80-84]"]
    AgeDist["85-99"] = GenderAgeRaw["Male [85-99]"] + GenderAgeRaw["Female [85-99]"]

    
    # ### Retrieve household distribution data
    
    # In[6]:
    
    
    houseHolds = censusdata.download('acs5', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
                               ['B11016_001E',
                                'B11016_002E',
                                'B11016_003E',
                                'B11016_004E',
                                'B11016_005E',
                                'B11016_006E',
                                'B11016_007E',
                                'B11016_008E',
                                'B11016_009E',
                                'B11016_010E',
                                'B11016_011E',
                                'B11016_012E',
                                'B11016_013E',
                                'B11016_014E',
                                'B11016_015E',
                                'B11016_016E',
                                'B09002_001E',
                                'B09002_002E',
                                'B09002_008E'
                                ])
    
    houseHolds = houseHolds.rename(columns={'B11016_001E': "Total Housholds",
                                'B11016_002E': "Total Family Households",
                                'B11016_003E': "2 p Family Households",
                                'B11016_004E': "3 p Family Households",
                                'B11016_005E': "4 p Family Households",
                                'B11016_006E': "5 p Family Households",
                                'B11016_007E': "6 p Family Households",
                                'B11016_008E': "7+ p Family Households",
                                'B11016_009E': "Total Non-Family Households",
                                'B11016_010E': "1 p Non-Family Households",
                                'B11016_011E': "2 p Non-Family Households",
                                'B11016_012E': "3 p Non-Family Households",
                                'B11016_013E': "4 p Non-Family Households",
                                'B11016_014E': "5 p Non-Family Households",
                                'B11016_015E': "6 p Non-Family Households",
                                'B11016_016E': "7+ p Non-Family Households",
                                'B09002_001E': "Household w/ Children",
                                'B09002_002E': "Married Couple w/ Children",
                                'B09002_008E': 'Single Parent w/ Children'
                                            
                                })
    
    houseHolds.head()
    
 
  
    
    houseHolds["2 p Family Households"].values[0]
    singleVmarried = [houseHolds["Married Couple w/ Children"].values[0],houseHolds["Single Parent w/ Children"].values[0]]/houseHolds["Household w/ Children"].values[0]
    childrenVnone = []
    
 
    
    birthDist = censusdata.download('acs5', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
                                     [
                                         'B13016_001E',
                                         'B13016_002E',
                                         'B13016_003E',
                                         'B13016_004E',
                                         'B13016_005E',
                                         'B13016_006E',
                                         'B13016_007E',
                                         'B13016_008E',
                                         'B13016_009E',
                                         'B13016_010E',
                                         'B13016_011E',
                                         'B13016_012E',
                                         'B13016_013E',
                                         'B13016_014E',
                                         'B13016_015E',
                                         'B13016_016E',
                                         'B13016_017E'              
                                     ])
    birthDist = birthDist.rename(columns={
                                         'B13016_001E': 'Total',
                                         'B13016_002E': 'Total Women had birth [15-50]',
                                         'B13016_003E': 'Women had birth [15-19]',
                                         'B13016_004E': 'Women had birth [20-24]',
                                         'B13016_005E': 'Women had birth [25-29]',
                                         'B13016_006E': 'Women had birth [30-34]',
                                         'B13016_007E': 'Women had birth [35-39]',
                                         'B13016_008E': 'Women had birth [40-44]',
                                         'B13016_009E': 'Women had birth [45-50]',
                                         'B13016_010E': 'Total Women did not have birth [15-50]',
                                         'B13016_011E': 'Women no birth [15-19]',
                                         'B13016_012E': 'Women no birth [20-24]',
                                         'B13016_013E': 'Women no birth [25-29]',
                                         'B13016_014E': 'Women no birth [30-34]',
                                         'B13016_015E': 'Women no birth [35-39]',
                                         'B13016_016E': 'Women no birth [40-44]',
                                         'B13016_017E': 'Women no birth [45-50]'                                      
                                })
    
    
    schoolDist = censusdata.download('acs5', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
                                     [
                                         'B14001_001E',
                                         'B14001_002E',    
                                         'B14001_003E',
                                         'B14001_004E',
                                         'B14001_005E',
                                         'B14001_006E',
                                         'B14001_007E',
                                         'B14001_008E',
                                         'B14001_009E',
                                         'B14001_010E'
                                     ])
    schoolDist = schoolDist.rename(columns={
                                         'B14001_001E':'Total',
                                         'B14001_002E':'Enrolled in school',    
                                         'B14001_003E':'Enrolled in school [03-04]',
                                         'B14001_004E':'Enrolled in school [05-06]',
                                         'B14001_005E':'Enrolled in school [07-10]',
                                         'B14001_006E':'Enrolled in school [11-14]',
                                         'B14001_007E':'Enrolled in school [15-18]',
                                         'B14001_008E':'Enrolled in school [19-23]',
                                         'B14001_009E':'Enrolled in school [23-40]',
                                         'B14001_010E':'Not enrolled in school'                                      
                                })
    schoolDist.head()
    

    
    # https://en.wikipedia.org/wiki/Age_disparity_in_sexual_relationships
    
    

    
    familyVnonfamily =  [houseHolds["Total Family Households"].values[0] ,houseHolds["Total Non-Family Households"].values[0]]/houseHolds["Total Housholds"].values[0]
    singleVmarried
    
    
    
    familyHouseholdProd = [0,0,houseHolds["2 p Family Households"].values[0],houseHolds["3 p Family Households"].values[0],houseHolds["4 p Family Households"].values[0],houseHolds["5 p Family Households"].values[0],houseHolds["6 p Family Households"].values[0],houseHolds["7+ p Family Households"].values[0]]/houseHolds["Total Family Households"].values[0]
    nonfamilyHouseholdProd = [0,houseHolds["1 p Non-Family Households"].values[0],houseHolds["2 p Non-Family Households"].values[0],houseHolds["3 p Non-Family Households"].values[0],houseHolds["4 p Non-Family Households"].values[0],houseHolds["5 p Non-Family Households"].values[0],houseHolds["6 p Non-Family Households"].values[0],houseHolds["7+ p Non-Family Households"].values[0]]/houseHolds["Total Non-Family Households"].values[0]
    familyVnonfamily =  [houseHolds["Total Family Households"].values[0] ,houseHolds["Total Non-Family Households"].values[0]]/houseHolds["Total Housholds"].values[0]
    singleVmarried = [houseHolds["Married Couple w/ Children"].values[0],houseHolds["Single Parent w/ Children"].values[0]]/houseHolds["Household w/ Children"].values[0]
    
    
    class Household:
        def __init__(self, ID, size, family):  
            self.ID = ID
            self.size = size
            self.family = family
            self.members = []
            
    
    class Agent:
        def __init__(self, ID, hhID, age):  
            self.ID = ID
            self.age = age
            self.hhID = hhID

    
    agents = pd.DataFrame({"ID":[],"age":[],"hhID":[]})
    households = pd.DataFrame({"ID":[],"size":[],"family":[]})
    
    # Create a list of individuals
    Individuals = np.zeros(100)
    for rang in AgeDist.columns.values.tolist()[1:]:
        rangePop = AgeDist[rang].values[0]
        lower = int(rang[0:2])
        upper = int(rang[3:])
        for i in range(AgeDist[rang].values[0]):
            Individuals[(np.random.randint(lower,upper+1))] += 1
    
    iID = 1
    hhID = 1     
    counter = 0
    while sum(Individuals) > 3000 and counter < 10000: 
        IndvTemp = Individuals.copy()
        #1. Generate Household attributes
    
        # Decided whether this household is a family
        isFamily = np.random.choice([True,False], p=familyVnonfamily)
    
        # Pick household size based on if family or non-family
        if isFamily:
            householdSize = np.random.choice(list(range(0,8)), p=familyHouseholdProd)
        else:
            householdSize = np.random.choice(list(range(0,8)), p=nonfamilyHouseholdProd)
    
        # Generate ID for household
    
        # Create Household Object
        household = Household(hhID, householdSize, isFamily)
    
        #2. Generate people for the household
        if isFamily:
            head = Agent(iID, hhID, np.random.choice(list(range(len(IndvTemp[18:]))), p = IndvTemp[18:]/sum(IndvTemp[18:])))
            
            if IndvTemp[head.age] < 1:
                counter += 1
                if debug:
                    print("Unable to generate household",counter,"\n trying again")
                continue
            else:
                IndvTemp[head.age] = IndvTemp[head.age] - 1         
                household.members.append(head)
                iID += 1
                
            Married = np.random.choice([True, False], p = familyVnonfamily)
    
            if Married:
                householdSize -= 1
                age = round(np.random.normal(head.age, 2))
                
                if IndvTemp[age] < 1:
                    counter += 1
                    if debug:
                        print("Unable to generate household",counter,"\n trying again")
                    continue
                else:
                    spouse = Agent(iID,hhID,age)
                    IndvTemp[spouse.age] -= 1
                    household.members.append(spouse)
                    iID += 1
    
            for i in range(householdSize-1):
                age = np.random.choice(list(range(len(IndvTemp[18:]))), p = IndvTemp[18:]/sum(IndvTemp[18:]))
    
                if age > 99 or IndvTemp[age] < 1:
                    counter += 1
                    if debug:
                        print("Unable to generate household",counter,"\n trying again")
                    break
                    
                child = Agent(iID,hhID,age)
                IndvTemp[child.age] -= 1
                household.members.append(child)
                iID += 1
            
            if IndvTemp[age] < 1:
                    continue
    
        else:
            head = Agent(iID, hhID, np.random.choice(list(range(len(IndvTemp[18:]))), p = IndvTemp[18:]/sum(IndvTemp[18:])))
            
            if IndvTemp[head.age] > 99 or IndvTemp[age] < 1:
                if debug:
                    print("Unable to generate household",counter,"\n trying again")
                counter += 1
                continue
            else:
                IndvTemp[head.age] = IndvTemp[head.age] - 1
            
            household.members.append(head)
            iID += 1
            # Business assigning logic potentially here
    
            # Generate roomates of head
            for i in range(householdSize-1):
                age = round(np.random.normal(head.age, round(head.age/10)))
                
                attempts = 0
                
                if age > 99 or IndvTemp[age] < 1:
                    counter += 1
                    if debug:
                        print("Unable to generate household",counter,"\n trying again")
                    break
                else:
                    roomate = Agent(iID,hhID,age)
                    IndvTemp[roomate.age] = IndvTemp[roomate.age] - 1
                    household.members.append(roomate)
                    iID += 1
            
            if IndvTemp[age] < 1:
                continue
        
        if sum(IndvTemp < 0) == 0:
            counter = 0
            hhID += 1
            households = households.append({"ID" : household.ID,"size": household.size, "family": household.family} , ignore_index=True)
            for p in household.members:
                agents = agents.append({'ID' : p.ID,'age': p.age, 'hhID' : p.hhID}, ignore_index=True)
            Individuals = IndvTemp.copy()
    
    
    
    households.to_csv('households_'+county_id+'_'+state_id+'.csv', encoding='utf-8')
    agents.to_csv('agents_'+county_id+'_'+state_id+'.csv', encoding='utf-8')
    
    return agents
    
    # In[ ]:
    

def generate_households_by_name(county, state):
        
    state_id = ""
    county_id = ""
    geographical = censusdata.download('acs5', 2018, censusdata.censusgeo([('county', '*')]),['ANRC'])
    # Newport County, Rhode Island: Summary level: 050, state:44> county:005
    for index, row in geographical.iterrows():
        if str(index).split(",")[1].split(":")[0][1:].lower() == state.lower():
            print(str(index).split(",")[0].lower())
        if str(index).split(",")[1].split(":")[0][1:].lower() == state.lower() and str(index).split(",")[0].lower()==county.lower():
            county_id = str(index)[-3:]
            state_id = str(index)[-14:-12]
            break
        
        
    generate_households(county_id, state_id)
        
    
    
   
#test = generate_households_by_name('summit county', 'utah')

