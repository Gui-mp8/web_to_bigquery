class BigQueryConfig:
    def __init__(self, project_name: str, dataset_name: str, table_name: str):
        self.project_name: str = project_name
        self.dataset_name: str = dataset_name
        self.table_name: str = table_name
