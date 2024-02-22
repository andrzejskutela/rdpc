import os
import re
import requests
from .datamodule import DataModule

class Downloader(DataModule):
	working_dir: str
	
	def __init__(self, working_dir: str):
		self.working_dir = working_dir
		super().registerAllowedMethods(['get'])

	def get(self, project: str, download: str, save_as: str):
		if not self.project_is_valid(project):
			if self.project_path_is_valid(project):
				self.create_empty_project(project)
			else:
				raise Exception(f"Path ")

		self.add_file_to_project(project, download, save_as)

	def download_file(self, project: str, download: str):
		ret = {}
		with open(self.path_join([project, "download.tmp"]), "wb") as file:
			r = requests.get(download, stream=True)
			if r.status_code == requests.codes.ok:
				file.write(r.content)
				ret['size'] = len(r.content)
			else:
				r.raise_for_status()

		return ret

	def create_empty_project(self, project: str):
		os.makedirs(self.path_join([project, "import_files"]), exist_ok=True)
		with open(self.path_join([project, "import_files", ".gitignore"]), "w") as file:
			file.write("""\
*
!.gitignore
""")

	def add_file_to_project(self, project: str, download: str, save_as: str):
		if not re.search("^[a-z0-9_]{3,40}\\.[a-z]{1,5}$", save_as):
			raise Exception(f"Invalid save as value {save_as!r}")

		data = self.download_file(project, download)
		os.rename(self.path_join([project, "download.tmp"]), self.path_join([project, "import_files", save_as]))
		with open(self.path_join([project, "import_list.txt"]), "a") as file:
			file.write(f"{save_as} {data['size']} {download}\n")

	def project_path_is_valid(self, project: str):
		not_allowed = ["data_manager"]
		return re.search("^[a-z_]{3,}$", project) and not (project in not_allowed)

	def path_join(self, fragments: list):
		return os.path.join(self.working_dir, *fragments)

	def project_exists(self, project: str):
		return os.path.isdir(self.path_join([project]))

	def project_is_valid(self, project: str):
		if not self.project_exists(project):
			return False

		objects = [os.path.basename(f) for f in os.listdir(self.path_join([project]))]
		expected = ["import_files"]
		for expected_file in expected:
			if not expected in objects:
				return False

		return True
