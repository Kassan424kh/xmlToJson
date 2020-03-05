import json
import xmltodict
import pprint


FieldAndLinkTypes = {
            "FieldTypes" : [],
        }

def setValueInKeyIfhasSameName(dictData) -> dict:
    if not isinstance(dictData, str):
        
        for key, value in dictData.items():
            if key == "FieldSets":
                dictData[key] = []
            if isinstance(value, dict):
                if key == "ServerSettings":
                    for items in value.values():
                        newKeyAndValue = {}
                        value = {}
                        for s in items:
                            newKeyAndValue[s["Key"]["text"]] = "" if (
                                s["Value"] is None) else s["Value"]["text"]
                        value = newKeyAndValue
                    dictData[key] = value
                if len(value.keys()) == 1 and "string" in value.keys():
                    dictData[key] = value["string"]
                    if (key == "Description" or key == "SourceName" or key == "TargetName") and isinstance(dictData[key], dict) and "value" in dictData[key].keys():
                        stringMap = {"stringMap": {}}
                        languageValues = dictData[key].get("value")
                        if isinstance(languageValues, list):
                            for languageKey in languageValues:
                                if "language" in languageValue.keys() and "text" in languageValue.keys():
                                    languageKey = languageValue["language"]
                                    if languageValue["language"] == "de-DE":
                                        languageKey = "de"
                                    stringMap["stringMap"][languageKey
                                                           ] = languageValue["text"]
                        elif isinstance(languageValues, dict):
                            if "language" in languageValues.keys() and "text" in languageValues.keys():
                                languageKey = languageValues["language"]
                                if languageKey == "de-DE":
                                    languageKey = "de"
                                stringMap["stringMap"][languageKey
                                                       ] = languageValues["text"]
                        dictData[key] = stringMap
                if key == "Name" and "string" in value.keys() and isinstance(value["string"], dict) and "value" in value["string"].keys():
                    stringMap = {"stringMap": {}}
                    languageValues = value["string"]["value"]
                    if isinstance(languageValues, list):
                        for languageValue in languageValues:
                            if "language" in languageValue and "text" in languageValue:
                                languageKey = languageValue["language"]
                                if languageKey == "de-DE":
                                    languageKey = "de"
                                stringMap["stringMap"][languageKey
                                                       ] = languageValue["text"]
                    elif isinstance(languageValues, dict):
                        if "language" in languageValues.keys() and "text" in languageValues.keys():
                            languageKey = languageValues["language"]
                            if languageKey == "de-DE":
                                languageKey = "de"
                            stringMap["stringMap"][languageKey
                                                   ] = languageValues["text"]
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
                        dictData[key] = dictData[key][valueKey]
                if key == "Settings":
                    if isinstance(dictData[key], list):
                        newSettingsObject = {}
                        for settingsValue in dictData[key]:
                            if "SettingsKey" in settingsValue and "SettingsValue" in settingsValue:
                                newSettingsObject[settingsValue["SettingsKey"]
                                                  ] = settingsValue["SettingsValue"]
                        dictData[key] = newSettingsObject
                    elif isinstance(dictData[key], dict):
                        newSettingsObject = {}
                        newSettingsObject[dictData[key]["SettingsKey"]
                                          ] = dictData[key]["SettingsValue"]
                        dictData[key] = newSettingsObject
                if key == "FieldTypes":
                    for fieldType in dictData[key]:
                        if isinstance(fieldType, dict):
                            if "Description" in fieldType.keys() and fieldType["Description"] is None:
                                fieldType["Description"] = {"stringMap": None}
                            if "Settings" in fieldType.keys() and fieldType["Settings"] is None:
                                fieldType["Settings"] = {}
            if isinstance(value, dict) and len(value.values()) == 1 and "text" in value.keys():
                dictData[key] = dictData[key]["text"]
            if key == "FieldTypes" and isinstance(dictData[key], dict):
                dictData[key] = [dictData[key]]
            if key == "CVLvalues":
                i = 0
                for item in dictData[key]:
                    item["id"] = i
                    item["DateCreated"] = "2017-08-18T14:58:00"
                    item["LastModified"] = "2017-08-18T14:58:00"
                    i += 1
            if key == "Languages":
                dictData[key] = [
                    {
                        "Name": "en",
                        "DisplayName": "English"
                    },
                    {
                        "Name": "de",
                        "DisplayName": "German"
                    }
                ]
            if key == "Index":
                if dictData[key] is not None:
                    dictData[key] = int(dictData[key])
            # Set EntityTypesId to fieldTypes in EntityTypes
            if key == "EntityTypes":
                for entityType in dictData[key]:
                    for fieldType in entityType["FieldTypes"]:
                        fieldType["EntityTypeId"] = entityType["Id"]
                    entityType["LinkTypes"] = []

            if key == "FieldTypes":
                FieldAndLinkTypes[key].extend(dictData[key])
        
    return dictData



xmlFilePath = str(input(".XML file path (e.g.: path/to/your/file.xml): "))
pathToSaveJsonFile = str(input(".JSON file path (e.g.: path/to/your/file.json): "))
if xmlFilePath != "" and pathToSaveJsonFile != "":
    with open(xmlFilePath, 'r', encoding="utf-8") as fd:
        xmlData = fd.read()
        
        xmlToJson = json.loads(json.dumps(xmltodict.parse(
            xmlData,
            force_cdata=True,
            attr_prefix='',
            cdata_key='text',
            encoding="utf-8"
        )))
        
        data = setValueInKeyIfhasSameName(xmlToJson.get("Model"))
        
        model_data = {}
        with open(pathToSaveJsonFile, 'w', encoding="utf-8") as outfile:
            data["DbVersion"] = "6.3.0.5"
            data["CustomerName"] = None
            data["Version"] = "1.0"
            data.update(FieldAndLinkTypes)

            for linkType in data["LinkTypes"]:
                for entityType in data["EntityTypes"]:
                    if linkType["SourceEntityTypeId"] == entityType["Id"]:
                        entityType["LinkTypes"].append(linkType)
                

            model_data = data
            json.dump(model_data, outfile, ensure_ascii=False)

else:
    print("Please set files paths")