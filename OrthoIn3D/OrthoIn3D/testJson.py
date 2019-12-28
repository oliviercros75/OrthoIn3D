import json

oridict = {}

# Two dictionaries
dict1 = {
    "1" : {"Coords" : [43, 20, 10]}
    }
dict1["1"].update({"name" : 18})

dict2 = { 
    "2" : {"Coords" : [11, 22, 33]}
    }
dict2["2"].update({ "name" : 34})

    
# Adding elements from dict2 to dict1
oridict.update( dict1 )
oridict.update( dict2 )
    
print("Content of oridict : ")
for (key, value) in oridict.items() :
    print(key , " :: ", value )

print(oridict["1"]["Coords"][1])