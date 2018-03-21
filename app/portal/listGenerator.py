
def listGenerator(queryResponse):
    newList = []
    temporaryList = queryResponse[:]
    for outerValue in temporaryList:
        multiplier = 0
        for index, innerValue in enumerate(queryResponse):
            if outerValue['foss'] == innerValue['foss']:
                multiplier += innerValue['multiplier']
                queryResponse.pop(index)
        outerValue['multiplier'] = multiplier
        if (outerValue['multiplier'] != 0):
            newList.append(outerValue)
    return newList
