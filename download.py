import asyncio, csv
from datetime import datetime
from dataclasses import dataclass, field
from queue import PriorityQueue
# from collections import defaultdict
import httpx


if False:
    URL = 'https://www.retsinformation.dk/api/documentsearch/csv??t=*'
    r = httpx.get(URL, timeout=9999)
    with open("data.csv", "wt") as f:
        f.write(r.text)


@dataclass(order=True)
class PrioritizedItem:
    priority: datetime
    data: dict = field(compare=False)

async def main():
    q = PriorityQueue()  # type: PriorityQueue[PrioritizedItem]

    with open('data.csv', mode='r', newline='') as f:
        #f.readline()  # skip header
        for row in csv.DictReader(f):
            print(row)
            if row['DokumentType'] != 'Lov':
                print('Skipping: ' + row['DokumentType'])
                continue
            if (d_str := row['UnderskriftDato']):
                d = datetime.strptime(d_str, '%Y%m%d')  # YYYYMMDD
                row['UnderskriftDato'] = d
                q.put(PrioritizedItem(d, row))
            else:
                print(f'Failed: {row}')

    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.example.com/')

if __name__ == "__main__":
   asyncio.run(main())
