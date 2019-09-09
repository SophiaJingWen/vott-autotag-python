import random
import os
import json
import jsonutil

""" def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError """

class Asset:

    def __init__(self, option, assetId, assetName, width, height):

        self.assetObj = {
            "asset": {
                "format": "jpeg",
                "id": assetId, 
                "name": assetName,
                "path": 'file:' + option['picPath'] + '/' + assetName,
                "size": {
                    "width": width, 
                    "height" : height
                },
                "state": 2,
                "type": 1
            },
            "regions": [
                
            ],
            "version": "2.1.0"
        }

    def addRegions(self,regions):

        regionsArray = []

        for regionId in regions.keys():

            [top,left,width,height] = regions[regionId]

            regionObj = {
                "id": regionId,
                "type": "RECTANGLE",
                "tags": [
                    "未标注"
                ],
                
                "boundingBox": {
                    "height": height,
                    "width" : width,
                    "left" : left,
                    "top" : top
                },
                "points": [
                    {
                        "x": left, 
                        "y": top 
                    },
                    { 
                        "x": left + width, 
                        "y": top 
                    },
                    {
                        "x": left + width, 
                        "y": top + height
                    },
                    {
                        "x": left, 
                        "y": top + height 
                    }
                ]
            }

            regionsArray.append(regionObj)


        self.assetObj['regions'] = regionsArray

    def save(self,path):
        with open( path + '/' + self.getId() + '-asset.json', 'w', encoding='utf-8') as f:
            #json.dumps(self.assetObj, default=set_default, ensure_ascii=False, indent=4)
            json.dump(self.assetObj, f, ensure_ascii=False, indent=4)
            #fs.writeFileSync(`${path}/${this.getId()}-asset.json`, JSON.stringify(this.assetObj,null,4));

    def getAssetInfo(self):
        return self.assetObj['asset']

    def getId(self):
        return self.assetObj['asset']['id']

    def getName(self):
        return self.assetObj['asset']['name']

    assetObj : dict


class ExportSrc:

    def __init__(self,filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            result = json.load(f)
            self.exportVottObj = result

    def getExportVottObj(self):
        return self.exportVottObj

    def getAssets(self):
        return self.exportVottObj["assets"]

    def getName(self,assetId):
        return self.exportVottObj["assets"][assetId]["asset"]["name"]

    def getWidth(self,lastId):
        return self.exportVottObj["assets"][lastId]["asset"]["size"]["width"]

    def getHeight(self,lastId):
        return self.exportVottObj["assets"][lastId]["asset"]["size"]["height"]

    exportVottObj : dict



class Exporter:

    def __init__(self,option):
        self.exporterOption = option
    
    def export(self):
        self.clean()
        assets = self.createAssets()
        self.updateFile(assets)
    
    def clean(self):
        jsonutil.remove(self.exporterOption['outputPath'])

    def createAssets(self):
        exportVottObj = ExportSrc(self.exporterOption['exportVottPath'])
        boxObj : dict
        with open(self.exporterOption['boxPath'], 'r', encoding='utf-8') as f:
            boxObj = json.load(f)
        assets = []
        self.setImageSize()

        for assetId in exportVottObj.getAssets().keys():

            assetName = exportVottObj.getName(assetId)
            regions = boxObj[assetName]

            if regions:

                asset = Asset(self.exporterOption, assetId, assetName, self.width, self.height)
                asset.addRegions(regions)
                asset.save(self.exporterOption['outputPath'])
                assets.append(asset)

        return assets
        
    def setImageSize(self):
        [width, height] = self.getLastImageSize()
        self.width = width
        self.height = height

    def updateFile(self,assets):
        with open(self.exporterOption['testVottPath'], 'r', encoding='utf-8') as f:
            testVottObj = json.load(f)
        
        for asset in assets:
            assetId = asset.getId()

            if testVottObj['assets'].get(assetId):
                testVottObj['assets'][assetId]['state'] = 2
            else:
                testVottObj['assets'][assetId] = asset.getAssetInfo()

        with open(self.exporterOption['testVottPath'], 'w', encoding='utf-8') as f:
            json.dump(testVottObj, f, ensure_ascii=False, indent=4)
            #fs.writeFileSync(this.exporterOption.testVottPath, JSON.stringify(testVottObj,null,4));

    def getLastImageSize(self):

        exportVottObj = ExportSrc(self.exporterOption['exportVottPath'])
        width : int 
        height : int
        for (assetId,info) in exportVottObj.getAssets().items():
            if info['asset']['size']:
                width = exportVottObj.getWidth(assetId)
                height = exportVottObj.getHeight(assetId)
        return [width,height]

    exporterOption : dict
    width : int 
    height : int


option = {
    'boxPath' : "C:/Users/sophiawen/Desktop/数据/Vott/yly2_box.json",
    'exportVottPath' : "C:/Users/sophiawen/Desktop/test-output/vott-json-export/test-export.json",
    'testVottPath' : "C:/Users/sophiawen/Desktop/test-output/test.vott",
    'outputPath' : "C:/Users/sophiawen/Desktop/test-output",
    'picPath' : "C:/Users/sophiawen/Desktop/数据/Vott/yly2"
}


if __name__ == '__main__':
    myExporter = Exporter(option)
    myExporter.export()


    
