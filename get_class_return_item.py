import csv


def get_class_return_item(class_name, elems):
        path = None
        file_class = 0
        with open("description_three_random.csv", "r", encoding='utf-8') as csvFile:
            read = csv.DictReader(csvFile)
            for i, row in enumerate(read, start=0):
                if row["метка класса"] == class_name:
                    if row["абсолютный путь к файлу"] in elems:
                        continue
                    path = row["абсолютный путь к файлу"]
                    file_class = row["метка класса"]

        # if path != None:     
        #     with open("return_path.csv", "a", encoding='utf-8') as TextFile:
        #         writer = csv.writer(TextFile, delimiter=",")
        #         writer.writerow([path, file_class])
        

        return path
