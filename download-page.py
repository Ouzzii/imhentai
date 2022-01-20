from bs4 import BeautifulSoup as bs
from requests import get
from json import dumps,dump,load,loads
from shutil import copyfile
from os import mkdir
from os.path import exists

#download by id
id = input("id:")
id = "https://imhentai.xxx/gallery/630010"
#id = "https://imhentai.xxx/gallery/344375"
if id.startswith("www") or id.startswith("http"):
	print("")
else:
	id = f"https://www.imhentai.xxx/gallery/{id}"

index = bs(get(id).text,"html.parser")
#print(index)


tags = index.find_all("a",{"class":"tag btn btn-primary"})
tagList,artistList,groupList,languageList,categoryList,parodyList,characterList=[],[],[],[],"",[],[]

imageSource = index.find("div",{"class":"col-md-4 col left_cover"}).find("img")["data-src"]
pages = []
for i in range (0,int(index.find("li",{"class":"pages"}).text.split(" ")[-1])):
	pages.append(str(i+1).join(imageSource.split("cover")))

for Tag in tags:
	tag = Tag["href"].split("/")[-2]
	if "/tag" in Tag["href"]:
		tagList.append(tag)
	if "/character" in Tag["href"]:
		characterList.append(tag)
	if "/parody" in Tag["href"]:
		parodyList.append(tag)
	if "/artist" in Tag["href"]:
		artistList.append(tag)
	if "/group" in Tag["href"]:
		groupList.append(tag)
	if "/language" in Tag["href"]:
		languageList.append(tag)
	
		

pageName = {"Page-Name":index.find("h1").text}
pageUrl = {"Page-Url":id}
pageId = {"Page-Id":int(id.split("/")[-1])}
pageCount = {"Page":int(index.find("li",{"class":"pages"}).text.split(" ")[-1])}
assetTags = {"tags":tagList}
assetCharacters = {"characters":characterList}
assetParodies = {"parodies":parodyList}
assetArtists = {"artists":artistList}
assetGroups = {"groups":groupList}
assetLanguages = {"languages":languageList}
assetCategory = {"categories":categoryList}
assetPages = {"Page-Sources":pages}
assetList = [pageName,pageUrl,pageId,pageCount,assetTags,assetCharacters,assetParodies,assetArtists,assetGroups,assetLanguages,assetCategory,assetPages]

	
		
			
				
		
if index.find("a",{"class":"tag btn btn-primary doujinshi"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary doujinshi"}).text[0:9]})
elif index.find("a",{"class":"tag btn btn-primary imageset"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary imageset"}).text[0:9]})
elif index.find("a",{"class":"tag btn btn-primary artistcg"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary artistcg"}).text[0:9]})
elif index.find("a",{"class":"tag btn btn-primary gamecg"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary gamecg"}).text[0:7]})
elif index.find("a",{"class":"tag btn btn-primary western"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary western"}).text[0:7]})
elif index.find("a",{"class":"tag btn btn-primary manga"}) != None:
	assetCategory.update({"categories":index.find("a",{"class":"tag btn btn-primary manga"}).text[0:5]})
			
if len(tagList) == 0:
	assetTags.update({"tags":None})
if len(parodyList) == 0:
	assetParodies.update({"parodies":None})
if len(artistList) == 0:
	assetArtists.update({"artists":None})
if len(groupList) == 0:
	assetGroups.update({"groups":None})
if len(languageList) == 0:
	assetLanguages.update({"languages":None})
if assetCategory["categories"] == "":
	assetCategory.update({"categories":None})
if len(characterList) == 0:
	assetCharacters.update({"characters":None})
			

jsonFinnaly = {str(pageId["Page-Id"]):{}}
for i in assetList:
	jsonFinnaly[str(pageId["Page-Id"])].update(i)
	print(i)


readjfile = open("mainHentaidb.json","r")
jsonFile = load(readjfile)
readjfile.close()
writejfile = open("mainHentaidb.json","w")
jsonFile.update(jsonFinnaly)
dump(jsonFile, writejfile,indent=4)
writejfile.close()

#copyfile("mainHentaidb.json","hentais(backup).json")

print("===========================================================")

if exists("images") == True:
	pass
else:
	mkdir("images")
if exists(f"./images/{pageName['Page-Name']}|{pageId['Page-Id']}") == True:
	pass
else:
	mkdir(f"./images/{pageName['Page-Name']}|{pageId['Page-Id']}")
for i in pages:
	a = open("./images/"+pageName['Page-Name']+"|"+str(pageId["Page-Id"])+'/'+i.split("/")[-1],"wb")
	print(i)
	a.write(get(i).content)
	a.close()