#by advanced search

from os import system
from os.path import exists
from json import dumps,load,dump,loads
from requests import get
from bs4 import BeautifulSoup as bs
from shutil import copyfile

#https://imhentai.xxx/search/?key=yaoi%2Cfurry&apply=Search&lt=1&pp=0&dl=0&tr=0&m=1&d=0&w=1&i=0&a=0&g=0&en=1&jp=0&es=0&fr=0&kr=0&de=0&ru=0

searchTags = "%2C".join(input("tags:").split(","))
langEn = str(input("English 0 or 1:"))
langJp = str(input("Japanese 0 or 1:"))
langEs = str(input("Spainsh 0 or 1:"))
langFr = str(input("French 0 or 1:"))
langKr = str(input("Korean 0 or 1:"))
langDe = str(input("Deutsch 0 or 1:"))
langRu = str(input("Russian 0 or 1:"))

urlStructure = "https://imhentai.xxx/search/?key="+searchTags+ f"&apply=Search&lt=0&pp=0&dl=0&tr=0&m=1&d=1&w=1&i=1&a=1&g=1&en={langEn}&jp={langJp}&es={langEs}&fr={langFr}&kr={langKr}&de={langDe}&ru={langRu}"
print(urlStructure)

mainPage = get(urlStructure).text
mainPage = bs(mainPage,"html.parser").find_all("div",{"class":"inner_thumb"})
for i in mainPage:
	targetPage = "https://www.imhentai.xxx"+i.find("a")["href"]
	print(targetPage)
	targetPageName = "".join(i.find("img")["alt"].title().split(" "))
	galleryId = targetPage.split("/")[-2]
	
	targetPageIndex = get(targetPage).text
	targetPageIndex = bs(targetPageIndex,"html.parser")
	
	fullName = targetPageIndex.find("img",{"class":"lazy"})["alt"]
	tags = targetPageIndex.find_all("a",{"class":"tag btn btn-primary"})
	pageCount = int(targetPageIndex.find("li",{"class":"pages"}).text.split(" ")[-1])
	imageSource = targetPageIndex.find("div",{"class":"col-md-4 col left_cover"}).find("img")["data-src"]
	pages = [imageSource]
	for i in range (0,pageCount):
		pages.append(str(i+1).join(imageSource.split("cover")))
	#print(pages)
	tagList,artistList,groupList,languageList,categoryList,parodyList,characterList=[],[],[],[],"",[],[]
	
	for Tag in tags:
		tag = Tag["href"].split("/")[-2]
		if "/tag" in Tag["href"]:
			tagList.append(tag)
			#assetTags.update({"tags":tagList})
		if "/character" in Tag["href"]:
			characterList.append(tag)
		if "/parody" in Tag["href"]:
			parodyList.append(tag)
			#assetParodies.update("parodies":parodyList)
		if "/artist" in Tag["href"]:
			artistList.append(tag)
			#assetArtists.update({"artists":artistList})
		if "/group" in Tag["href"]:
			groupList.append(tag)
			#assetGroups.update({"groups":groupList})
		if "/language" in Tag["href"]:
			languageList.append(tag)
			#assetLanguages.update({"languages":languageList})
	
	pageName = {"Page-Name":fullName}
	pageUrl = {"Page-Url":targetPage}
	pageId = {"Page-Id":int(targetPage.split("/")[-2])}
	pageCount = {"Page":pageCount}
	assetTags = {"tags":tagList}
	assetCharacters = {"characters":characterList}
	assetParodies = {"parodies":parodyList}
	assetArtists = {"artists":artistList}
	assetGroups = {"groups":groupList}
	assetLanguages = {"languages":languageList}
	assetCategory = {"categories":categoryList}
	assetPages = {"Page-Sources":pages}
	assetList = [pageName,pageUrl,pageId,pageCount,assetTags,assetCharacters,assetParodies,assetArtists,assetGroups,assetLanguages,assetCategory,assetPages]
	
	

	if targetPageIndex.find("a",{"class":"tag btn btn-primary doujinshi"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary doujinshi"}).text[0:9]})
	elif targetPageIndex.find("a",{"class":"tag btn btn-primary imageset"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary imageset"}).text[0:9]})
	elif targetPageIndex.find("a",{"class":"tag btn btn-primary artistcg"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary artistcg"}).text[0:9]})
	elif targetPageIndex.find("a",{"class":"tag btn btn-primary gamecg"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary gamecg"}).text[0:7]})
	elif targetPageIndex.find("a",{"class":"tag btn btn-primary western"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary western"}).text[0:7]})
	elif targetPageIndex.find("a",{"class":"tag btn btn-primary manga"}) != None:
		assetCategory.update({"categories":targetPageIndex.find("a",{"class":"tag btn btn-primary manga"}).text[0:5]})
			
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
			

	jsonFinnaly = {str(galleryId):{}}
	for i in assetList:
		jsonFinnaly[str(galleryId)].update(i)
	print(assetList[0])
	print(assetList[4])	

	readjfile = open("mainHentaidb.json","r")
	jsonFile = load(readjfile)
	readjfile.close()
	writejfile = open("mainHentaidb.json","w")
	jsonFile.update(jsonFinnaly)
	dump(jsonFile, writejfile,indent=4)
	writejfile.close()
	
	#f = open("mainHentaidb.json","r")
	#after = len(f.read())
	#f.close
	#copyfile("mainHentaidb.json","hentais(backup).json")
		
	#if before == after or before != after:

	print("=========================================================================")
	
	
	
	
	
"""
tags:bbw,futanari,big-breasts
https://www.imhentai.xxx/gallery/392789/
https://www.imhentai.xxx/gallery/774479/
https://www.imhentai.xxx/gallery/777320/
https://www.imhentai.xxx/gallery/465135/
https://www.imhentai.xxx/gallery/779431/
https://www.imhentai.xxx/gallery/786322/
https://www.imhentai.xxx/gallery/784901/
https://www.imhentai.xxx/gallery/698780/
https://www.imhentai.xxx/gallery/760902/
https://www.imhentai.xxx/gallery/741977/
https://www.imhentai.xxx/gallery/778837/
https://www.imhentai.xxx/gallery/594941/
https://www.imhentai.xxx/gallery/707184/
https://www.imhentai.xxx/gallery/633287/
https://www.imhentai.xxx/gallery/601463/
https://www.imhentai.xxx/gallery/783137/
https://www.imhentai.xxx/gallery/468400/
https://www.imhentai.xxx/gallery/255396/
https://www.imhentai.xxx/gallery/520747/
https://www.imhentai.xxx/gallery/787400/


"""