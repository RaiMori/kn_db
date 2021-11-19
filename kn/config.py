

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class KnConfig:
    def __init__(self) -> None:
        self.data_path = r"C:/_projects/kn_monitoring/data"
        self.db_compare_base = r"C:\_projects\kn_monitoring\data\db-A03-2021-11-03-18_08_22.json"
        self.base_url = 'http://localhost:5000'