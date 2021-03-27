from datetime import datetime

def getAge(idNum):
    if len(idNum) == 14:
        if idNum[0] == '3':
            centuryIs = 2000
            dateofbirth =  centuryIs + int(idNum[1]+idNum[2])
            today = datetime.today()
            datem = today.year
            age = datem - dateofbirth
            return age
        elif idNum[0] == '2':
            centuryIs = 1900
            dateofbirth =  centuryIs + int(idNum[1]+idNum[2])
            today = datetime.today()
            datem = today.year
            age = datem - dateofbirth
            return age
        else:
             return 0    
    else:
        return 0

      