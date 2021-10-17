import json
if __name__=="__main__":
    import kn_scrapper
DB_FILE_OLD = r"C:\_projects\test-prj\db-A03-2021-10-11-01_00_01.json"
DB_FILE_OLD = r"C:\_projects\test-prj\db-A03-2021-10-16-16_25_57.json"
DB_FILE_NEW = r"C:\_projects\test-prj\db-A03-2021-10-17-18_45_56.json"


class KnTransfers:
    def __init__(self, old_db=DB_FILE_OLD, new_db=DB_FILE_NEW) -> None:
        self.old_db = old_db
        self.new_db = new_db

    def get_last_db(block):
        pass

    
    def get_db(self, file):
        with open(file, 'r+') as f:
            content = f.read()

        return json.loads(content)

    def get_dbs(self):
        old = self.get_db(self.old_db)
        new = self.get_db(self.new_db)
        return old, new

    def generate_person_db(self,DB_FILE_NEW):
        with open(DB_FILE_NEW, "r") as f:
            db_str = f.read()
            db =  json.loads(db_str)

        persons = {}
        for room in db:
            for k, v in room.items():
                room_num = k
                v = v
            for p in v:
                persons[p] = room_num
        return persons

    def get_transfers(self):
        persons_old, persons_new = self.get_persons_dbs()
        transfers = []
        for p, r in persons_new.items():
            if not persons_old.get(p, ""):
                #print(f"Person {p} is new in room {r}")
                transfers.append((p, 'new', r))
                continue

            if persons_old[p] == r:
                continue

            if persons_old[p] != r:
                transfers.append((p, 'moved', (persons_old[p], r)))
                #print(f"Person {p} moved from old room: {persons_old[p]} to new room {r}")
                continue

        for p, r in persons_old.items():
            if not persons_new.get(p, ""):
                transfers.append((p, "out", r))

        return transfers

    def get_persons_dbs(self):
        persons_old = self.generate_person_db(self.old_db)
        persons_new = self.generate_person_db(self.new_db)
        return persons_old,persons_new

    def compare(self, scrapper_class=None):
        trs = self.get_transfers()
        print('########## Transfers ###########')
        [print(t) for t in trs]
        print('_____________________')
        old, new = self.get_dbs()
        print(__name__)
        if not scrapper_class:
            scrapper_class = kn_scrapper.KNScrapper
        print('########## Old statistics ##########')
        scrapper_class.statistics(old)
        print('____________________')
        
        print('########## New statistics ##########')
        scrapper_class.statistics(new)
        print('____________________') 






if __name__=="__main__":
    transfers = KnTransfers()
    # trs = transfers.get_transfers()
    # [print(t) for t in trs]
    # old, new = transfers.get_dbs()
    # print('########## Old statistics ##########')
    # kn_scrapper.KNScrapper.statistics(old)
    # print('____________________')
    
    # print('########## New statistics ##########')
    # kn_scrapper.KNScrapper.statistics(new)
    # print('____________________')
    # #s.statistics(old)
    transfers.compare()
