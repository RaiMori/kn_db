import pathlib
import re
from datetime import datetime
from kn.config import KnConfig
DATA_PATH = 'C:/_projects/kn_monitoring/data'

cfg = KnConfig()
class DbManagment():

    def __init__(self, data_path=cfg.data_path) -> None:
        self.data_path = pathlib.Path(data_path)

    def get_latest(self):
        pass

    def get_files_dates(self, block):
        files = []
        date_pattern = 'db-A\d{2}-(\d{4}-\d{2}-\d{2}-\d{2}_\d{2}_\d{2}).json'
        for f in self.data_path.iterdir():
            date_str = re.search(date_pattern, f.name).group(1)
            date = datetime.strptime(date_str, '%Y-%m-%d-%H_%M_%S')
            files.append((f.name, date))
        return files

    def get_files(self):
        files = []
        for f in self.data_path.iterdir():
            files.append(f.name)

        return files


if __name__=='__main__':
    db = DbManagment()
    db.get_yesterday()