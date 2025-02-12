import requests
from bs4 import BeautifulSoup
import csv

# URL of the KAMIS page
url = 'https://kamis.kilimo.go.ke/site/market?product=1&per_page=50000'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing the data
table = soup.find('table')

if table:
    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        rows.append(row_data)

    # Write data to CSV
    with open('dry_maize.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write data rows

    print('Data has been written to commodity_prices.csv')
else:
    print('No table found on the webpage.')
