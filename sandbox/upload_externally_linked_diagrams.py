import requests
import json
import GeodesignHub
import os
import sys
import pandas as pd

import logging
import logging.handlers
from json.decoder import JSONDecodeError
from pathlib import Path


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

    def getLogger(self):
        return self.logger


if __name__ == "__main__":

    myLogger = ScriptLogger()
    logger = myLogger.getLogger()
    session = requests.Session()
    logger.info("Starting job..")

    try:
        with open("config.json") as config:
            c = json.load(config)
    except JSONDecodeError:
        print("Error reading config file..")
        logger.info("Error reading config file..")
        sys.exit(1)

    try:
        assert c.keys() == set(["service_url", "project_ids", "api_token"])
    except AssertionError:
        logger.error("Error in config file parameters..")
        sys.exit(1)

    project_ids = c["project_ids"]
    for project_id in project_ids:
        my_api_helper = GeodesignHub.GeodesignHubClient(
            url=c["service_url"], project_id=project_id, token=c["api_token"]
        )
        df = pd.read_csv("upload_data/ext_diagrams.csv")

        for index, row in df.iterrows():
            description = row["description"]
            feature_type = row["feature_type"]
            funding_type = row["funding_type"]
            flat_geobuf_url = row["flat_geobuf_url"]
            project_or_policy = row["project_or_policy"]
            system_id = row["system_id"]

            # print(description, feature_type, funding_type, flat_geobuf_url, project_or_policy)
            response = my_api_helper.post_as_diagram_with_external_geometries(
                url=flat_geobuf_url,
                layer_type="fgb-layer",
                projectorpolicy=project_or_policy,
                featuretype=feature_type,
                description=description,
                fundingtype=funding_type,
                sysid=system_id,
            )
            print(response.json())
