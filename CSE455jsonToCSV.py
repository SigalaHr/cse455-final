import os
import json
import random
def convert_annotations(annotation_folder_path, train_annotation_path, test_annotation_path, train_text_file_path, test_text_file_path, path_to_image_folder, path_to_classes_file, random_test_portion):
    with open(path_to_classes_file, 'w+') as classes_file:
        classes_file.write("Friendly\n")
        classes_file.write("Enemy\n")
            
    data = {}
    with open(train_annotation_path, 'w+') as train_anno, open(test_text_file_path, 'w+') as test_text_file, open(train_text_file_path, 'w+') as train_text_file:
        with open(test_annotation_path, 'w+') as test_anno:
            train_anno.write("ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside\n")
            test_anno.write("ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside\n")
            
            test_text = ""
            train_text = ""
            for filename in os.listdir(annotation_folder_path):
                with open(annotation_folder_path + "/" + filename) as f:
                            data = json.load(f)
                            try:
                                data["asset"]["name"]
                                is_training_image = False
                                if(random.random() > random_test_portion):
                                    is_training_image = True
                                if(is_training_image):
                                    train_text_file.write(path_to_image_folder + "/" + data["asset"]["name"] + "\n")
                                else:
                                    test_text_file.write(path_to_image_folder + "/" + data["asset"]["name"] + "\n")
                                    
                                for region in data["regions"]:
                                    line_out = ""
                                    line_out += data["asset"]["name"]
                                    line_out += ","
                                    line_out += "idkwhattoputhere"
                                    line_out += ","
                                    #For now, classify enemy with name overlay as an enemy
                                    if(region["tags"][0] == "EnemyWithNameOverlay"):
                                        line_out += "Enemy"
                                    else:
                                        line_out += region["tags"][0]
                                    #Confident
                                    line_out += ",1,"
                                    bb = region["boundingBox"]
                                    line_out += str(bb["left"])
                                    line_out += ","
                                    line_out += str(bb["top"])
                                    line_out += ","
                                    line_out += str(bb["left"] + bb["width"])
                                    line_out += ","
                                    line_out += str(bb["top"] + bb["height"])
                                    line_out += ","
                                    #Again, just an enemy for now, but we can say it's occluded confidently. Sometimes boxes will overlap, but
                                    #too lazy to check for that, might need to relable data if it makes a big difference.
                                    if(region["tags"][0] == "EnemyWithNameOverlay"):
                                        line_out += "1,"
                                    else:
                                        line_out += "0,"
                                    #truncated if on edge of screen, though I truncated boxes for some when they were occluded...
                                    if(bb["left"] <= .01 or
                                       bb["top"] <= .01 or
                                       bb["left"] + bb["width"] >= data["asset"]["size"]["width"]-.01 or
                                       bb["top"] + bb["height"] >= data["asset"]["size"]["height"]-.01):
                                            line_out += "1,"
                                    else:
                                            line_out += "0,"

                                    #group, not
                                    line_out += "0,"
                                    #depiction, not
                                    line_out += "0,"
                                    #inside? not?
                                    line_out += "0"
                                    line_out += "\n"

                                    if(is_training_image):
                                        train_anno.write(line_out)
                                    else:
                                        test_anno.write(line_out)
                                    
                                    #print(line_out)
                            except:
                                pass
        
convert_annotations("./training_annotated",
                    "./train-annotations-bbox.csv",
                    "./test-annotations-bbox.csv",
                    "./train_list.txt",
                    "./test_list.txt",
                    "/homes/iws/sigalahr/cse455/final/images",
                    "./classes.txt",                    
                    .1)
