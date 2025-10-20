import requests, json, GeodesignHub
import os, sys
import shutil
import pandas as pd
import logging
import logging.handlers
from json.decoder import JSONDecodeError
from pathlib import Path
from io import StringIO
import uuid


class ScriptLogger:
    def __init__(self):
        self.log_file_name = "logs/latest.log"
        self.path = os.getcwd()
        self.logpath = os.path.join(self.path, "logs")
        self.outputpath = os.path.join(self.path, "output")
        if not os.path.exists(self.logpath):
            os.mkdir(self.logpath)
        if not os.path.exists(self.outputpath):
            os.mkdir(self.outputpath)
        self.logging_level = logging.INFO
        # set TimedRotatingFileHandler for root
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
        self.handler = logging.handlers.TimedRotatingFileHandler(
            self.log_file_name, when="S", interval=30, backupCount=10
        )
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger()  # or pass string to give it a name
        self.logger.addHandler(self.handler)
        self.logger.setLevel(self.logging_level)

    def get_logger(self):
        return self.logger


def load_and_validate_config(logger):
    logger.info("Attempting to read configuration file: config.json")
    try:
        with open("config.json") as config:
            c = json.load(config)
        logger.info("Configuration file loaded successfully")
    except JSONDecodeError as je:
        logger.error(f"Error decoding JSON from config file: {je}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        sys.exit(1)

    logger.info("Validating configuration file parameters")
    try:
        assert c.keys() == set(["service_url", "project_ids", "api_token"])
        logger.info("Configuration file parameters validated successfully")
    except AssertionError as ae:
        logger.error("Error in config file parameters")
        sys.exit(1)

    return c


def fetch_and_save_project_details(my_api_helper, project_directory, logger):
    all_projects_response = my_api_helper.get_project_details()
    if all_projects_response.status_code == 200:
        all_project_details = all_projects_response.json()
        logger.info("Project data downloaded")
        all_projects_df = pd.DataFrame([all_project_details])
        
        
        logger.info("Writing Project data file to disk..")
        all_projects_df.to_csv(Path.joinpath(project_directory, "project.csv"))
        all_projects_df.name = "Project Details"
        logger.info("Project data file written")
    else:
        logger.error(
            "Error in getting project data from Geodesignhub: %s"
            % all_projects_response.text
        )


def fetch_and_save_systems(my_api_helper, project_directory, logger):
    all_systems_response = my_api_helper.get_all_systems()
    if all_systems_response.status_code == 200:
        all_systems = all_systems_response.json()
        all_system_details = []
        for system in all_systems:
            system_detail_response = my_api_helper.get_single_system(system["id"])
            if system_detail_response.status_code != 200:
                logger.error(
                    "Error in getting System Details %s" % system_detail_response.text
                )
                continue
            all_system_details.append(system_detail_response.json())

        logger.info("Systems data downloaded")
        all_systems_df = pd.read_json(StringIO(json.dumps(all_system_details)))
        all_systems_df["Global_ID"] = [
            str(uuid.uuid4()) for _ in range(len(all_systems_df))
        ]
        all_systems_df.name = "Systems"
        logger.info("Writing Systems file to disk..")
        all_systems_df.to_csv(Path.joinpath(project_directory, "systems.csv"))
        logger.info("Systems file written")
    else:
        logger.error(
            "Error in getting systems data from Geodesignhub: %s"
            % all_systems_response.text
        )


def fetch_and_save_diagrams(my_api_helper, project_directory, logger):
    all_diagrams_response = my_api_helper.get_all_diagrams()
    if all_diagrams_response.status_code == 200:
        all_diagrams = all_diagrams_response.json()
        logger.info("Diagrams data downloaded")
        all_diagrams_df = pd.read_json(StringIO(json.dumps(all_diagrams)))
        all_diagrams_df["Global_ID"] = [
            str(uuid.uuid4()) for _ in range(len(all_diagrams_df))
        ]
        all_diagrams_df.name = "Diagrams"
        logger.info("Writing diagrams to disk..")
        all_diagrams_df.to_csv(Path.joinpath(project_directory, "diagrams.csv"))
        logger.info("Diagrams file written")
    else:
        logger.error(
            "Error in getting diagrams data from Geodesignhub: %s"
            % all_diagrams_response.text
        )


def fetch_and_save_design_teams(my_api_helper, project_directory, logger):
    all_design_team_details = []
    all_design_team_response = my_api_helper.get_all_design_teams()
    if all_design_team_response.status_code == 200:
        all_design_teams = all_design_team_response.json()
        for design_team in all_design_teams:
            design_team_detail_response = my_api_helper.get_all_details_for_design_team(
                design_team["id"]
            )
            if design_team_detail_response.status_code != 200:
                logger.error(
                    "Error in getting Design Team Details %s"
                    % design_team_detail_response.text
                )
                continue
            all_design_team_details.append(design_team_detail_response.json())
        flattened_details = []
        for team in all_design_team_details:
            for synth in team.get('synthesis', []):
                flattened_details.append(synth)
        all_design_team_details = flattened_details
        logger.info("Design Team data downloaded")
        all_design_teams_df = pd.read_json(
            StringIO(json.dumps(all_design_team_details))
        )
        all_design_teams_df.name = "Design Teams"
        logger.info("Writing Design Team file to disk..")
        all_design_teams_df.to_csv(Path.joinpath(project_directory, "design_teams.csv"))
        logger.info("Design Team file written")
    else:
        logger.error(
            "Error in getting Design Team data from Geodesignhub: %s"
            % all_design_team_response.text
        )
    return all_design_team_details


def fetch_and_save_syntheses(
    my_api_helper,
    project_directory,
    logger,
    all_design_team_details,
):
    all_design_syntheses_and_diagrams = []
    for current_team_synthesis in all_design_team_details:
        
        current_team_id = int(current_team_synthesis["cteamid"])
        synthesis_id = current_team_synthesis["id"]
        synthesis_name = current_team_synthesis["description"]
        synthesis_digrams_response = my_api_helper.get_single_synthesis_diagrams(
            teamid=current_team_id, synthesisid=synthesis_id
        )
        if synthesis_digrams_response.status_code != 200:
            logger.error(
                "Error in getting Diagram Details %s"
                % synthesis_digrams_response.text
            )
            continue
        synthesis_and_diagrams = synthesis_digrams_response.json()
        synthesis_and_diagrams['diagrams'] = ",".join(
            [str(diagram) for diagram in synthesis_and_diagrams['diagrams']]
        )
        synthesis_and_diagrams["description"] = synthesis_name
        all_design_syntheses_and_diagrams.append(synthesis_and_diagrams)
    
    design_synthesis_details_df = pd.read_json(
        StringIO(json.dumps(all_design_syntheses_and_diagrams))
    )
    logger.info("Writing Design Synthesis data file to disk..")
    design_synthesis_details_df["Global_ID"] = [
        str(uuid.uuid4()) for _ in range(len(design_synthesis_details_df))
    ]
    design_synthesis_details_df.name = "Design Syntheses"

    design_synthesis_details_df.to_csv(
        Path.joinpath(project_directory, "design_syntheses.csv")
    )
    logger.info("Design Synthesis file written")


def fetch_and_save_negotiation_logs(my_api_helper, project_directory, logger):
    negotiation_logs_response = my_api_helper.get_project_negotiation_logs()
    if negotiation_logs_response.status_code == 200:
        all_negotiation_logs = negotiation_logs_response.json()
        logger.info("Negotiation Logs data downloaded")
        negotiation_logs_df = pd.read_json(
            StringIO(json.dumps(all_negotiation_logs["all_negotiations"]))
        )
        negotiation_logs_df.name = "Negotiation Logs"

        for index, log in negotiation_logs_df.iterrows():
            log_file_name = f"negotiation_log_{log['session_id']}.csv"
            moves = log.get('moves', [])
            moves_list = []
            for move in moves:
                moves_list.append({
                    'diagram': move['diagram'],
                    'move': move['move'],
                    'timestamp': move['timestamp']
                })
            log_df = pd.DataFrame(moves_list)
            log_df.to_csv(Path.joinpath(project_directory, log_file_name), index=False)

        logger.info("Writing Negotiation Logs file to disk..")
        negotiation_logs_df = negotiation_logs_df.drop(columns=['moves'])
        negotiation_logs_df.to_csv(
            Path.joinpath(project_directory, "negotiation_logs.csv")
        )
        logger.info("Negotiation Logs file written")
    else:
        logger.error(
            "Error in getting Negotiation Logs data from Geodesignhub: %s"
            % negotiation_logs_response.text
        )


def process_project(project_id, c, logger):

    my_api_helper = GeodesignHub.GeodesignHubClient(
        url=c["service_url"], project_id=project_id, token=c["api_token"]
    )
    # make output directory if it doesn't exist
    output_directory = Path("output")
    output_directory.mkdir(parents=True, exist_ok=True)

    # make project folder
    project_directory = output_directory / project_id
    project_directory.mkdir(parents=True, exist_ok=True)

    zip_file_name = project_id
    zip_file_directory = output_directory / zip_file_name

    fetch_and_save_project_details(my_api_helper, project_directory, logger)
    fetch_and_save_systems(my_api_helper, project_directory, logger)
    fetch_and_save_diagrams(my_api_helper, project_directory, logger)
    all_design_team_details = fetch_and_save_design_teams(
        my_api_helper, project_directory, logger
    )
    fetch_and_save_syntheses(
        my_api_helper,
        project_directory,
        logger,
        all_design_team_details,
    )
    fetch_and_save_negotiation_logs(my_api_helper, project_directory, logger)

    # Combine all the csv files as a single Excel workbook with multiple sheets
    with pd.ExcelWriter(
        Path.joinpath(project_directory, f"{project_id}_data.xlsx"),
        engine="openpyxl",
    ) as writer:
        for csv_file in project_directory.glob("*.csv"):
            df = pd.read_csv(csv_file)
            sheet_name = csv_file.stem
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    shutil.make_archive(
        str(Path("output", zip_file_name)), "zip", str(zip_file_directory)
    )
    shutil.rmtree(project_directory)


if __name__ == "__main__":
    myLogger = ScriptLogger()
    logger = myLogger.get_logger()
    session = requests.Session()
    logger.info("Starting job")

    c = load_and_validate_config(logger)
    project_ids = c["project_ids"]
    for project_id in project_ids:
        process_project(project_id, c, logger)
