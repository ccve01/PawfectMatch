import requests
import pandas as pd

ANIMAL_TYPES_LIST = [None, 'Dog', 'Cat', 'Rabbit', 'Small-Furry', 'Horse',
                     'Bird', 'Scales-Fins-Other', 'Barnyard']
ANIMAL_GENDERS_LIST = [None, 'Male', 'Female']
ANIMAL_AGE_LIST = [None, 'Baby', 'Young', 'Adult', 'Senior']
ANIMAL_SIZE_LIST = [None, 'Small', 'Medium', 'Large', 'Xlarge']
YES_NO_OPTION = ['No', 'Yes']

API_key = 'OXmcV0LKuvPuDmXXVJFb7nsl5O0djD5SbPbWk0yU4yMbIsxRHH'
API_secret = 'TxgjuRnIIKKzn7tbVrtMw3PkObM4S7ESYNUJak0i'

def get_token(API_key, API_secret):
    response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': API_key,
        'client_secret': API_secret,
    })  
    return response.json()['access_token']


def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'


def get_request(access_token, BASE_url):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    response = requests.get(BASE_url, headers=headers)
    return response


def convert_to_json(response):
    return response.json()

def parse_animals(animals_json):
    animalsdf = pd.DataFrame()
    animals_dict = {}
    count = 0

    for animal in animals_json["animals"]:
        animals_dict[count] = {
            'id': animal["id"],
            'type': animal["type"],
            'breed(primary)': animal["breeds"]["primary"],
            'color(primary)': animal["colors"]["primary"],
            'age': animal["age"],
            'gender': animal["gender"],
            'size': animal["size"],
            'coat': animal["coat"],
            'name': animal["name"],
            'description': animal["description"],
            'status': animal["status"],
            'published_at': animal["published_at"],
            'contact(email)': animal["contact"]["email"],
            'contact(phone)': animal["contact"]["phone"],
        }

        address_text = ""
        for line in animal["contact"]["address"].values():
            if (line is not None):
                address_text += line + " "
        animals_dict[count]['contact(address)'] = address_text

        try:
            photomedium = animal["primary_photo_cropped"]["medium"]
            animals_dict[count]['photos'] = photomedium
            animals_dict[count]['video'] = animal['videos'][0]["embed"]
        except TypeError:
            animals_dict[count]['photos'] = None
        except IndexError:
            animals_dict[count]['video'] = None

        count += 1

    animalsdf = pd.DataFrame.from_dict(animals_dict,
                                       orient='index')
    return animalsdf

def valid_input(user_response, valid_types_list):
    for valid_type in valid_types_list:
        if (user_response == valid_type):
            return True
    return False

def print_header(title):
    print(f'\n{title}')
    print('-' * len(title))

def menu(menu_list):
    print_header('Menu')
    for index, name in enumerate(menu_list):
        try:
            lastindex = name.rfind('-')
            if(lastindex > 0):
                name = name[:lastindex] + ' & ' + name[lastindex+1:]
                name = name.replace('-', ', ')
        except AttributeError:
            pass
        print(f'({index}) {name}')

def handle_option(option):
    try:
        return int(option)
    except ValueError:
        return -1

def build_url(dict_inputs):
    url = "https://api.petfinder.com/v2/animals?"
    no_preference = True
    for key, value in dict_inputs.items():
        if value is not None:
            no_preference = False
            url += f'{key}={value}&'
    url = url[:-1]

    if no_preference:
        return 'https://api.petfinder.com/v2/animals'
    else:
        return url


def loop_input_menu(menu_options, request_msg, min_menu_op=0):
    menu(menu_options)
    option = handle_option(input(request_msg))

    while(not valid_input(option, range(min_menu_op, len(menu_options)))):
        menu(menu_options)
        option = handle_option(input(request_msg))

    return option

