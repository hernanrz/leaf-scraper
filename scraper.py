from pyquery import PyQuery as pq
import csv
import requests
import os.path

ENDPOINT = "https://www.leafly.com/explore/page-{}/sort-alpha"
FIRST = "https://www.leafly.com/explore/sort-alpha"

session = requests.session()

session.headers.update({
    "Host": "www.leafly.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv67.0) Gecko/20100101 Firefox/67.0",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.leafly.com/explore/sort-alpha",
})

re = session.get("https://www.leafly.com/explore/sort-alpha")

# f = open("1.txt", "w+")

# f.write(re.text)

# f.close()

fetching = True
page = 0

def get_data(url):
    req = session.get(url)
    
    data = req.json()

    return data

def get_pyquery(strain):
    url = "https://www.leafly.com/{}/{}".format(strain["Category"], strain["UrlName"])
    print("GET {}".format(url))
    return pq(url.lower())

def get_aromas(d):
    flavors = d(".flavor-name")
    
    result = []
    for flavor in flavors:
        result.append(flavor.text[3:])

    return result

def get_items(arr):
    items = []

    for item in arr:
        items.append(item.text)

    return items

def get_mental(d):
    mentals = d("#effects-tab-content .histogram-label")

    return get_items(mentals)

def get_physical(d):
    phys = d("#medical-tab-content .histogram-label")

    return get_items(phys)

def get_negative(d):
    ne = d("#negatives-tab-content .histogram-label")

    return get_items(ne)

def strain_to_row(strain):
    """
    turn a strain dict into a csv compatible row
    """
    row = []
    print("Processing row")
    d = None
    if "UrlName" in strain and "Category" in strain:
        d = get_pyquery(strain)
    else:
        return [""]*20

    # Strain name
    if "Name" in strain:
        row.append(strain[u"Name"])
    else:
        row.append("")

    # Strain type
    if "DisplayCategory" in strain:
        row.append(strain[u"DisplayCategory"])
    else:
        row.append("")


    # Mental effects
    tags = get_mental(d)

    if len(tags) < 5:
        fill = 5 - len(tags)

        for i in range(fill):
            tags.append("")
    
    for i in range(5):
        row.append(tags[i])

    # Physical effects
    symptoms = get_physical(d)

    if len(symptoms) < 5:
        fill = 5 - len(symptoms)

        for i in range(fill):
            symptoms.append("")
    
    for i in range(5):
        row.append(symptoms[i])


    # Negative effects
    negative_effects = get_negative(d)

    if len(negative_effects) < 5:
        fill = 5 - len(negative_effects)

        for i in range(fill):
            negative_effects.append("")
    
    for i in range(5):
        row.append(negative_effects[i])

    flavors = []
    try:
        flavors = get_aromas(d)
    except:
        flavors = []
        
        
    # Flavors
    if len(flavors) < 3:
        fill = 3 - len(flavors)

        for i in range(fill):
            flavors.append("")
    
    for i in range(3):
        row.append(flavors[i])

    return row

csv_data = [["Strain", "Type", "MentalEffect1","MentalEffect2","MentalEffect3","MentalEffect4","MentalEffect5", "PhysicalEffect1","PhysicalEffect2","PhysicalEffect3","PhysicalEffect4","PhysicalEffect5","NegativeEffect1","NegativeEffect2","NegativeEffect3","NegativeEffect4","NegativeEffect5", "Aroma1", "Aroma2","Aroma3",]]

while  fetching:
    url = ENDPOINT

    if page == 0:
        url = FIRST
    else:
        url = url.format(page)

    data = get_data(url)

    print("Page {}".format(page))

    for strain in data[u"Model"][u"Strains"]:
        row = strain_to_row(strain)
        csv_data.append(row)

    page += 1
    fetching = data["Model"][u"PagingContext"][u"HasNextPage"]

with open("data.csv", "w+") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

csv_file.close()
