from math import sin, cos, acos, pi


def dms2dd(d, m, s):
    """Converts an angle in "degrees minutes seconds" to "decimal degrees"
    """
    return d + m/60 + s/3600


def dd2dms(dd):
    """Converts an angle in "decimal degrees" to "degrees minutes seconds"
    """
    d = int(dd)
    x = (dd-d)*60
    m = int(x)
    s = (x-m)*60
    return d, m, s


def deg2rad(dd):
    """Converts an angle in "decimal degrees" to radians
    """
    return dd/180*pi


def rad2deg(rd):
    """Converts an angle in radians to "decimal degrees"
    """
    return rd/pi*180


def distanceGPS(latA, longA, latB, longB):
    """Returns the distance in meters between two points A and B known by
       their GPS coordinates (in radians).
    """
    # Radius of the Earth in meters (IAG-GRS80 sphere)
    RT = 6378137
    # Angle in radians between the two points
    S = acos(sin(latA)*sin(latB) + cos(latA)*cos(latB)*cos(abs(longB-longA)))
    # Distance between the two points, measured on a great circle arc
    return S*RT/1000

# Function to calculate and display the distance between two cities
def calculate_distance(data, city_name1, city_name2):
    city1_data = next((item for item in data if item['CapitalName'] == city_name1), None)
    city2_data = next((item for item in data if item['CapitalName'] == city_name2), None)

    if city1_data is None or city2_data is None:
        print("One or both of the specified cities are not present in the data.")
    else:
        lat1 = deg2rad(city1_data['CapitalLatitude'])
        lon1 = deg2rad(city1_data['CapitalLongitude'])
        lat2 = deg2rad(city2_data['CapitalLatitude'])
        lon2 = deg2rad(city2_data['CapitalLongitude'])

        distance_km = distanceGPS(lat1, lon1, lat2, lon2)
        print(f"Distance between {city_name1} and {city_name2}: {distance_km:.2f} kilometers")

# Load data from the text file
def load_data_from_text(file_path):
    """
    Loads city data from a text file and returns a list of dictionaries.
    Each dictionary contains information about a city.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Ignore empty lines
                parts = line.split(',')
                if len(parts) == 6:
                    data.append({
                        'CountryName': parts[0],
                        'CapitalName': parts[1],
                        'CapitalLatitude': float(parts[2]),
                        'CapitalLongitude': float(parts[3]),
                        'CountryCode': parts[4],
                        'ContinentName': parts[5]
                    })
    return data

# Function to find the capital name of a country based on the country's name
def find_capital_by_country(data, country_name):
    """
    Finds the capital name of a country based on the country's name.
    Returns the capital name or None if the country is not found.
    """
    country_data = next((item for item in data if item['CountryName'] == country_name), None)
    if country_data:
        return country_data['CapitalName']
    else:
        return None
    
def search_by_continent(data, continent_name):
    matching_entries = []

    for item in data:
        if item['ContinentName'].lower() == continent_name.lower():
            matching_entries.append(item)

    return matching_entries

def find_closest_capital(data, city_name):
    city_data = next((item for item in data if item['CapitalName'] == city_name), None)

    if city_data is None:
        return None

    lat1 = deg2rad(city_data['CapitalLatitude'])
    lon1 = deg2rad(city_data['CapitalLongitude'])

    closest_distance = float('inf')
    closest_capital = None

    for item in data:
        if item['CapitalName'] != city_name:
            lat2 = deg2rad(item['CapitalLatitude'])
            lon2 = deg2rad(item['CapitalLongitude'])

            distance_km = distanceGPS(lat1, lon1, lat2, lon2)

            if distance_km < closest_distance:
                closest_distance = distance_km
                closest_capital = item['CapitalName']

    return closest_capital, closest_distance




# Function to find and display the capital of a country
def find_and_display_capital(data, country_name):
    capital_name = find_capital_by_country(data, country_name)
    if capital_name:
        print(f"The capital of {country_name} is {capital_name}.")
    else:
        print(f"The capital of {country_name} is not found in the data.")

if __name__ == "__main__":
    data = load_data_from_text('capitale.txt')

    while True:
        print("\nMenu:")
        print("1. Calculate distance between two capitals")
        print("2. Find closest capital to an otherone")
        print("3. Search for countries or capitals by continent")
        print("4. Find the capital of a country")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            city1 = input("Enter the name of the first capital: ")
            city2 = input("Enter the name of the second capital: ")
            calculate_distance(data, city1, city2)
            

        elif choice == '2':
            city_name = input("Enter the name of the capital: ")
            closest_capital, distance = find_closest_capital(data, city_name)
            if closest_capital is not None:
                print(f"The closest capital to {city_name} is {closest_capital} at a distance of {distance} kilometers.")
            else:
                print("The specified city is not in the data.")
        elif choice == '3':
            continent_name = input("Enter the name of the continent: ")
            matching_entries = search_by_continent(data, continent_name)
            if matching_entries:
                print(f"Matching entries in {continent_name}:")
                for item in matching_entries:
                    print(f"Country: {item['CountryName']}, Capital: {item['CapitalName']}")
            else:
                print(f"No entries found for {continent_name}.")
        elif choice == '4':
            country_name = input("Enter the name of the country: ")
            capital = find_capital_by_country(data, country_name)
            if capital is not None:
                print(f"The capital of {country_name} is {capital}.")
            else:
                print(f"Country {country_name} not found in the data.")
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2/3/4/5).")