import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# Read the input file
input_df = pd.read_excel('/home/vaiii/Downloads/20211030 Test Assignment-20250107T165015Z-001/20211030 Test Assignment/Input.xlsx')

# Iterate through each row of the DataFrame
for index, row in input_df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']  # Fetching the URL_ID to use as the file name
    
    # Send a GET request to the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch URL {url}. Error: {e}")
        continue  # Skip to the next iteration if the URL fetch fails
    
    # Parse the content of the request with BeautifulSoup
    soup1 = BeautifulSoup(response.text, 'html.parser')
    
    web_data = {}
    
    # Extract Title
    try:
        title = soup1.find('h1', class_="entry-title").get_text()
        web_data["Title"] = title
    except AttributeError:
        print(f"Title not found for URL {url}")
        continue
    
    # Parse the main content
    soup = soup1.find('div', class_="td-post-content tagdiv-type")
    if not soup:
        print(f"Main content not found for URL {url}")
        continue
    # Extract key-value pairs from the "Client Background" section
    
    # Initialize client_background as an empty dictionary
    client_background = {}

    try:
        # Find the "Client Background" section and its content

        client_bg_section = soup.find("h1", string="Client Background")
        print('objective_section')
        if client_bg_section:
            client_bg_section = soup.find("h1", string="Client Background").find_next_siblings()
            if client_bg_section:    
                for sibling in client_bg_section:
                    if sibling.name == "h1":
                        break
                    if sibling.name == "p":
                        text = sibling.get_text(strip=True)
                        try:
                            key, value = text.split(":", 1)  # Split only at the first colon
                            client_background[key.strip()] = value.strip()
                        except ValueError:
                            # If no colon found, skip this entry
                            print(f"Skipping invalobjective_headerid entry (no colon): {text}")
                            continue  # Skip this entry
                web_data["Client Background"] = client_background
        else:
            objective_header = soup.find("h3", string=re.compile("Objective", re.IGNORECASE))
        
            if objective_header:
                objective_content = []
                
                # Iterate through all siblings until the next <h3> tag
                for sibling in objective_header.find_next_siblings():
                    if sibling.name == "h3":  # Stop when another h3 appears
                        break
                    if sibling.name in ["p", "li"]:  # Add paragraphs and list items
                        objective_content.append(sibling.get_text(strip=True))
                    elif sibling.name in ["ol", "ul"]:  # Extract all list items inside ordered/unordered lists
                        for li in sibling.find_all("li"):
                            objective_content.append(li.get_text(strip=True))
                web_data["objective_content"] = objective_content   
            else:
                print("Objective section not found.")

    except Exception as e:
        print(f"An error occurred: {e}")



    # Extract various sections
    #client_background = {}
    # try:
    #     client_bg_section = soup.find("h1", string="Client Background").find_next_siblings()
    #     for sibling in client_bg_section:
    #         if sibling.name == "h1":
    #             break
    # # Export the web_data to a JSON file with the name based on URL_ID
    # output_file = f"Scrap/{url_id}.json"
    # with open(output_file, 'w', encoding='utf-8') as json_file:
    #     json.dump(web_data, json_file, indent=4, ensure_ascii=False)

    # print(f"Data for URL_ID {url_id} saved successfully.")

    #         if sibling.name == "p":
    #             key, value = sibling.get_text(strip=True).split(":")
    #             client_background[key.strip()] = value.strip()
    #     web_data["Client Background"] = client_background
    # except AttributeError:
    #     web_data["Client Background"] = {}


    try:
        problem_section = soup.find("h1", string="The Problem")
        if problem_section:
            problem_section = soup.find("h1", string="The Problem").find_next("p").get_text()
            web_data["The Problem"] = problem_section.strip()
            
    except AttributeError:
        web_data["The Problem"] = ""

    try:
        solution_section = soup.find("h1", string="Our Solution")
        if solution_section:
            solution_section = soup.find("h1", string="Our Solution").find_next_sibling("p").get_text()
            web_data["Our Solution"] = solution_section.strip()
    except AttributeError:
        web_data["Our Solution"] = ""

    try:
        solution_architecture = soup.find("h1", string="Solution Architecture")
        if solution_architecture:
            solution_architecture = soup.find("h1", string="Solution Architecture").find_next("div").get_text()
            web_data["Solution Architecture"] = solution_architecture.strip()
        
    except AttributeError:
        web_data["Solution Architecture"] = ""

    try:
        deliverables = []
        deliverable_section = soup.find("h1", string="Deliverables")
        if deliverable_section:
            deliverable_section = soup.find("h1", string="Deliverables").find_next_siblings()
            for item in deliverable_section:
                if item.name == "h1":
                    break
                if item.name == "p":
                    deliverables.append(item.get_text().strip())
            web_data["Deliverables"] = deliverables
    except AttributeError:
        web_data["Deliverables"] = []

    try:
        tech_stack = {}
        tech_stack_section = soup.find("h1", string="Tech Stack")
        if tech_stack_section:
            tech_stack_section = soup.find("h1", string="Tech Stack").find_next("ul")
            categories = tech_stack_section.find_all("li", recursive=False)
            for category in categories:
                sub_heading = category.find("strong")
                if sub_heading:
                    key = sub_heading.get_text().strip()
                    tech_stack[key] = []
                else:
                    tech_stack[key].append(category.get_text().strip())
            web_data["Tech Stack"] = tech_stack
    except AttributeError:
        web_data["Tech Stack"] = {}

    try:
        snapshots = []
        snapshot_section = soup.find("h1", string=re.compile("Project Snapshots", re.IGNORECASE))
        if snapshot_section:
            snapshot_section = soup.find("h1", string=re.compile("Project Snapshots", re.IGNORECASE)).find_next_siblings()
            last_key = ''
            snapshot_dict = {}
            for item in snapshot_section:
                if item.name == "h1":
                    break
                if item.name == "ol":
                    li_items = item.find("li").get_text().strip()
                    last_key = li_items
                    snapshot_dict[last_key] = []
                if item.name == "figure":
                    img_tag = item.find("img")
                    if img_tag and "src" in img_tag.attrs:
                        image_url = img_tag["src"]
                        snapshot_dict[last_key] = [image_url]
            web_data["Project Snapshots"] = snapshot_dict
    except AttributeError:
        web_data["Project Snapshots"] = {}

    try:
        project_website_url = soup.find("h1", string="Project website url")
        if project_website_url:
            project_website_url = soup.find("h1", string="Project website url").find_next("a").get_text()
            web_data["Project website url"] = project_website_url
        
    except AttributeError:
        web_data["Project website url"] = ""

    try:
        summarize_text = []
        summarize_section = soup.find("h1", string="Summarize")
        if summarize_section:
            summarize_section = soup.find("h1", string="Summarize").find_next_siblings()          
            for item in summarize_section:
                if item.name == "h1":
                    break
                if item.name == "p":
                    summarize_text.append(item.get_text(strip=True))
            web_data["Summarize"] = " ".join(summarize_text)
    except AttributeError:
        web_data["Summarize"] = ""

    try:
        contact_details = []
        contact_section = soup.find("h1", string="Contact Details")
        if contact_section:
            contact_section = soup.find("h1", string="Contact Details").find_next_siblings()
            for item in contact_section:
                if item.name == "h1":
                    break
                if item.name == "p":
                    contact_details.append(item.get_text(strip=True))
            web_data["Contact Details"] = contact_details
    except AttributeError:
        web_data["Contact Details"] = []
    
    

    # Export the web_data to a JSON file with the name based on URL_ID
    output_file = f"Scrap/{url_id}.json"
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(web_data, json_file, indent=4, ensure_ascii=False)

    print(f"Data for URL_ID {url_id} saved successfully.")
