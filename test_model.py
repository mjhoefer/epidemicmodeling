#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:41:31 2020

@author: mikehoefer
"""

import random

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



class Location(object):
    # Constructor 
    def __init__(self, name, kind, open_hours, capacity): 
        self.name = name 
        self.kind = kind  # school, work, restaurant, etc
        self.open_hours = open_hours   # list of hours [12,13,14] == 12-2pm
        self.capacity = capacity
     
    
        self.current_tenants = []
        
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
            if agent.infection_status == 'infected':
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
        self.infection_status = 'susceptible'
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
        for i in range (17, 21):
            schedule[i] = random.choice([loc for loc in locations if loc.kind != 'Home'])


        # then return home
        for i in range (21, 23):
            schedule[i] = self.home
        
        self.schedule = schedule
        
        
    def update_location(self, hour):
        self.current_location.current_tenants.remove(self)
        self.current_location = self.schedule[hour]
        self.current_location.current_tenants.append(self)


def update_agent_status(infection_percent):
    # location mixing logic
    #for location in locations:
    #    location.get_people_interactions()
    
    
    for agent in agents:
        # infection logic
        # TODO more intelligence needed here
        if agent.current_location.has_infected_person():
            if random.random() < infection_percent:
                agent.infection_status = "infected"

    return





locations = []
agents = [] 


# Create locations
locations.append(Location("The Downer", 'Restaurant', [10,11,12,13,14,15,16,17,18,19,20,21,22,23], 100))
locations.append(Location("CU Boulder", 'School', [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 30000))
locations.append(Location("King Soopers", 'Grocery', [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 200))
locations.append(Location("3009 Madison Ave Apt J 208", 'Home', [i for i in range(23)], 5))



# Create agents
num_agents = 10

for i in range(num_agents):
    agents.append(Agent('Agent' + str(i), 
                        random.choice([loc for loc in locations if loc.kind != 'Grocery']), 
                        random.choice([loc for loc in locations if loc.kind == 'Home']),
                        random.randint(10,90)))




# randomly infect one person
random.choice(agents).infection_status = 'infected'

chance_of_infection = .01

num_days = 5

for i in range(num_days):
    
    # generate every agent's schedule
    for agent in agents:
        agent.generate_daily_schedule(False)
    
    for j in range(23):
        # update agent location
        for agent in agents:
            agent.update_location(j)
            
        # run infection logic
        update_agent_status(chance_of_infection)
        
        
    num_infected = len([agent for agent in agents if agent.infection_status == 'infected'])
    num_susceptible = len([agent for agent in agents if agent.infection_status == 'susceptible'])
    print("After day", i, "there are", num_infected, "infected out of ", num_infected + num_susceptible)
        


    


























