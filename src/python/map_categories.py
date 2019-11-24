import os


data_dir = "/home/krutika/Data/ds001246-download"
with open(os.path.join(data_dir, "imagenet_synset_to_human_label_map.txt"), "r") as file1:
    with open(os.path.join(data_dir, "stimulus_ImageNetTraining.tsv"), "r") as file2:
        with open(os.path.join(data_dir, "mapped_stimulus_ImageNetTraining.tsv"), "w") as file3:
            content1 = file1.read().split("\n")
            content2 = file2.read().split("\n")
            categories_map = {
                line.split("\t")[0]: line.split("\t")[1]
                for line in content1

            }
            stimulii = [line.split("\t") for line in content2]
            new_map = {}
            for stimulus in stimulii:
                category = stimulus[0].split("_")[0]
                if category not in new_map.keys():
                    new_map[category] = categories_map[category]
            string = ""
            for key, val in new_map.items():
                string += key+"\t"+val+"\n"
            file3.write(string)
