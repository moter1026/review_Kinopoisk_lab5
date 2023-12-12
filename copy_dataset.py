import os
import shutil
import description


def delete_files_and_dir(dir):
    all_files = os.listdir(dir)
    for file in enumerate(all_files):
        os.remove(dir+"/"+file[1])
    os.rmdir(dir)

def make_copy_dataset(name: str):
    if not os.path.isdir(name):
        os.mkdir(name)
    else:
        delete_files_and_dir("./" + name)
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



    name_file = "description_two"
    name_dir = "./" + name

    description.make_description(name_file, name_dir)
