from os import system
from os.path import exists
from json import dumps,load,dump,loads
from requests import get
from bs4 import BeautifulSoup as bs
from shutil import copyfile
#basic


response = get("https://m3.imhentai.xxx/010/ys9uka7zin/1.jpg")

file = open("./images/[[Magnetus]Twitter-630010/sample_image.png", "wb")

file.write(response.content)

file.close()

print("x")


f = open("mainHentaidb.json","r")
Keys = list(load(f).keys())
f.close()
#print(Keys)


#advanced
count = 0
fullUrl = "https://imhentai.xxx/?page=1"
mainPage = get(fullUrl).text
#lastestPage = bs(mainPage,"html.parser").find_all("a",{"class":"page-link"})
#print(lastestPage)
#lastestPage = int(list(bs(mainPage,"html.parser").find_all("a",{"class":"page-link"}))[-2].text)



while True:
	count+=1
	fullUrl = "https://imhentai.xxx/?page="+str(count)
	print(fullUrl)
	
	mainPage = get(fullUrl).text
	#print(mainPage)
	mainPage = bs(mainPage,"html.parser").find_all("div",{"class":"inner_thumb"})
	#print(mainPage)
	for i in mainPage:
		targetPage = "https://www.imhentai.xxx"+i.find("a")["href"]
		#targetPage = "https://imhentai.xxx/gallery/736976/"
		#targetPageName = "".join(i.find("img")["alt"].title().split(" "))
		
		galleryId = targetPage.split("/")[-2]
		#print(targetPage,targetPageName,galleryId)
		
		targetPageIndex = get(targetPage).text
		targetPageIndex = bs(targetPageIndex,"html.parser")

		
		fullName = targetPageIndex.find("h1").text
		print(fullName)
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
			
		if 1 == 1: #not str(galleryId) in Keys:
			jsonFinnaly = {str(galleryId):{}}
			for i in assetList:
				jsonFinnaly[str(galleryId)].update(i)
				print(i)
			

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
		else:
			print(f"this asset already in json file:{galleryId}")
		#if before == after or before != after:

		print("===========================================================")
