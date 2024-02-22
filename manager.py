#!//usr/bin/python3.11

import os
import sys
import importlib, importlib.util

def how_to_use_info():
	print(f"{sys.argv[0]} module method [args]...\n")

handler = None
try:
	if len(sys.argv) > 2:
		import_name = "data_manager." + sys.argv[1]
		class_name = sys.argv[1].title()

		if (spec := importlib.util.find_spec(import_name)) is not None:
			imported = importlib.import_module(import_name)
			class_ = getattr(imported, class_name)
			handler = class_(os.getcwd())
		else:
			raise Exception(f"Can't find the {import_name!r} module")
	else:
		raise Exception("Not enough arguments given")

	handler.execute(sys.argv[2], sys.argv[3:])
except Exception as e:
	how_to_use_info()
	exc_type, exc_obj, traceback = sys.exc_info()
	fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
	print(f"{e} ({fname}:{traceback.tb_lineno})")

