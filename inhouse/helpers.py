from datetime import datetime

def getAge(idNum):
    if idNum < 10000000000000:
        return 0
    today = datetime.today()
    datem = today.year
    dateofbirth = int(idNum/10000000000) - 1000
    age = datem - dateofbirth 
    return age




