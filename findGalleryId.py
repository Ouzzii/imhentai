from json import load

gallery_id = input("id:")

readFile = open("mainHentaidb.json")
jsonFile = load(readFile)
readFile.close()

for i in jsonFile.keys():
	print(jsonFile[i]["Page-Name"])
#	if i == str(gallery_id):
#		print(i)