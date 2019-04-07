
import csv
import requests

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

def strain_to_row(strain):
    """
    turn a strain dict into a csv compatible row
    """
    row = []

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
    if "Tags" in strain:
        tags = [tag[u"DisplayLabel"] for tag in strain[u"Tags"]]
    else:
        tags = []

    if len(tags) < 5:
        fill = 5 - len(tags)

        for i in range(fill):
            tags.append("N/I")
    
    for i in range(5):
        row.append(tags[i])

    # Physical effects
    if "Symptoms" in strain:
        symptoms = [symptom[u"DisplayLabel"] for symptom in strain[u"Symptoms"]]
    else:
        symptoms = []

    if len(symptoms) < 5:
        fill = 5 - len(symptoms)

        for i in range(fill):
            symptoms.append("")
    
    for i in range(5):
        row.append(symptoms[i])


    # Negative effects
    if "NegativeEffects" in strain:
        negative_effects = [ne[u"DisplayLabel"] for ne in strain[u"NegativeEffects"]]
    else:
        negative_effects = []

    if len(negative_effects) < 5:
        fill = 5 - len(negative_effects)

        for i in range(fill):
            negative_effects.append("")
    
    for i in range(5):
        row.append(negative_effects[i])

    # Flavors
    if "Flavors" in strain:
        flavors = [ne[u"DisplayLabel"] for ne in strain[u"Flavors"]]
    else:
        flavors = []

    if len(flavors) < 3:
        fill = 3 - len(flavors)

        for i in range(fill):
            flavors.append("")
    
    for i in range(3):
        row.append(flavors[i])

    return row

csv_data = [["Strain", "Type", "MentalEffect1","MentalEffect2","MentalEffect3","MentalEffect4","MentalEffect5", "PhysicalEffect1","PhysicalEffect2","PhysicalEffect3","PhysicalEffect4","PhysicalEffect5","NegativeEffect1","NegativeEffect2","NegativeEffect3","NegativeEffect4","NegativeEffect5", "Aroma1", "Aroma4","Aroma3",]]

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
