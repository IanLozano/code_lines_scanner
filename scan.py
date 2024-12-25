import os, sys
import matplotlib.pyplot as plt
import datetime as dt

save_folder = "SCAN"
if not os.path.exists(save_folder):
    os.mkdir(save_folder)
    
folder = input("Enter folder to scan: ")
print("FOLDER", folder)
if not os.path.exists(folder):
    print("Folder {} does not exist!".format(folder))
    sys.exit(0)
print("Continuing script!")

file_list = os.listdir(folder)

files = os.listdir(folder)[1:]
files_dict = {files[i]: 0 for i in range(len(files))}
extensions = [f.split(".")[1] for f in files]
extensions_set = list(set(extensions))
extensions_dict = {extensions_set[i]: 0 for i in
                       range(len(extensions_set))}
extensions_dict

for k in files_dict:
    # print(k)
    
    with open(folder + os.sep + k, "r") as r:
        read = r.readlines()
        
    files_dict[k] = len(read)
    
for k in files_dict:
    ext_key = k.split(".")[1]
    extensions_dict[ext_key] += files_dict[k]
total = sum(extensions_dict.values())

for k in extensions_dict:
    
    value = (extensions_dict[k]/total)*100
    
    r_value = round(value, 2)
    extensions_dict[k] = str(r_value) + "%"
for k in extensions_dict:
    print("Language: {}".format(k))

plt.figure(figsize = (10, 5))
plt.title("% of Languages in {} dir".format(folder),
          fontsize = 30)
data = list(extensions_dict.values())
labels = list(extensions_dict.keys())
for k in extensions_dict:
    number = float(extensions_dict[k].split("%")[0])

    plt.bar(k, height = number)
timestamp = dt.datetime.now().strftime("%Y-%m-%d")
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.xlabel("languages", fontsize = 15)
plt.ylabel("%", fontsize = 15)
plt.legend(labels = data, fontsize = 20)
plt.savefig(save_folder + os.sep + folder + "_{}_.png".format(timestamp),
            bbox_inches = "tight")
plt.show()
