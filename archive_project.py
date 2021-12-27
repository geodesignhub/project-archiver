import requests, json, GeodesignHub
import os, sys
import shutil
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
      assert c.keys() ==set(['service_url', 'project_ids', 'api_token'])
    except AssertionError as ae: 
      logger.error("Error in config file parameters")
      sys.exit(1)
    
    project_ids = c['project_ids']
    for project_id in project_ids:

      my_api_helper = GeodesignHub.GeodesignHubClient(url = c['service_url'], project_id= c['project_id'], token=c['api_token'])
      # make project folder
      project_directory = Path("output", c['project_id'])
      project_directory.mkdir(parents=True, exist_ok=True)

      zip_file_name = c['project_id']
      zip_file_directory = Path("output", zip_file_name)

      # Get all Systems
      all_projects_response = my_api_helper.get_project_id()
      if all_projects_response.status_code == 200:
        all_project_details = all_projects_response.json()
        
        print("Project data downloaded")
        df = pd.read_json(json.dumps(all_project_details), typ='series')
        logger.info("Writing Project data file to disk..")
        df.to_csv(Path.joinpath(project_directory, "project.csv"))
        logger.info("Project data file written")
      else: 
        logger.error("Error in getting systems data from Geodesignhub: %s " % all_projects_response.text)
      
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
      all_design_team_details = []
      all_design_team_response = my_api_helper.get_all_design_teams()
      if all_design_team_response.status_code == 200:
        all_design_teams = all_design_team_response.json()
        all_design_team_details = []
        for design_team in all_design_teams:
          design_team_detail_response = my_api_helper.get_all_details_for_design_team(design_team['id'])
          try: 
            assert design_team_detail_response.status_code == 200
          except AssertionError as ae: 
            logger.error("Error in getting Design Team Details %s" % design_team_detail_response.text)
          else:
            all_design_team_details.append(design_team_detail_response.json())
    
        print("Design Team data downloaded")
        df = pd.read_json(json.dumps(all_design_team_details))
        logger.info("Writing  Design Team file to disk..")
        df.to_csv(Path.joinpath(project_directory, "design_teams.csv"))
        logger.info(" Design Team file written")
      else: 
        logger.error("Error in getting  Design Team data from Geodesignhub: %s " % all_design_team_response.text)
      
      # Get all Synthesis and diagrams
      all_design_syntheses_and_diagrams = []
      for current_team_synthesis in all_design_team_details:
        all_current_team_details = current_team_synthesis['synthesis']
        
        for current_team_details in all_current_team_details:        
          current_team_id = int(current_team_details['cteamid'])
          synthesis_id = current_team_details['id']
          synthesis_name = current_team_details['description']
          synthesis_digrams_response = my_api_helper.get_single_synthesis_diagrams(teamid = current_team_id, synthesisid = synthesis_id)
          try: 
            assert synthesis_digrams_response.status_code == 200
          except AssertionError as ae: 
            logger.error("Error in getting Diagram Details %s" % synthesis_digrams_response.text)
          else:
            synthesis_and_diagrams = synthesis_digrams_response.json()
            synthesis_and_diagrams['description'] = synthesis_name
            all_design_syntheses_and_diagrams.append(synthesis_and_diagrams)

      df = pd.read_json(json.dumps(all_design_syntheses_and_diagrams))
      logger.info("Writing  Design Team data file to disk..")
      
      df.to_csv(Path.joinpath(project_directory, "design_syntheses.csv"))
      logger.info("Design Team file written")
      print("Design Team and diagrams written")

      shutil.make_archive(Path('output', zip_file_name), 'zip', zip_file_directory)
      shutil.rmtree(project_directory)