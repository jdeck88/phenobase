import requests
import csv
from utilities import get_authorization_headers

def write_observations(authorization_headers, observations_url):
    
    page = 1
    has_more_pages = True

    with open("budburst.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['observation_id', 'latitude', 'longitude', 'observation_date', 'scientific_name', 'phenophase_id', 'plant_group_id', 'add_date', 'modified_date', 'site_species_id', 'report_id', 'is_youth_observation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header row
        writer.writeheader()

        while has_more_pages:
            params = {
                'report_type': 'phenophase',
                'per_page': 1000,  # 1000 is max per page
                'page': page,
                #'created_after': '2023-12-01',
            }

            response = requests.get(observations_url, params=params, headers=authorization_headers)
            data = response.json()

            # Check if there are more pages
            has_more_pages = page <= response.json()['meta']['last_page']
            last_page = response.json()['meta']['last_page']

            # Process the current page
            for observation in data['data']:
                writer.writerow(observation)
                
            print(f"Writing page {page} of {last_page} to CSV...")

            # Update page number for the next iteration
            page += 1
            
             # Break the loop if there are no more pages
            if not has_more_pages:
                break
            


authorization_headers = get_authorization_headers()
observations_url = 'https://budburst.org/api/observations'

write_observations(authorization_headers, observations_url)
       