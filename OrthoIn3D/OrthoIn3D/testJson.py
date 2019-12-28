import json

data_dict = {'patientName': 'Doe',
                          'patientSurname': 'John',
                          'Sex' : 'None',
                          'age': 45,
                          'mandi': False,
                          'maxi': False,
                          'missingTeethMandi' : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          'missingTeethMaxi' : [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                          'inclusionSphereDiamMandi' : [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8],
                          'inclusionSphereDiamMaxi' : [8,8,7,7,6,5,3,2,2,3,5,6,7,7,8,8],
             'pickedPoints': {}
                         }

teeth_dict = {}

# Two dictionaries
tooth_dict1 = {
    "1" : {"Coords" : [43, 20, 10]}
    }
tooth_dict1["1"].update({"name" : 18})
tooth_dict1["1"].update({"diamSphere" : 4})

tooth_dict2 = { 
    "2" : {"Coords" : [11, 22, 33]}
    }
tooth_dict2["2"].update({ "name" : 34})
tooth_dict2["2"].update({ "diamSphere" : 2})

    
# Adding elements from dict2 to dict1
teeth_dict.update( tooth_dict1 )
teeth_dict.update( tooth_dict2 )
    
print("Content of teeth_dict : ")
for (key, value) in teeth_dict.items() :
    print(key , " :: ", value )

print(teeth_dict["1"]["Coords"][1])

data_dict["pickedPoints"].update(teeth_dict)

print("Content of data_dict : ")
for (key, value) in data_dict.items() :
    print(key , " :: ", value )
    
print(data_dict["pickedPoints"]["2"]["Coords"][2])