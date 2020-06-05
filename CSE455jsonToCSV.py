import os
import json

annotation_folder_path = "C:/Users/Justin McGowen/Documents/CompVis/training_annotated"

train_annotation_path = "C:/Users/Justin McGowen/Documents/CompVis/test-annotations-bbox.csv"
test_annotation_path  = "C:/Users/Justin McGowen/Documents/CompVis/validation-annotations-bbox.csv"



def convert_annotations(annotation_folder_path, train_annotation_path, test_annotation_path):

    data = {}
    with open(train_annotation_path, 'w+') as train_anno:
        with open(test_annotation_path, 'w+') as test_anno:
            train_anno.write("ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside\n")
            test_anno.write("ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside\n")
            for filename in os.listdir(annotation_folder_path):
                with open(annotation_folder_path + "/" + filename) as f:
                    data = json.load(f)
                    try:
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

                            ######################################################################################################################
                            ######################################################################################################################
                            ##
                            ##          THIS NEXT PART NEEDS CHANGING BECAUSE IM NOT SURE WHAT WE GET - NEED TO SPLIT INTO TRAIN AND TEST FILES
                            ##
                            ######################################################################################################################
                            ######################################################################################################################
                            is_training_image = True
                            if(is_training_image):
                                train_anno.write(line_out)
                            else:
                                test_anno.write(line_out)
                            #print(line_out)
                    except:
                        pass
        
convert_annotations("C:/Users/Justin McGowen/Documents/CompVis/training_annotated",
                    "C:/Users/Justin McGowen/Documents/CompVis/test-annotations-bbox.csv",
                    "C:/Users/Justin McGowen/Documents/CompVis/validation-annotations-bbox.csv")
