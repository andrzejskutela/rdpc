import os
import re

class Downloader:
	working_dir: str

	def __init__(self, working_dir: str):
		self.working_dir = working_dir

	def get(self, project: str, download: str):
		if not self.project_is_valid(project):
			if self.project_path_is_valid(project):
				self.create_empty_project(project)
			else:
				raise Exception(f"Path ")

		self.add_file_to_project(project, download)

	def create_empty_project(self, project: str):
		os.makedirs(self.path_join([project, "import_files"]), exist_ok=True)
		with open(self.path_join([project, "import_files", ".gitignore"]), "w") as file:
			file.write("""\
*
!.gitignore
""")

	def add_file_to_project(self, project: str, download: str):
		with open(self.path_join([project, "import_list.txt"]), "a") as file:
			file.write(download + "\n")

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
