from os import system
from os.path import exists
#system("pip install bs4")
#system("pip install requests")
from json import dumps,load,dump,loads
from requests import get
from bs4 import BeautifulSoup as bs
from shutil import copyfile
from random import choices

#gallery_page
if exists("mainHentaidb.json") == False:
	with open("mainHentaidb.json","w")as f:
		f.write("{}")
else:
	galleriIds = open("mainHentaidb.json","r")
	galleriIdsj = loads(galleriIds.read())
	galleriIds.close()
count = "1234567890"
readi = open("mainHentaidb.json")
reado = readi.read()
readi.close()
lastestPage = int(bs(get("https://www.imhentai.xxx").text,"html.parser").find("div",{"class":"inner_thumb"}).find("a")["href"].split("/")[-2])
while True:
	galleriIds = open("mainHentaidb.json","r")
	galleriIdsj = loads(galleriIds.read())
	galleriIds.close()

	gallery_id = int("".join(choices(list(count),k= int("".join(choices(list("123456"),k=1 )  )  )     )   )  )
	targetPage = "https://www.imhentai.xxx/gallery/"+str(gallery_id)
	#if targetPage in reado or gallery_id > 787531:
	if gallery_id > lastestPage or str(gallery_id) in list(galleriIdsj.keys()):
		print(f"{targetPage}\n///////////////////PASSED///////////////////")
		print("===========================================================")
	else:
		ir = get(targetPage).text
		i = bs(ir,"html.parser")
		print(targetPage)
		galleryId = targetPage.split("/")[-2]
		#print(targetPage,targetPageName,galleryId)
		
		targetPageIndex = get(targetPage).text
		targetPageIndex = bs(targetPageIndex,"html.parser")
		
		fullName = targetPageIndex.find("h1").text
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
		pageId = {"Page-Id":int(gallery_id)}
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
			#print(i)
		print(pageId)

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
		copyfile("mainHentaidb.json","hentais(backup).json")
		
		#if before == after or before != after:

		print("===========================================================")
		