import os
import csv


class Description:
    full_path = 0 #полный путь
    path = 0 #относительный путь
    type_class = 0

    def __init__(self, full_path, path, type_class):
        self.full_path = full_path
        self.path = path
        self.type_class = type_class

def about(dir: str) -> list:
    all_elems = os.listdir(dir);
    dirs = [];
    description = []
    for elem in enumerate(all_elems):
        if(elem[1].find(".") == -1):
            dirs.append(elem[1])
        else:
            ind = elem[1].find("_")
            full_path = os.path.abspath(dir+"/"+elem[1])
            path = os.path.relpath(dir+"/"+elem[1], os.getcwd())
            type_class = os.path.basename(os.getcwd()+"/"+dir)
            if not (ind == -1):
                type_class = elem[1][0:ind]
            description.append(Description(full_path, path, type_class))
    for next_dir in enumerate(dirs):
        description = description + about(str(dir)+"/"+str(next_dir[1]))
    return description



def make_description(name: str, name_dir: str) -> None:
    with open(name+".csv", mode="w+", encoding='utf-8') as textFile:
        file_writer = csv.writer(textFile, delimiter = ",")
        file_writer.writerow(["абсолютный путь к файлу", "относительный путь", "метка класса"])
        all_descriptions = about(name_dir)
        for description in enumerate(all_descriptions):
            file_writer.writerow([description[1].full_path, description[1].path, description[1].type_class])

