'''
The function in this file takes in the payments
to be made in selected month and produces a new
list in which each user's record is merge into
one and total amount that needs to be paid is
displayed.
'''


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
