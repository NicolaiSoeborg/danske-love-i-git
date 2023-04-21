import os
import csv
from datetime import datetime
from collections import defaultdict

def clean(name, val):
    if name in ["Nummer", "År"]:
        return int(val)
    #if name in ["UnderskriftDato", "PubliceretTidspunkt", "SidstPubliceretTidspunkt", "BekendtgørelsesDato", "HistoriskDato"]:
    #    try:
    #        return datetime.strptime(val, '%Y%m%d')  # .isoformat()
    #        #return datetime.strptime(val, '%Y%m%d').strftime('%s')  # unix
    #    except:
    #        return val
    #if name == "Historisk":
    #    if val == "True": return True
    #    elif val == "False": return False
    #    assert False, f'Bad value: {val}'
    return val


def iter_laws():
    with open('love.csv', mode='r', encoding='iso8859_10', newline='') as f:
        for row in csv.DictReader(f):
            res = {}
            for k, v in row.items():
                res[k] = clean(k, v)
            yield res


seen = set()
for law in iter_laws():
    if law['ACCN'] in seen:
        print("WAAT", law)
        exit(0)
    seen.add(law['ACCN'])
    if law['ÆndrerI'] != '':  # Tiltræder
        print(law)

"""
https://www.retsinformation.dk/eli/accn/G198450870Z1/xml
https://www.retsinformation.dk/eli/accn/ACCN/xml
<EndDate REFid="submit_1">2000-06-06</EndDate>
<Status>Historic</Status>

=> https://www.retsinformation.dk/api/document/eli/retsinfo/1984/50870
=> https://www.retsinformation.dk/api/document/eli/retsinfo/År/Nummer

"""
