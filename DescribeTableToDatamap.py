import json
from collections import OrderedDict
import os



def main():


    datamap = OrderedDict()
    datamap["definitions"] = OrderedDict()
    datamap["plan"] = OrderedDict()
    datamap["export"] = {"format": "json"}

    # should loop through all DescribeTable text files in here and create an Entity in Definitions
    # as well as an entry in Plan for each.

    dynamoContents = {}

    with open("output.txt", 'r') as f:
        dynamoContents = json.load(f)

    print(dynamoContents['Table']['AttributeDefinitions'])
    print(dynamoContents['Table']['KeySchema'])

    entity = dynamoContents["Table"]["TableName"]

    datamap["definitions"][entity] = {}
    datamap["definitions"][entity]["properties"] = OrderedDict()

    # add hash key first
    for attributeDict in dynamoContents['Table']['KeySchema']:
        if attributeDict['KeyType'] == 'HASH':

            attributeName = attributeDict['AttributeName']

            datamap["definitions"][entity]["properties"][attributeName] = {"unique": True}

    # add range key second
    for attributeDict in dynamoContents['Table']['KeySchema']:
        if attributeDict['KeyType'] == 'RANGE':
            attributeName = attributeDict['AttributeName']

            datamap["definitions"][entity]["properties"][attributeName] = {"unique": True}

    # add rest of the attributes
    for attributeDict in dynamoContents['Table']['AttributeDefinitions']:
        attributeName = attributeDict['AttributeName']

        if attributeName not in datamap["definitions"][entity]["properties"].keys():
            datamap["definitions"][entity]["properties"][attributeName] = {"constant": None}

    print(datamap)
    with open(os.path.join('datamap','dynamoDatamap.json'), "w") as outfile:
        json.dump(datamap, outfile)



if __name__ == '__main__':
    main()