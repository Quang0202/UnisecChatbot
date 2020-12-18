# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 21:54:19 2019

@author: Huong
"""
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
interpreter = RasaNLUInterpreter('models/current/nlu')
agent = Agent.load("models/current/dialogue", interpreter=interpreter)

from RasaHost import host
host.nlu_path = "./data/nlu/"
host.stories_path = "./data/stories/"
host.domain_path = "./data/domain.yml"
host.agent = agent
if __name__ == '__main__':    
    host.run()