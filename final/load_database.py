import csv
from final.models import *

def add_cities():
    # 590 records
    i = 0
    with open('final.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i += 1
            if i%100 == 0:
                print('Done : ', i)

            c = City(
                name = row[1],
            )
            try:
                c.save()
            except:
                print('Cant save : ', row)
        print('All Done')

def create_types():
    type_names = [
        'Honeymoon',
        'Adventure',
        'Pilgrimage',
        'Business',
        'Group',
        'Solo',
        'Photography',
        'Food',
        'Sightseeing',
        'Medical',
        'Cruise',
        'Agritourism',
        'Alternative',
        'tourism',
        'Festivals',
        'Wildlife',
        'sanctuary',
        'Camping',
        'Other'
    ]
    print(type_names)

    for name in type_names:
        Type(name=name).save()
        print('Saved Type : ', name)

def create_activities():
    activity_names = [
        'Star gazing',
        'Fly Fishing',
        'Horseback riding',
        'Cycling',
        'Mountain biking',
        'Whitewater rafting',
        'Rock climbing',
        'Camping',
        'Desert safari',
        'Skydiving',
        'Bonfire',
        'Cultural night',
        'Other'
    ]

    print(activity_names)

    for name in activity_names:
        Activity(name=name).save()
        print('Saved Activity : ', name)

def add_states():
    states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttarakhand",
    "Uttar Pradesh",
    "West Bengal",
    "Union Territories",
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and",
    "Daman & Diu",
    "The Government of NCT of Delhi",
    "Jammu & Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry"
    ]

    for state in states:
        i = 0
        try:
            c = City(name=state)
            c.save()
            print("Added", state)
        except:
            i += 1
            print("Cant add", state)

    print("States added ," , len(states) -i)
