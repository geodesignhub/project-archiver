import requests, json, GeodesignHub
import os, sys
import time
import pandas as pd
import logging
import logging.handlers
from json.decoder import JSONDecodeError
from pathlib import Path

class ScriptLogger():
    def __init__(self):
        self.log_file_name = 'logs/latest.log'
        self.path = os.getcwd()
        self.logpath = os.path.join(self.path, 'logs')
        self.outputpath = os.path.join(self.path, 'output')
        if not os.path.exists(self.logpath):
            os.mkdir(self.logpath)
        if not os.path.exists(self.outputpath):
            os.mkdir(self.outputpath)
        self.logging_level = logging.INFO
        # set TimedRotatingFileHandler for root
        self.formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
        self.handler = logging.handlers.TimedRotatingFileHandler(self.log_file_name, when="S", interval=30, backupCount=10)
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger() # or pass string to give it a name
        self.logger.addHandler(self.handler)
        self.logger.setLevel(self.logging_level)
    def getLogger(self):
        return self.logger


if __name__ == "__main__":

    myLogger = ScriptLogger()
    logger = myLogger.getLogger()
    session = requests.Session()
    logger.info("Starting job")
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    try: 
      with open('config.json') as config:
        c = json.load(config)
    except JSONDecodeError as je: 
      print("Error reading config file")
      logger.info("Error reading config file")
      sys.exit(1)

    except Exception as e: 
      print("Error reading config file")
      logger.error("Error reading config file")
      sys.exit(1)

    try:
      assert c.keys() ==set(['serviceurl', 'projectid', 'apitoken'])
    except AssertionError as ae: 
      logger.error("Error in config file parameters")
      sys.exit(1)

    my_api_helper = GeodesignHub.GeodesignHubClient(url = c['serviceurl'], project_id= c['projectid'], token=c['apitoken'])

    # make project folder
    project_directory = Path("output", c['projectid'])
    project_directory.mkdir(parents=True, exist_ok=True)

    # Get all Systems
    all_systems_response = my_api_helper.get_all_systems()
    if all_systems_response.status_code == 200:
      all_systems = all_systems_response.json()
      all_system_details = []
      for system in all_systems:
        system_detail_response = my_api_helper.get_single_system(system['id'])
        try: 
          assert system_detail_response.status_code == 200
        except AssertionError as ae: 
          logger.error("Error in getting System Details %s" % system_detail_response.error)
        else:
          all_system_details.append(system_detail_response.json())
  
      print("Systems data downloaded")
      df = pd.read_json(json.dumps(all_system_details))
      logger.info("Writing Systems file to disk..")
      df.to_csv(Path.joinpath(project_directory, "systems.csv"))
      logger.info("Systems file written")
    else: 
      logger.error("Error in getting systems data from Geodesignhub: %s " % all_systems_response.text)
      

    # Get all Diagrams 
    all_diagrams_response = my_api_helper.get_all_diagrams()
    if all_diagrams_response.status_code==200:
      all_diagrams = all_diagrams_response.json()
      print("Diagrams data downloaded")
      df = pd.read_json(json.dumps(all_diagrams))

      logger.info("Writing diagrams to disk..")
      df.to_csv(Path.joinpath(project_directory,  "diagrams.csv"))
      logger.info("Diagrams file written")
    else: 
      logger.error("Error in getting systems data from Geodesignhub: %s " % all_systems_response.text)
      
    # Get all Design Teams
    all_design_team_response = my_api_helper.get_all_design_teams()
    if all_design_team_response.status_code == 200:
      all_design_teams = all_design_team_response.json()
      all_design_team_details = []
      for design_team in all_design_teams:
        design_team_detail_response = my_api_helper.get_single_design_team(design_team['id'])
        try: 
          assert design_team_detail_response.status_code == 200
        except AssertionError as ae: 
          logger.error("Error in getting Design Team Details %s" % design_team_detail_response.text)
        else:
          all_design_team_details.append(design_team_detail_response.json())
  
      print(" Design Team data downloaded")
      df = pd.read_json(json.dumps(all_design_team_details))
      logger.info("Writing  Design Team file to disk..")
      df.to_csv(Path.joinpath(project_directory, "design_teams.csv"))
      logger.info(" Design Team file written")
    else: 
      logger.error("Error in getting  Design Team data from Geodesignhub: %s " % all_systems_response.text)
      


    # Get all Syntehsis

    # Get all participants


