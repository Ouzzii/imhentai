#find specific tag
from json import loads

specificTag = input("for tags use ,  not space!!\ntag:").split(",")

fileRead = open("mainHentaidb.json")
fileJson = loads(fileRead.read())
fileRead.close()

tags = []
tags2 = []
names = []
id = []
for keys in fileJson.keys():
	if fileJson[keys]["tags"] != None:
		tags.append(fileJson[keys]["tags"])
		names.append(fileJson[keys]["Page-Name"])
		id.append(fileJson[keys]["Page-Id"])



for i in tags:
    for a in range(len(specificTag)):
        if specificTag[a] in i:
            tags2.append(i)
            break
for i in tags:
	for a in range(len(specificTag)):
		try:
			if not specificTag[a] in i:
 	    		   tags2.remove(i)
		except:
			pass
for i in tags2:
	print(i)
