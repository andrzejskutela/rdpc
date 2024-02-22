class DataModule:
	allowed_methods: list

	def execute(self, method: str, argv: list):
		if method in self.allowed_methods:
			method = getattr(self, method)
			method(*argv)
		else:
			raise Exception(f"Method {method!r} is not allowed in module {self.__class__.__name__!r}")

	def list(self):
		print(self.allowed_methods)

	def registerAllowedMethods(self, methods: list):
		self.allowed_methods = ['list'] + methods
