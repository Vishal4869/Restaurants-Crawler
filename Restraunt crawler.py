from bs4 import BeautifulSoup
import requests
import PySimpleGUI as sg
import json


page=0

def restaurant_info(url):
    # print('==='+count+'===')
    r = requests.get(url)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    # Get Title
    try:
        htitle = soup.find("h1").text
        print("Restaurant Name: " + htitle)
    except:
        htitle = '-'
        print("Restaurant Name: " + htitle)

    # Get Ratings
    try:
        ratings = soup.find("div", {"class": lambda value: value and value.startswith("i-stars")}).get('aria-label')
        # rating = ratings[0].split()
        # rating=rating[0]
        print("Rating: " + ratings)
    except:
        ratings = '-'
        print("Rating: " + ratings)

    # Get Website
    try:
        website = soup.find(lambda tag: tag.name == "p" and "Business website" in tag.text).nextSibling.text
        print("Website: " + website)
    except:
        print("Website: " + '-')

    # Get Contact No
    try:
        contact_no = soup.find(lambda tag: tag.name == "p" and "Phone number" in tag.text).nextSibling.text
        print("Contact_no: " + contact_no)
    except:
        contact_no = '-'
        print("Contact_no: " + contact_no)

    # Get Address
    try:
        address = soup.find(lambda tag: tag.name == "p" and "Get Directions" in tag.text).nextSibling.text
        print("Address: " + address)
    except:
        address = '-'
        print("Address: " + address)

        # Get Timing
    try:
        hours_table = soup.find("table", {"class": lambda value: value and value.startswith("hours-table")})
        time = hours_table.select("p")
        timings = []
        for i in range(0, len(time), 2):
            try:
                timings.append(time[i].text + '-' + time[i + 1].text)
            except:
                pass
            i = i + 1

        print("Timings: ")
        print(timings)
    except:
        timings = '-'
        print("Timings: " + '-')

    try:
        dishes = soup.find_all("img", {"class": lambda value: value and value.startswith("dishImageV2")})
        popular_dishesh = []

        for d in dishes:
            popular_dishesh.append(d.get('alt'))

        print("Popular Dishes: ")
        print(popular_dishesh)

    except:
        popular_dishesh = '-'
        print("Popular Dishes: " + '-')

    print('------------------------------------')
    # count= int(count)+1

    dictionary = {
        "Restaurant Name": htitle,
        "Rating": ratings,
        "Website": website,
        "Contact_no": contact_no,
        "Address": address,
        "Timings": timings,
        "Popular Dishes": popular_dishesh
    }
    return dictionary

layout = [  [sg.Text('')],
            [sg.Text("Location: " ), sg.InputText('', key='input_text',size=(60,2))],
            [sg.Text("                                         Use CTRL+V to Paste",text_color='blue' )],

            [
                    sg.Text("Save JSON file at :"),
                    sg.In(size=(45, 1), enable_events=True, key="-FOLDER-"),
                    sg.FolderBrowse(),
                ],
            [sg.Text('')],
            [sg.Text(''),sg.Button("Start",size=(10,2)),sg.Text(''),sg.Exit("Exit",size=(10,2))],
            [sg.Text('')],
            [sg.Output(size=(70, 20), key="-output-")]]


window = sg.Window("Web Crawler For Restaurants",layout,size=(600,560))
while True:
    event, values = window.Read()
    if event == 'Start':
        try:

            req1 = values['input_text']
            folderpath = values['-FOLDER-']
            if req1 == '':
                sg.popup("Enter the Location",text_color='yellow')
                continue
            if folderpath == '':
                sg.popup("Select The folder",text_color='yellow')
                continue
            try:
                while int(page) < 3:
                    url1 = "https://www.yelp.com/search?find_desc=Restaurants&amp;find_loc="+req1+"&amp;start="
                    url = url1 + str(page)
                    r = requests.get(url)
                    htmlContent = r.content
                    soup = BeautifulSoup(htmlContent, 'html.parser')

                    try:
                        mains = soup.find_all("div", {
                            "class": "container__09f24__mpR8_ hoverable__09f24__wQ_on margin-t3__09f24__riq4X margin-b3__09f24__l9v5d padding-t3__09f24__TMrIW padding-r3__09f24__eaF7p padding-b3__09f24__S8R2d padding-l3__09f24__IOjKY border--top__09f24__exYYb border--right__09f24__X7Tln border--bottom__09f24___mg5X border--left__09f24__DMOkM border-color--default__09f24__NPAKY"})
                    except:
                        print('Error in Main Search')
                        # main

                    for main in mains:
                        try:
                            name2 = main.find("h3").a.get('href')
                            name_url = "https://www.yelp.com/" + name2
                            dict = restaurant_info(name_url)
                            # Serializing json
                            json_object = json.dumps(dict, indent=4)

                            # Writing to sample.json
                            with open(folderpath+"/output.json", "a") as outfile:
                                outfile.write(json_object + ',' + '\n')
                        except:
                            print('--')
                    page += 10

            except:
                print("Something Went wrong")


            # req = Request('%s'%req1, headers={'User-Agent': 'Mozilla/5.0'})
            # html_page = urlopen(req).read()
            #
            # soup = BeautifulSoup(html_page, "lxml")
            #
            # links = []
            # for link in soup.findAll('a'):
            #     links.append(link.get('href'))
            #
            # chapter = [k for k in links if 'http://images.mangafreak.net:8080' in k]
            #
            # j = 0
            # for i in chapter:
            #     r = requests.get(i, stream=True)
            #     j = j + 1
            #     k = folderpath+'chapter' + str(j) + '.zip'
            #     with open(k, 'wb') as outfile:
            #         print("Downloading to %s" % k)
            #         outfile.write(r.content)
            # print("Done !!!")
        except:
            sg.popup('Error,Check URL or Folder name', text_color='red')
            continue


    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

window.close()
