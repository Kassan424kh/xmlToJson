import json 
import xmltodict
import pprint


def setValueInKeyIfhasSameName(dictData) -> dict:
    if not isinstance(dictData, str):
        for key, value in dictData.items():
            if isinstance(value, dict):
                if key == "ServerSettings":
                    for items in value.values():
                        newKeyAndValue= {}
                        value = {}
                        for s in items:
                            newKeyAndValue[s["Key"]["text"]] = None if (s["Value"] is None) else s["Value"]["text"]
                        value = newKeyAndValue
                    dictData[key] = value
                if len(value.keys()) == 1 and "string" in value.keys():
                    dictData[key] = value["string"]
                    if key == "Description" and isinstance(dictData[key], dict)  and "value" in dictData[key].keys():
                        stringMap = {"stringMap" : {}}
                        languageValues = dictData[key]["value"]
                        for languageValue in languageValues:
                            if "language" in languageValue and "text" in languageValue:
                                stringMap["stringMap"][languageValue["language"]] = languageValue["text"]
                        if len(stringMap["stringMap"].keys()) < 1:
                            stringMap["stringMap"] = None
                        dictData[key] = stringMap
                if key == "Name" and "string" in value.keys() and isinstance(value["string"], dict) and "value" in value["string"].keys():
                    stringMap = {"stringMap" : {}}
                    languageValues = value["string"]["value"]
                    for languageValue in languageValues:
                        if "language" in languageValue and "text" in languageValue:
                            stringMap["stringMap"][languageValue["language"]] = languageValue["text"]
                    if len(stringMap["stringMap"].keys()) < 1:
                        stringMap["stringMap"] = None
                    dictData[key] = stringMap
                for valueKey, valueValue in value.items():
                    if isinstance(valueValue, dict):
                        setValueInKeyIfhasSameName(valueValue)
                    elif isinstance(valueValue, list):
                        for element in valueValue:
                            setValueInKeyIfhasSameName(element)
                    if key == str(valueKey) + "s" or (key == "Categories" and valueKey == "Category"):
                        dictData[key] =  dictData[key][valueKey]
                if key == "FieldTypes":
                    for fieldType in dictData[key]:
                        print(fieldType)
                        if isinstance(fieldType, dict) and "Description" in fieldType.keys() and fieldType["Description"] is None:
                            fieldType["Description"] = {"stringMap" : None}

            if isinstance(value, dict) and len(value.values()) ==  1 and "text" in value.keys():
                dictData[key] = dictData[key]["text"]

            
    return dictData



xmlFilePath = str(input(".XML file path (e.g.: path/to/your/file.xml): "))
pathToSaveJsonFile = str(input(".JSON file path (e.g.: path/to/your/file.json): "))
if xmlFilePath != "" and pathToSaveJsonFile != "":
    with open(xmlFilePath, 'r') as fd:
        xmlData = fd.read()
        xmlToJson = json.loads(json.dumps(xmltodict.parse(
            xmlData, 
            force_cdata=True, 
            attr_prefix='', 
            cdata_key='text', 
        )
        ))
        data = setValueInKeyIfhasSameName(xmlToJson.get("Model"))
        model_data = {}
        with open(pathToSaveJsonFile, 'w') as outfile:
            model_data = data
            json.dump(model_data, outfile)

else:
    print("Please set files paths")
