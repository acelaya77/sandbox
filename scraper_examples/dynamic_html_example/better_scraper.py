import requests
import json
import os
import csv

#"url = 'https://api-gateway.boats.com/api-boattrader-client/app/search/boat?apikey=8b08b9bc353c494a80c60fb86debfc56&pageSize={self.page_size}&page={self.page}&country={self.country}&facets=country,state,make,makeModel,class,fuelType,hullMaterial,stateCity,priceRevisedSince,minMaxPercentilPrices,condition&fields=id,make,model,year,featureType,specifications.dimensions.lengths.nominal.ft,location.address.state,location.address.country,location.address.city,aliases,owner.logos.enhanced,owner.name,owner.rootName,price.hidden,price.type.amount.USD,price.discount.amount.USD,price.discount.revisedDate,portalLink,media.0.title,media.0.date.modified,media.0.mediaType,media.0.width,media.0.videoEmbedUrl,media.0.videoVideoThumbnailUri,media.0.url,attributes&useMultiFacetedFacets=true&distance={self.distance}mi&length={self.length_min}-{self.length_max}&uom=ft&sort=length-desc&multiFacetedBoatTypeClass=[%22sail%22]'

class Scrapper:
    def __init__(self,distance,page_size,page,country,length_min,length_max):
        self.distance = distance
        self.page_size = page_size
        self.page = page
        self.country = country
        self.length_min = length_min
        self.length_max = length_max
        self.headers = {
                "Accept":   "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Host":    "api-gateway.boats.com",
                "Upgrade-Insecure-Requests":	"1",
                "User-Agent":  "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
        }
    
    def set_url(self):
        #print("set_url")
        #url = f"https://api-gateway.boats.com/api-boattrader-client/app/search/boat?apikey=8b08b9bc353c494a80c60fb86debfc56&facets=country,state,make,makeModel,class,fuelType,hullMaterial,stateCity,priceRevisedSince,minMaxPercentilPrices,condition&fields=id,make,model,year,featureType,specifications.dimensions.lengths.nominal.ft,location.address.state,location.address.country,location.address.city,aliases,owner.logos.enhanced,owner.name,owner.rootName,price.hidden,price.type.amount.USD,price.discount.amount.USD,price.discount.revisedDate,portalLink,media.0.title,media.0.date.modified,media.0.mediaType,media.0.width,media.0.videoEmbedUrl,media.0.videoVideoThumbnailUri,media.0.url,attributes&pageSize={self.page_size}&page={self.page}&country={self.country}&useMultiFacetedFacets=true&distance={self.distance}mi&length={self.length_min}-{self.length_max}&uom=ft&sort=length-desc&multiFacetedBoatTypeClass=[%22sail%22]"
        url = f"https://api-gateway.boats.com/api-boattrader-client/app/search/boat?apikey=8b08b9bc353c494a80c60fb86debfc56&pageSize={self.page_size}&page={self.page}&country={self.country}&facets=country,state,make,makeModel,class,fuelType,hullMaterial,stateCity,priceRevisedSince,minMaxPercentilPrices,condition&fields=id,make,model,year,featureType,specifications.dimensions.lengths.nominal.ft,location.address.state,location.address.country,location.address.city,aliases,owner.logos.enhanced,owner.name,owner.rootName,price.hidden,price.type.amount.USD,price.discount.amount.USD,price.discount.revisedDate,portalLink,media.0.title,media.0.date.modified,media.0.mediaType,media.0.width,media.0.videoEmbedUrl,media.0.videoVideoThumbnailUri,media.0.url,attributes&useMultiFacetedFacets=true&distance={self.distance}mi&length={self.length_min}-{self.length_max}&uom=ft&sort=length-desc&multiFacetedBoatTypeClass=[%22sail%22]"
        #print(url)
        return url 

    def make_request(self):
        #print("make_request")
        url = self.set_url()
        return requests.request("GET",url,headers=self.headers)

    def get_data(self):
        #print("get_data")
        self.data = self.make_request().json()
    
    def save_path(self,name):
        #print("save_path")
        download_dir = "output"
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        return f"{os.path.join(os.path.realpath(os.getcwd()),download_dir,name)}.csv"
    
    def init_csv(self,name):
        #print("init_csv")
        filepath = self.save_path(name)
        with open(filepath,'w', newline="") as f:
            csvwriter = csv.writer(f,delimiter=",")
            csvwriter.writerow(['id','price','make','model','year','length','city','state','country','owner'])

    def export_data(self,myList,name):
        #print("export_data")
        filepath = self.save_path(name)
        #print("writing: {}".format(filepath))
        with open(filepath, "a", newline='') as f:
            csvwriter = csv.writer(f,delimiter=",")
            #print("")
            #print(myList)
            #print("")
            csvwriter.writerow(myList)
        #with open(filepath,"w+",newline='') as f:
        #    f.write = csv.writer(filepath)
        #    f.write.writerows(['id','price','make','model','year','length','city','state','country','owner'])
        #    f.write.writerows(myList)

    def scrape(self,pages):
        #print("scrape")
        self.init_csv("output")
        for page in range(1,pages):
            print("Page: {} of {}".format(page,pages))
            self.make_request()
            self.get_data()
            #print("")
            #print("\r\rGot data?\r\r")
            #print(self.data)
            #print("")
            for item in self.data['search']['records']:
                thisList = []
                thisList.append(item['id'])
                if item['price']['hidden']:
                    thisList.append("")
                else:
                    thisList.append("${:,.2f}".format(item['price']['type']['amount']['USD']))
                thisList.append(item['make'])
                thisList.append(item['model'])
                thisList.append(item['year'])
                thisList.append(item['specifications']['dimensions']['lengths']['nominal']['ft'])
                if 'city' in item['location']['address']:
                    thisList.append(item['location']['address']['city'])
                else:
                    thisList.append("")
                thisList.append(item['location']['address']['state'])
                thisList.append(item['location']['address']['country'])
                if 'rootName' in  item['owner']:
                    thisList.append(item['owner']['rootName'])
                else:
                    thisList.append(item['owner']['name'])
                self.export_data(thisList,"output")
            #self.pages += 1
    
scrapper = Scrapper(5000,56,1,"US",34,55)
scrapper.scrape(7)