def user_input():
    dict_inputs = {}

    print_header('Available Animals For Adoption')
    option = loop_input_menu(ANIMAL_TYPES_LIST,
                             'Animal preference: ')
    dict_inputs['type'] = ANIMAL_TYPES_LIST[option]

    print_header('Gender options')
    option = loop_input_menu(ANIMAL_GENDERS_LIST,
                             'Gender preference: ')
    dict_inputs['gender'] = ANIMAL_GENDERS_LIST[option]

    print_header('Age Ranges')
    option = loop_input_menu(ANIMAL_AGE_LIST,
                             'Age preference: ')
    dict_inputs['age'] = ANIMAL_AGE_LIST[option]

    print_header('Animal Size')
    option = loop_input_menu(ANIMAL_SIZE_LIST,
                             'Size preference: ')
    dict_inputs['size'] = ANIMAL_SIZE_LIST[option]

    print_header('Would you like to give a location')
    option = loop_input_menu(YES_NO_OPTION, 'Choice: ')
    if option == 1:
        test = True
        error = ('https://www.petfinder.com/developers/v2/docs/errors/' +
                 'ERR-00002/')
        option = input('Enter your postal code: ')
        while(test):
            response = get_request(get_token(API_key, API_secret),
                                   'https://api.petfinder.com/v2/animals'
                                   + '?location=' + option)
            code = convert_to_json(response)
            try:
                if code['type'] != error:
                    print(code['type'])
                    test = False
            except KeyError:
                break
            option = input('Input valid postal code: ')
        dict_inputs['location'] = option

        print_header('Edit Search Range? (Default 100 miles)')
        option = loop_input_menu(YES_NO_OPTION, 'Choice: ')

        if option == 1:
            print_header('Search range in miles(max 500 miles): ')
            option = handle_option(input('Range in miles(max 500 miles): '))
            while(not valid_input(option, range(1, 501))):
                option = handle_option(input('Range in miles' +
                                             '(max 500 miles): '))
            dict_inputs['distance'] = option

    print_header('Would you like to edit the number of results? (default:20)')
    option = loop_input_menu(YES_NO_OPTION, 'Choice: ')

    if option == 1:
        print_header('Enter max number of search results you would like' +
                     '(max 100): ')
        option = handle_option(input('Number of returned search' +
                                     'results(max 100): '))
        while(not valid_input(option, range(1, 101))):
            option = handle_option(input('Number of returned search' +
                                         'results(max 100): '))
        dict_inputs['limit'] = option

    return dict_inputs


def display_profile(dataSeries, paramList=None, labelList=None, formList=None):
    if (paramList is None):
        paramList = dataSeries.keys().to_list()

    if (formList is None):
        formList = []
    formList = formList + ("\n " * (len(paramList)-len(formList))).split(" ")

    if (labelList is None):
        labelList = paramList.copy()
        for i in range(0, len(paramList)):
            labelList[i] = labelList[i] + ": "
    elif len(labelList) < len(paramList):
        while (len(labelList) < len(paramList)):
            labelList.append(paramList[len(labelList)] + ": ")

    # Print based on specified parameters
    for i in range(0, len(paramList)):
        if labelList[i] is not None:
            print(f'{labelList[i]}', end='')
        print(f'{dataSeries.get(paramList[i])}', end=formList[i])


def display_selected_animals(animalsdf):
    for index, animal in animalsdf.iterrows():
        print('({})'.format(index+1), end="\t")
        display_profile(animal,
                        paramList=["type", "age", "gender", "name"],
                        labelList=[None, None, None, "Name: "],
                        formList=["\t", " ", "\t", "\n"])


# Gets dataframe with animals that may be selected
def user_select_animals(animalsdf):
    print("Based on your search criteria this is what we could find: \n")
    option = len(animalsdf)
    if (option == 0):
        print("_NONE_\nNo pets in the area based on your criteria")

    while(not (option == 0)):
        print_header(" List of Animals Found ")
        display_selected_animals(animalsdf)
        print(f'(0) Exit selection')

        option = handle_option(input("Select an animal:"))
        while(not valid_input(option, range(0, len(animalsdf)+1))):
            option = handle_option(input("Select an animal:"))
        if option == 0:
            return

        # Full animal profile display
        print_header("     Full Animal Profile     ")
        display_profile(animalsdf.iloc[option-1],
                        paramList=["id", "name", "type", "age", "gender",
                                   "size",
                                   "color(primary)", "breed", "coat",
                                   "status",
                                   "photos", "video",
                                   "description",
                                   "contact(address)",
                                   "contact(email)", "contact(phone)",
                                   "published_at"],
                        labelList=["ID:_", "Name: ", "Type: ", "(", "~ ",
                                   "~ ",
                                   "~ ", "Breed: ", "Coat: ",
                                   "Adoption Status: ",
                                   "Photo Link: ", "Video Link: ",
                                   "Description:\n",
                                   "_Contact Information_\nAddress: ",
                                   "Email: ", "Phone: ",
                                   "Published on site at: "],
                        formList=["_\n", "\n", " ", " ", " ",
                                  " ",
                                  ")\n", "\n", "\n",
                                  "\n\n",
                                  "\n", "\n\n",
                                  "\n\n",
                                  "\n",
                                  "\n", "\n\n",
                                  ""])
        print_header("                             ")
        input("Press Enter to return to Select Screen: ")


if __name__ == '__main__':
    AUTH_URL = 'https://api.petfinder.com/v2/oauth2/token'
    token = get_token(API_key, API_secret)

    # Process user request for animals
    output = user_input()
    url = build_url(output)
    response = get_request(token, url)
    animalsdf = parse_animals(convert_to_json(response))

    # Terminal visulaization of animals
    user_select_animals(animalsdf)
