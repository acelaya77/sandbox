import requests
import json

url = 'https://api-gateway.boats.com/api-boattrader-client/app/search/boat?apikey=8b08b9bc353c494a80c60fb86debfc56&pageSize=56&page=1&country=US&facets=country,state,make,makeModel,class,fuelType,hullMaterial,stateCity,priceRevisedSince,minMaxPercentilPrices,condition&fields=id,make,model,year,featureType,specifications.dimensions.lengths.nominal.ft,location.address.state,location.address.country,location.address.city,aliases,owner.logos.enhanced,owner.name,owner.rootName,price.hidden,price.type.amount.USD,price.discount.amount.USD,price.discount.revisedDate,portalLink,media.0.title,media.0.date.modified,media.0.mediaType,media.0.width,media.0.videoEmbedUrl,media.0.videoVideoThumbnailUri,media.0.url,attributes&useMultiFacetedFacets=true&distance=2000mi&length=22-48&uom=ft&sort=length-desc&multiFacetedBoatTypeClass=[%22sail%22]'

request = requests.get(url)

data = request.json()

#print(data)

for item in data['search']['records']:
    thisList = []
    thisList.append(item['id'])
    thisList.append(item['make'])
    thisList.append(item['model'])
    thisList.append(item['year'])
    thisList.append(item['specifications']['dimensions']['lengths']['nominal']['ft'])
    thisList.append(item['location']['address']['city'])
    thisList.append(item['location']['address']['state'])
    thisList.append(item['location']['address']['country'])
    thisList.append(item['owner']['logo']['rootname'])
    print(thisList)
