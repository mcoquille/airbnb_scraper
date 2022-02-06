from time import sleep
from lib import scraping

BASE_URL = "https://www.airbnb.co.uk"
BASE_ROOM_URL = BASE_URL + "/rooms/"

def get_room_url(room_id):
    return BASE_ROOM_URL + room_id

def get_property_name(soup):
    name_html = soup.find('h1', class_='_fecoyn4')
    if name_html:
        name = name_html.get_text()
        if name:
            return name
        else:
            raise ValueError("HTML of property name has no text.")
    else:
        raise ValueError("Couldn't find the HTML of the property name.")

def get_property_type(soup):
    type_html = soup.find('div', class_='_1qsawv5')
    if type_html:
        type_ = type_html.get_text()
        if type_:
            try:
                splitted_type = type_.split(' hosted by')
            except:
                raise ValueError("String doesn't contain ' hosted by'.")
            cleaned_type = splitted_type[0]
            return cleaned_type

        else:
            raise ValueError("HTML of property type has no text.")
    else:
        raise ValueError("Couldn't find the HTML of the property type.")

def get_core_features(soup):
    features_block = soup.find('ol', class_='_194e2vt2')
    if features_block:
        features_html = features_block.find_all('span')
        if features_html:
            features = [f.get_text() for f in features_html]
            cleaned_features = [f for f in features if f != ' · ']
            return cleaned_features
        else:
            raise ValueError("Couldn't find the HTML of the features")
    else:
        raise ValueError("Couldn't find the HTML of the features_block.")

def map_core_features(features):
    dct_features = {}
    for f in features:
        try:
            num, name = f.split()
        except:
            raise ValueError("The string isn't two elements separated by a space.")
        if not name.endswith('s'):
            name += 's'
        try:
            num = int(num)
        except:
            raise ValueError("The supposed number cannot be changed into an integer.")
        dct_features[name] = num
    return dct_features

def find_url_to_show_amenities(soup):
    url_html = soup.find('a', class_='b1sec48q v7aged4 dir dir-ltr')
    if url_html:
        url = url_html.attrs['href']
        url = BASE_URL + url
        return url
    else:
        raise ValueError("Couldn't find the HTML of the amenities link")

def get_amenities(soup):
    amenities_html = soup.find_all('div', class_='_gw4xx4')
    if amenities_html:
        amenities = [a.get_text() for a in amenities_html]
        cleaned_amenities = [a for a in amenities if 'Unavailable' not in a]
        return cleaned_amenities
    else:
        raise ValueError("Couldn't find the HTML of the amenities.")

def scrape_room(driver, room_id):

    # Initiate room
    room = {}

    room_url = get_room_url(room_id)
    driver.get(room_url)
    # We wait 2 seconds for all elements to be rendered
    sleep(2)
    soup = scraping.get_soup_from_driver(driver)

    # We are not allowed to go to this URL
    if 'status code 403' in soup.get_text():
        return False

    # PROPERTY NAMME
    room['name'] = get_property_name(soup)
    # PROPERTY TYPE
    room['type_'] = get_property_type(soup)

    features = get_core_features(soup)
    features_map = map_core_features(features)
    # NUMBER OF BEDROOMS
    room['num_of_bedrooms'] = features_map['bedrooms']
    # NUMBER OF BATHROOMS
    room['num_of_bathrooms'] = features_map['bathrooms']

    amenities_url = find_url_to_show_amenities(soup)
    driver.get(amenities_url)
    # We wait 2 seconds for all elements to be rendered
    sleep(2)
    amenities_soup = scraping.get_soup_from_driver(driver)
    # LIST OF AMENITIES
    room['amenities'] = get_amenities(amenities_soup)

    return room
