class Statistics:
    def __init__(self, filename:str, total_keys: int, unique_values: int, duplicated_values: int):
        self.filename = filename
        self.total_keys = total_keys
        self.unique_values = unique_values
        self.duplicated_values = duplicated_values

    def get_csv_line(self):
        return f"{self.filename}\t{self.total_keys}\t{self.unique_values}\t{self.duplicated_values}\n"
