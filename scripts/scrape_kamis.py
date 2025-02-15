import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_kamis(url, filename):
    """Scrape market data from KAMIS and save it to a CSV file."""
    # Ensure the directory exists
    os.makedirs('Data/Products', exist_ok=True)
    
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            rows.append(row_data)
        
        file_path = os.path.join('Data/Products', filename)
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write headers
            writer.writerows(rows)    # Write data rows
        
        print(f'Data has been written to {file_path}')
    else:
        print('No table found on the webpage.')
