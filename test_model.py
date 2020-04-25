#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:41:31 2020

@author: mikehoefer
"""

import random

import requests

import os

import censusdata
import pandas as pd

from generate_households import generate_households

import cenpy

os.chdir('/Users/mikehoefer/Documents/courses/mult-agent-sys/project/python')

# each day composed of 24 hours

# schedule:
# 10 -> location_id
# 11 -> location_id

#class TransitionMatrix():
#    1 -> house: 100%
#    2 -> house: 100%
#    8 -> house: 10%, school: 90%
#    9 -> ...
#    4 -> house: 30%, restaurant: 30%, work: 40%



##############################################
####  SIMULATION CLASSES
##############################################

class Location(object):
    # Constructor 
    def __init__(self, name, kind, open_hours, capacity, is_public = False, num_employees_target=0): 
        self.name = name 
        self.kind = kind  # school, work, restaurant, home, etc
        self.open_hours = open_hours   # list of hours [12,13,14] == 12-2pm
        self.capacity = capacity
        self.current_tenants = []
        self.num_employees_target = num_employees_target
        self.is_public = is_public
        self.num_employees = 0
        self.is_closed = False
        
        #self.interaction_matrix # could be day by day
    

    def get_people_interactions():
#        # location specific infection logic here
#        for agent_self in self.current_tenants:
#            for agent_other in self.current_tenants:
#                # logic to determine if these agents interact
#                if (these_agents_interact):
#                    # save the fact that they interacted 
#                    update_interaction_matrix(agent_self, agent_other)
#                    run_agent_interaction(agent_self, agent_other)
#                
#                
#                if agent.workplace == self:
#                    # agent works here, higher infection chance possibly
#                else:
#                    # agent is just visiting
#                    
#                if agent_other.infection_status == "coughing":
#                    if random.rand() < .8:
#                        agent_self.infection_status = "infected"
#                else:
#                    if random.rand() < .3:
#                        # TODO location based infection logic
#                        # update list of agent interactors
#                        agent.interacted_list.append
        return False

    def update_interaction_matrix(agent1, agent2):
        self.interaction_matrix[agent1.age][agent2.age] += 1
    
    def has_infected_person(self):
        for agent in self.current_tenants:
            if agent.is_infected:
                return True
        return False

# idea: find the most critical agent interactions
        # what are the most common pathways through which infection occurs

class Agent(object):
    # Constructor 
    def __init__(self, name, workplace, home, age): 
        self.name = name     
        self.workplace = workplace
        self.home = home
        
        # using booleans for the SIR states to make processing faster
        self.is_infected = False
        self.is_immune = False
        self.is_recovered = False
        
        
        self.current_location = home
        self.current_location.current_tenants.append(self)
        self.age = age
        self.schedule = None

    # transition matrix


    def generate_daily_schedule(self, is_weekend = False):
        # TODO more intelligence needed here
        schedule = {}
        
        # assume first 7 hours are spent at home
        for i in range(7):
            schedule[i] = self.home
            
        
        # work/school for the next 9 hours
        for i in range (7, 17):
            schedule[i] = self.workplace
            
        
        # one random locations for the next few hours
        random_loc = random.choice([loc for loc in locations if loc.is_public])
        for i in range (17, 21):
            schedule[i] = random_loc


        # then return home
        for i in range (21, 23):
            schedule[i] = self.home
        
        self.schedule = schedule
        
        
    def change_location(self, new_loc):
        if self.current_location == new_loc:
            return
        
        self.current_location.current_tenants.remove(self)
        self.current_location = new_loc
        new_loc.current_tenants.append(self)
        
    def update_location_via_schedule(self, hour):
        self.change_location(self.schedule[hour])
        
    def go_to_work(self):
        self.change_location(self.workplace)
        
    def go_home(self):
        self.change_location(self.home)



##############################################
####  SIMULATION HELPER FUNCTIONS
##############################################


def universal_scheduler_sim(agents, locations, infection_percent = 0.01):
    # runs one day of the simulation, every agent following the same schedule
    for i in range(7):
        # first seven hours are at home - no contact while sleeping. How about that.
        continue
    
    
    # send everyone to work
    for agent in agents:
        agent.go_to_work()
    
    for i in range (7, 17):
        # see who gets infected for each hour of the day
        update_agent_status(infection_percent)
            
    # send everyone home
    for agent in agents:
        agent.go_home()
        
    # let people get infected at home
    for i in range (17, 23):
        # see who gets infected for each hour of the day
        update_agent_status(infection_percent)
    

# simple code that checks each agent's location, and flips a coin to see if 
# they become infected (there must be an infected person in the location)
def update_agent_status(infection_percent):
    # location mixing logic
    #for location in locations:
    #    location.get_people_interactions()
    
    
    for agent in agents:
        # infection logic
        # TODO more intelligence needed here
        if agent.current_location.has_infected_person():
            if random.random() < infection_percent:
                agent.is_infected = True

    return



##############################################
####  DATA GATHERING FUNCTIONS
##############################################

####
# CENSUS UTILITY FUNCTIONS
####
def get_county_and_state_id(county, state):
    state_id = ""
    county_id = ""
    geographical = censusdata.download('acs5', 2018, censusdata.censusgeo([('county', '*')]),['ANRC'])
    
    # Newport County, Rhode Island: Summary level: 050, state:44> county:005
    for index, row in geographical.iterrows():
        
        if str(index).split(",")[1].split(":")[0][1:] == state and str(index).split(",")[0]==county:
            county_id = str(index)[-3:]
            state_id = str(index)[-14:-12]
            break
        
    return county_id, state_id


#####
# BUSINESS FUNCTIONS
####

# returns a pandas DF of the query of the census business data
def pull_business_data(county_id, state_id):
    r = requests.get('https://api.census.gov/data/2017/cbp?get=' + 
                     'NAICS2017_LABEL,NAICS2017,ESTAB,INDGROUP,INDLEVEL,EMP,EMP_N,GEO_ID,LFO,LFO_LABEL,EMPSZES_LABEL,EMPSZES' + 
                     '&for=county:' + str(county_id)+ '&INDLEVEL=2&in=state:' + str(state_id) )
        
    business_raw = r.json()
    
    df = pd.DataFrame(business_raw)
    
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    return df


# creates synthetic businesses from the census dataframe
    # Max business size is necessary bc the census doesn't have a category
    # for businesses with more than 1k people...
def create_business_df (df, max_business_size = 2000, capacity=100):
    # business size lookup dict (size range)
    business_sizes = {'210' : (1, 4),
                      '220' : (5, 9),
                      '230' : (10, 19),
                      '241' : (20, 49),
                      '242' : (50, 99),
                      '251' : (100, 249),
                      '252' : (250, 499),
                      '254' : (500, 999),
                      '260' : (1000, max_business_size),
                      }
    
    
    # If the NAICS label is one of these, we'll call it public
    public_types = ['44-45',    # Retail Traide
                    '61',       # Educational Services
                    '72',       # Accomodation and Food Services
                    '62',       # Health care and social assistance
                    '71']       # Arts, entertainment, and recreation
                    
    
    # go through and construct the list of businesses 
    
    new_locations = []  # list of dicts to be turned into a DF
    counter = 0
    curr_type = ''
    
    for i, row in df.iterrows():
        
        # skip aggregated categories and categories representing all business sectors
        if str(row['EMPSZES']) == '001' or str(row['NAICS2017']) == '00':
            # skip aggregated categories
            continue
        else:
            if curr_type != row['NAICS2017_LABEL']:
                curr_type = row['NAICS2017_LABEL']
                counter = 0
            # make one location per ESTAB
            
            for j in range(int(row['ESTAB'])):
                curr_bus = {}
                curr_bus['business_id'] = row['NAICS2017_LABEL'] + '_' + str(counter)
                curr_bus['category'] = row['NAICS2017_LABEL']
                curr_bus['hours'] = [k for k in range(24)]
                curr_bus['capacity'] = capacity
                curr_bus['is_public'] = row['NAICS2017'] in public_types
                curr_bus['target_num_employees'] = random.randint(business_sizes[row['EMPSZES']][0], business_sizes[row['EMPSZES']][1])
                
                new_locations.append(curr_bus)
                counter += 1 
                
    return pd.DataFrame(new_locations)

# turns the synthetic business df into a list of objects
def create_business_objects(df):
    new_locs = []
    
    for i, row in df.iterrows():
        new_loc = Location(row['business_id'],     # business name
                           row['category'],                          # category
                           row['hours'],                          # open all hours of the day
                           row['capacity'],                                        # set capacity for now
                           row['is_public'],                # if business is open to public
                           row['target_num_employees'])  # num employees
        
        new_locs.append(new_loc)
        
    return new_locs


# quick check to see how many employees there should be
def calc_business_capacity(list_o_bus):
    running_total = 0
    for bus in list_o_bus:
        running_total += bus.num_employees_target
        
    return running_total


# see how many businesses we have of each type
def calc_business_qtys(list_o_bus):
    count = {}
    emps = {}
    for bus in list_o_bus:
        if bus.kind not in count.keys():
            count[bus.kind] = 1
            emps[bus.kind] = bus.num_employees_target
        else:
            count[bus.kind] += 1
            emps[bus.kind] += bus.num_employees_target
            
    return count, emps



#####
# AGENT FUNCTIONS
####
    
# pulls data from US census to generate list of agents
def create_agent_df(county_id, state_id):
    # Sky code here
    df = generate_households(county_id, state_id)
    
    return df



# takes Pandas DF and creates a list of agents
# this also constructs household locations!
# returns two lists: agent objects, and household (Location) objects
def build_agent_objects(agent_df):
    # agent is an ID, age, and HH
    
    # sort by HHid, so we can start by making a household, then assigning it
    raw_agents.sort_values('hhID')
    
    curr_hh_id = -1
    curr_hh = None
    
    
    hh_list = []
    agent_list = []
    for i, row in raw_agents.iterrows():
        # check if we're still in the same HH
        if row['hhID'] == curr_hh_id:
            # do not create new household
            pass
        else:
            # create new HH as a location, add to location list
            curr_hh_id = row['hhID']
            curr_hh = Location("hh_" + str(curr_hh_id),     # business name
                                       "home",                          # category
                                       [k for k in range(24)],                          # open all hours of the day
                                       0,                                        # set capacity for now
                                       False,                # if business is open to public
                                       0)  # num employees
            hh_list.append(curr_hh)
        
        # create the agent
        new_agent = Agent('Agent' + str(i), # name - not really needed
                            None,   # workplace assigned later
                            curr_hh,   # home
                            row['age'])  # age
        agent_list.append(new_agent)
        
    return agent_list, hh_list

def get_number_of_workers(list_o_agents, working_age = 18):
    worker_count = 0
    lazy_count = 0
    
    for agent in list_o_agents:
        if agent.age >= working_age:
            worker_count += 1
        else:
            lazy_count +=1
            
    return worker_count, lazy_count



###
# ASSIGNMENT OF AGENTS TO BUSINESSES
###
def assign_agents_to_bus(agents, businesses, working_age = 18, retirement_age=70):
    # rather than randomly assign individuals to businesses
    # which would represent more of a "fully mixed" model,
    # we seek to effectively simulate localized clustering
    # through sequential assignment of agents to business
    
    # we will assume that if you're over 18, you work.
    
    # eh... for now... randomly assign... let's assume the locality
    # is small enough that geography is not a constraint... hmm
    
    # because we may have more workers than business slots, we need to randomly
    # assign unemployment - in this case - we will shuffle the list
    # and assign sequentially.  This is effectively random employment
    random.shuffle(agents)
    
    
    # create new list - every business can hire to start
    eligible_bus = list(businesses)
    
    jobs_left = True
    
    for agent in agents:
        if agent.age >= working_age and agent.age <= retirement_age:
            # we have a worker!
            
            # if no jobs left, they work at home
            if not jobs_left:
                agent.workplace = agent.home
            else:
                # pick a business randomly:
                bus_candidate = random.choice(eligible_bus)
                
                agent.workplace = bus_candidate
                
                bus_candidate.num_employees += 1
                
                # if business is at capacity, remove from eligible list
                if bus_candidate.num_employees == bus_candidate.num_employees_target:
                    eligible_bus.remove(bus_candidate)
                    if not eligible_bus:
                        # if the list is empty - we're out of jobs!
                        jobs_left = False
        else:
            # youngster, assign workplace to home for now. Schools coming later
            agent.workplace = agent.home
                
    return # nothing to return here
 
##############################################
#### FUNCTIONS TO RUN THE SIMULATION
##############################################

county = "Summit County"
state = "Utah"

county_id, state_id = get_county_and_state_id(county, state)


# CREATE BUSINESSES

# aggregated frame
bus_agg_df = pull_business_data(county_id, state_id)

# make synthetic frame
bus_locs_df = create_business_df(bus_agg_df)

# save synthetic businesses for simulation repeatability
bus_locs_df.to_csv("synthetic_business_locations.csv")

bus_locs = create_business_objects(bus_locs_df)


# CHECKING BASIC STATS BEFORE RUNNING
count = calc_business_capacity(bus_locs)    
print ("We have", count, "jobs available.")

### extra stats if need be
#num_bus, num_emps = calc_business_qtys(bus_locs)


# CREATE AGENTS and HOUSEHOLDS

#raw_agents = pd.read_csv('agents.csv')


# takes some time - use debug=True for verbose
raw_agents = create_agent_df(county_id, state_id)


# save off agent CSV for future use
raw_agents.to_csv('agent_df_summit.csv')

agents, households = build_agent_objects(raw_agents)



workers, non_workers = get_number_of_workers(agents, working_age = 18)


# assign agents to businesses
assign_agents_to_bus(agents, bus_locs, 18, 70)


locations = bus_locs + households

# READY TO RUN SIM!


# randomly infect one person

num_initially_infected = 10

for i in range (num_initially_infected):
    random.choice(agents).is_infected = True

# percent chance of being infected if you are at a location with an infected person
chance_of_infection = .01

num_days = 5


num_agents = len(agents)


# run the simulation - UNIVERSAL SCHEDULER
for i in range(num_days):
    
    universal_scheduler_sim(agents, locations)
        
    # print stats
    num_infected = len([agent for agent in agents if agent.is_infected])
    print("After day", i, "there are", num_infected, "infected out of ", num_agents)
        





### OLD - IGNORE FOR NOW ####


# run the simulation - CUSTOM SCHEDULER --> SLOW 
for i in range(num_days):
    
    # generate every agent's schedule
    for k, agent in enumerate(agents):
        agent.generate_daily_schedule(False)
        if k % 1000 == 0:
            print("generated", k, "schedules out of", num_agents)
        
    print("Done generating schedules for day", i)
    
    for j in range(23):
        # update agent location
        for agent in agents:
            agent.update_location(j)
            
        # run infection logic
        update_agent_status(chance_of_infection)
        
        
    # print stats
    num_infected = len([agent for agent in agents if agent.infection_status == 'infected'])
    num_susceptible = len([agent for agent in agents if agent.infection_status == 'susceptible'])
    print("After day", i, "there are", num_infected, "infected out of ", num_infected + num_susceptible)
        


##############################################
#### EXPERIMENTING WITH SIMULATION RUNS
##############################################

    # Coming soon
    
    



















##############################################
#### OLD
##############################################



# CENSUS scratching
import cenpy
County = "Boulder County"
State = "Colorado"

state_id = ""
county_id = ""
geographical = censusdata.download('acs1', 2018, censusdata.censusgeo([('county', '*')]),['ANRC'])

# Newport County, Rhode Island: Summary level: 050, state:44> county:005
for index, row in geographical.iterrows():
    
    if str(index).split(",")[1].split(":")[0][1:] == State and str(index).split(",")[0]==County:
        county_id = str(index)[-3:]
        state_id = str(index)[-14:-12]
        break
    
    
print("State ID:", state_id, "\nCounty ID:", county_id)    



GenderAgeRaw = censusdata.download('acs1', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
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

    
# gather households
    
    
houseHolds = censusdata.download('acs1', 2018, censusdata.censusgeo([('state',str(state_id)),('county', str(county_id))]),
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



# getting businesses
    


# business size lookup dict (size range)
business_sizes = {'210' : (1, 4),
                  '220' : (5, 9),
                  '230' : (10, 19),
                  '241' : (20, 49),
                  '242' : (50, 99),
                  '251' : (100, 249),
                  '252' : (250, 499),
                  '254' : (500, 999),
                  '260' : (1000,2000),
                  }

# go through and construct the list of businesses 

new_locations = []
counter = 0
curr_type = ''
for i, row in df.iterrows():
    if row['EMPSZES'] == '001':
        # skip aggregated categories
        continue
    else:
        if curr_type != row['NAICS2017_LABEL']:
            curr_type = row['NAICS2017_LABEL']
            counter = 0
        # make one location per ESTAB
        for j in range(int(row['ESTAB'])):
            new_loc = Location(row['NAICS2017_LABEL'] + '_' + str(counter), 
                               row['NAICS2017_LABEL'], 
                               [k for k in range(24)], 
                               100, 
                               random.randint(business_sizes[row['EMPSZES']][0], business_sizes[row['EMPSZES']][1]))
            new_locations.append(new_loc)
            counter += 1 
            


df['EMP'].astype(int).sum()

# so we will limit ourselves to where INDLEVEL is 2.
df.to_csv('Boulder-Businesses.csv')

# school scratching

# read in colorado schools

schools = pd.read_csv('COLORADO-SCHOOLS.csv')


schools_all = pd.read_csv('ccd_SCH_052_1819_l_1a_091019.csv', encoding='cp1252') #, nrows=1000)

schools_sum = pd.read_csv('ccd_SCH_052_1819_l_1a_091019.csv', encoding='cp1252', nrows=1000)


# Aggregate by school to get the student count per school
schools_sum.groupby("ST_SCHID").STUDENT_COUNT.sum()
test = schools_all.aggregate()

schools2 = pd.read_csv('ccd_SCH_052_1819_l_1a_091019.csv', encoding='cp1252', nrows=10000) #, nrows=1000)






# agent work

#homes = pd.read_csv('houseHolds.csv')

























# census scratching

import cenpy
from cenpy import products
import matplotlib.pyplot as plt
%matplotlib inline
acs = cenpy.products.ACS()
acs.from_place('Boulder County, CO')



chicago = products.ACS(2018).from_place('CO', level='block',
                                        variables=['A*', 'B01001_003E'])

f, ax = plt.subplots(1,1,figsize=(20,20))
chicago.dropna(subset=['B00002_001E'], axis=0).plot('B00002_001E', ax=ax, cmap='plasma')
ax.set_facecolor('k')















    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import pandas as pd
import censusdata
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)



censusdata.search('acs5', 2015, 'label', 'unemploy')[160:170]    


censusdata.printtable(censusdata.censustable('acs5', 2015, 'B23025'))    


censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', 2015)    
    
    
    
    
    
    
    
    
censusdata.geographies(censusdata.censusgeo([('state', '08'), ('county', '013')]), 'acs5', 2015)
    
    
    
censusdata.geographies(censusdata.censusgeo([('state', '08'), ('county', '013')]), 'acs5', 2018)
    
    
boulder = censusdata.censusgeo([('state', '08'), ('county', '013')])
    
    

cookbg = censusdata.download('acs5', 2015, boulder, ['B00002_001E'])
cookbg    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    











