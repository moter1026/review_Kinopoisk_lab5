import os
import shutil
import description
import random
import csv
# import pandas as pd


def delete_files_and_dir(dir):
    all_files = os.listdir(dir)
    for file in enumerate(all_files):
        os.remove(dir+"/"+file[1])
    os.rmdir(dir)

def make_copy_dataset_random(name: str):
    if not os.path.isdir(name):
        os.mkdir(name)
    else:
        delete_files_and_dir("./"+ name)
        os.mkdir(name)


    if os.path.isdir("./dataset/good/copy"):
        delete_files_and_dir('./dataset/good/copy')
        
        
    if os.path.isdir("./dataset/bad/copy"):
        delete_files_and_dir("./dataset/bad/copy")

    shutil.copytree('./dataset/good',
        os.path.join('./dataset/good/copy'))
    shutil.copytree('./dataset/bad',
        os.path.join('./dataset/bad/copy'))

    all_good_files = os.listdir("./dataset/good/copy")
    all_bad_files = os.listdir("./dataset/bad/copy")

    length_of_all_files = len(all_good_files) + len(all_bad_files)

    for file in enumerate(all_good_files):
        try:
            os.rename('./dataset/good/copy/'+file[1], './'+ name +'/good_'+file[1])
        except Exception as e:
            continue;
        # end try

    for file in enumerate(all_bad_files):
        try:
            os.rename('./dataset/bad/copy/'+file[1], './'+ name +'/bad_'+file[1])
        except Exception as e:
            continue;
        # end try

    delete_files_and_dir('./dataset/good/copy')
    delete_files_and_dir("./dataset/bad/copy")

    name_of_descript_file = "description_three_random"
    path = "./" + name
    description.make_description(name_of_descript_file, path)

    rand_names = []
    list_objects = []

    list_objects = []
    with open("description_three_random.csv", encoding='utf-8') as r_file:
        reader_object = csv.reader(r_file, delimiter = ",")
        count = 0
        
        for row in reader_object:
            if count == 0:
                list_objects.append(row)
            elif (count % 2 == 0):
                while 1:
                    rand_num = random.randrange(0, 10000)
                    if not(rand_num in rand_names):
                        os.rename(row[1], row[1][0:row[1].rfind("\\") + 1]+str(rand_num)+".txt")
                        rand_names.append(rand_num)
                        row[0] = row[0][0:row[0].rfind("\\") + 1] + str(rand_num)+".txt"
                        row[1] = row[1][0:row[1].rfind("\\") + 1] + str(rand_num)+".txt"
                        list_objects.append(row)
                        break
            count += 1
    with open("description_three_random.csv", encoding='utf-8', mode="w") as w_file:
        writer = csv.writer(w_file)
        writer.writerows(list_objects)