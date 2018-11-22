import json


j = '''
{
	"amqp": {
		"host": "",
		"port": 11,
		"user": "",
		"password": "",
		"exchange": "",
		"vhost": ""
	},

	"rss": {
		"id": "",
		"tite": "",
		"hello": "",
		"port": 49
	}
}'''


pattern = {
	"amqp": {
		"host": str,
		"port": int,
		"user": str,
		"password": str,
		"exchange": str,
		"vhost": str
	},

	"rss": {
		"id": str,
		"tite": str,
		"hello": str,
		"port": int,
	}
}

class JsonValidator:
	def __init__(self, json_data, json_mapping):
		self.json    = json_data
		self.mapping = json_mapping
		self.__json  = json.loads(self.json)

		if not self.check_mapping():
			raise Exception()

	def check_mapping(self):
		return self._check_mapping(self.mapping)
	
	def _check_mapping(self, mapping):
		t = True

		for key in mapping:
			if t == False:
				return False

			if type(mapping[key]) == dict:
				t = self._check_mapping(mapping[key])

			elif type(mapping[key]) == list:
				if len(mapping[key]) == 1:
					t = self._check_mapping({ key: mapping[key][0]})
				else:
					t = False

			elif self.check_type(mapping[key]):
				pass
			else:
				return False

		return (t and True)



	def check_type(self, t):
		return t == int or t == float or t == str

	def validate(self):
		return self._validate(self.__json, self.mapping)

	def _validate(self, j, mapping):
		t = True
		for key in j:
			if t == False:
				return False

			if type(j[key]) == list:
				if len(j[key]) > 0:
					for e in j[key]:
						if t == False:
							return False
						try:
							t = self._validate(e, mapping[key][0])
						except Exception as ex:
							t = False


			elif type(j[key]) == dict:
				t = self._validate(j[key], mapping[key])

			elif self.check_type(type(j[key])):
				if type(j[key]) != mapping[key]:
					return False

			else:
				return False

		return (t and True)

	
a = JsonValidator(j, pattern)
t = a.check_mapping()

print()
print("mapping is correct ? {}".format(t))

t = a.validate()
print()
print("JSON is correct ? {}".format(t))
