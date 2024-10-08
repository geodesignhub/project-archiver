import requests
import json

# Version: 1.3.7


class GeodesignHubClient:
    """
    This a a Python client that make calls to the Geodesignhub API
    and return data. It requires the requests package and the json module.

    """

    def __init__(self, token: str, url: str = None, project_id: str = None):
        """
        Declare your project id, token and the url (optional).
        """
        self.project_id = project_id
        self.token = token
        self.sec_url = url if url else "https://www.geodesignhub.com/api/v1/"
        self.session = requests.Session()

    def get_project_id(self):
        """This method gets all systems for a particular project."""
        sec_url = self.sec_url + "projects" + "/" + self.project_id + "/"
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_all_systems(self):
        """This method gets all systems for a particular project."""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "systems" + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_project_center(self):
        """This method gets the center as lat,lng for a particular project."""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "center" + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_single_system(self, system_id: int):
        """This method gets details  a single system for a particular project."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(system_id)
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_constraints(self):
        """This method gets the geometry of constraints for a project if available"""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "constraints"
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_first_boundaries(self):
        """Gets the first boundaries if defined for a project"""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "boundaries" + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_second_boundaries(self):
        """Gets the second boundaries if defined for a project."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "secondboundaries"
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_project_bounds(self):
        """Returns a string with bounding box for the project study area coordinates in a 'southwest_lng,southwest_lat,northeast_lng,northeast_lat' format."""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "bounds" + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_project_tags(self):
        """Returns a list of tags created in the project."""
        sec_url = self.sec_url + "projects" + "/" + self.project_id + "/" + "tags" + "/"
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_all_design_teams(self):
        """Return all the change teams for that project."""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "cteams" + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_single_synthesis(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        assert len(synthesisid) == 16, "Synthesis : %s" % synthesisid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_single_synthesis_details(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        assert len(synthesisid) == 16, "Synthesis : %s" % synthesisid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/details/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_single_synthesis_esri_json(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        assert len(synthesisid) == 16, "Synthesis : %s" % synthesisid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/esri/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_single_synthesis_diagrams(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/diagrams/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_synthesis_timeline(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/timeline/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_synthesis_diagrams(self, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/diagrams/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_design_team_members(self, teamid: int):
        """Return all the change teams for that project."""
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "cteams"
            + "/"
            + str(teamid)
            + "/"
            + "members"
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_synthesis_system_projects(self, sysid: int, teamid: int, synthesisid: str):
        assert isinstance(teamid, int), "Team id is not a integer: %r" % teamid
        assert isinstance(sysid, int), "System id is not a integer %r" % sysid
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/cteams/"
            + str(teamid)
            + "/"
            + str(synthesisid)
            + "/systems/"
            + str(sysid)
            + "/projects/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def post_as_diagram(
        self,
        geoms,
        projectorpolicy: str,
        featuretype: str,
        description: str,
        sysid: str,
        fundingtype: str,
    ):
        """Create a self.session object with correct headers and creds."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/"
            + "add"
            + "/"
            + projectorpolicy
            + "/"
        )
        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        postdata = {
            "geometry": geoms,
            "description": description,
            "featuretype": featuretype,
            "fundingtype": fundingtype,
        }
        r = self.session.post(sec_url, headers=headers, data=json.dumps(postdata))
        return r

    def post_as_diagram_with_external_geometries(
        self,
        url: str,
        layer_type: str,
        projectorpolicy: str,
        featuretype: str,
        description: str,
        sysid: str,
        fundingtype: str,
    ):
        """Create a self.session object with correct headers and creds."""
        securl = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/"
            + "add/external/"
            + projectorpolicy
            + "/"
        )

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        postdata = {
            "url": url,
            "description": description,
            "layer_type": layer_type,
            "featuretype": featuretype,
            "fundingtype": fundingtype,
        }

        r = self.session.post(securl, headers=headers, data=json.dumps(postdata))
        return r

    def get_single_diagram(self, diagid: int):
        """This method gets the geometry of a diagram given a digram id."""
        assert isinstance(diagid, int), "diagram id is not an integer: %r" % id
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "diagrams"
            + "/"
            + str(diagid)
            + "/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_all_diagrams(self):
        """This method gets the geometry of all diagrams in a project ."""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "diagrams/all/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def get_diagram_changeid(self, diagid: int):
        """Returns the a hash of the last modified date, can be used to see if a diagram has changed from the last time it was accessed."""
        assert isinstance(diagid, int), "diagram id is not an integer: %r" % id
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "diagrams"
            + "/"
            + str(diagid)
            + "/changeid/"
        )
        headers = {"Authorization": "Token " + self.token}
        r = self.session.get(sec_url, headers=headers)
        return r

    def post_as_ealuation_JSON(self, geoms, sysid: int, username: str = None):
        """Create a self.session object with correct headers and creds."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/e/map/json/"
        )
        if username:
            sec_url += username + "/"

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }

        r = self.session.post(sec_url, headers=headers, data=json.dumps(geoms))
        return r

    def add_project_tags(self, tag_ids):
        """Add tags to a project"""
        sec_url = self.sec_url + "projects" + "/" + self.project_id + "/" + "tags" + "/"
        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        r = self.session.post(sec_url, headers=headers, data=json.dumps(tag_ids))
        return r

    def get_project_plugins(self):
        """Get plugins for a project"""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "plugins" + "/"
        )

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        r = self.session.get(sec_url, headers=headers)
        return r

    def add_plugins_to_project(self, tag_ids):
        """Add tags to a project"""
        sec_url = (
            self.sec_url + "projects" + "/" + self.project_id + "/" + "plugins" + "/"
        )

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }

        r = self.session.post(sec_url, headers=headers, data=json.dumps(tag_ids))
        return r

    def post_as_impact_JSON(self, geoms, sysid: int, username: str = None):
        """Create a self.session object with correct headers and creds."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/i/map/json/"
        )
        if username:
            sec_url += username + "/"
        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        r = self.session.post(sec_url, headers=headers, data=json.dumps(geoms))
        return r

    def post_as_evaluation_GBF(self, geoms, sysid: int, username: str = None):
        """Create a self.session object with correct headers and creds."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/e/map/gbf/"
        )
        if username:
            sec_url += username + "/"
        headers = {"Authorization": "Token " + self.token}
        r = self.session.post(sec_url, headers=headers, files={"geoms.gbf": geoms})
        return r

    def post_gdservice_JSON(self, geometry, jobid: str):
        """Create a self.session object with correct headers and creds."""
        sec_url = self.sec_url + "gdservices/callback/"
        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        data = {"geometry": geometry, "jobid": jobid}
        r = self.session.post(sec_url, headers=headers, data=json.dumps(data))
        return r

    def post_as_impact_GBF(self, geoms, sysid: int, username: str = None):
        """Create a self.session object with correct headers and creds."""
        sec_url = (
            self.sec_url
            + "projects"
            + "/"
            + self.project_id
            + "/"
            + "systems"
            + "/"
            + str(sysid)
            + "/i/map/gbf/"
        )
        if username:
            sec_url += username + "/"
        headers = {"Authorization": "Token " + self.token}
        r = self.session.post(sec_url, headers=headers, files={"geoms.gbf": geoms})
        return r

    def create_new_project(self, project_create_payload):
        """Create a self.session object with correct headers and creds."""
        sec_url = self.sec_url + "projects/create/"

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        r = self.session.post(
            sec_url, headers=headers, data=json.dumps(project_create_payload)
        )
        return r

    def create_new_igc_project(self, project_create_payload):
        """Create a self.session object with correct headers and creds."""
        sec_url = self.sec_url + "projects/create-igc-project/"

        headers = {
            "Authorization": "Token " + self.token,
            "Content-Type": "application/json",
        }
        r = self.session.post(
            sec_url, headers=headers, data=json.dumps(project_create_payload)
        )
        return r
