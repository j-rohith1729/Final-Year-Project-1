from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from datetime import date

# Function to scrape listing elements from Google Flights
def scrape_listings(soup):
    return soup.select('li.pIav2d')

# Function to scrape company name from a flight listing
def scrape_company_name(listing):
    airline_element = listing.select_one('div.Ir0Voe div.sSHqwe')
    return airline_element.text.strip()

# Function to scrape flight duration from a flight listing
def scrape_flight_duration(listing):
    duration_element = listing.select_one('div.AdWm1c.gvkrdb')
    return duration_element.text.strip()

# Function to scrape price from a flight listing
def scrape_price(listing):
    price_element = listing.select_one('div.U3gSDe div.FpEdX span')
    return price_element.text.strip()

# Function to scrape departure and arrival dates from a flight listing
def scrape_departure_arrival_dates(listing):
    departure_date_element = listing.select_one('span.mv1WYe span:first-child [jscontroller="cNtv4b"] span')
    arrival_date_element = listing.select_one('span.mv1WYe span:last-child [jscontroller="cNtv4b"] span')
    return departure_date_element.text.strip(), arrival_date_element.text.strip()

# Function to scrape flight CO2 emission from a flight listing
def scrape_co2_emission(listing):
    co2_element = listing.select_one('div.V1iAHe div.AdWm1c')
    return co2_element.text.strip()

# Function to scrape flight stops from a flight listing
def scrape_flight_stops(listing):
    stops_element = listing.select_one('div.EfT7Ae span.ogfYpf')
    return stops_element.text.strip()

# Main function
def creator(link,days):
    days_left = days
    url = link 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = scrape_listings(soup)

    flight_data = []
    for listing in listings:
        company_name = scrape_company_name(listing)
        flight_duration = scrape_flight_duration(listing)
        price = scrape_price(listing)
        departure_date, arrival_date = scrape_departure_arrival_dates(listing)
        co2_emission = scrape_co2_emission(listing)
        stops = scrape_flight_stops(listing)

        # Store flight information in a dictionary
        flight_info = {
            'company_name': company_name,
            'flight_duration': flight_duration,
            'price': price,
            'departure_date': departure_date,
            'arrival_date': arrival_date,
            'co2_emission': co2_emission,
            'stops': stops,
            'days_left': days_left
        }

        flight_data.append(flight_info)

    # Convert data to a DataFrame
    df = pd.DataFrame(flight_data)
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    filename = date_string + ".csv"
    
    # Check if the CSV file exists
    if os.path.exists(filename):
        # If the file exists, append the data without writing the header
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # If the file doesn't exist, create it and write the data with the header
        df.to_csv(filename, mode='w', header=True, index=False)
    
    print(f"Data appended to {filename} with 'days left' = {days_left}")



def main():
    file_path='links.txt'
    links = []
    with open(file_path, 'r') as file:
        for line in file:
            link = line.strip()  
            if link:  
                links.append(link)
    days=1
    for link in links:
        creator(link,days)
        days=days+1
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    filename = date_string + ".csv"
    df=pd.read_csv(filename)

    df=df[~(df['price']=='Price unavailable')]

    df.reset_index(drop=True, inplace=True)
    # Save the DataFrame with the new index to a CSV file (optional)
    df.to_csv(filename, index=False)
    print("COMPLETED")

    



    

if __name__ == "__main__":
    main()
