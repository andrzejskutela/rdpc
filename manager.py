#!//usr/bin/python3.12

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

	method = getattr(handler, sys.argv[2])
	method(*sys.argv[3:])
except Exception as e:
	how_to_use_info()
	print(e)

