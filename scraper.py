from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import time
import csv

class Program:
    def __init__(self, name, joinable, description, avgreward, avgrewardsubtext, maxreward, maxrewardsubtext, safeharbor, soloonly):
        self.name = name
        self.joinable = joinable
        self.description = description
        self.avgreward = avgreward
        self.avgrewardsubtext = avgrewardsubtext
        self.maxreward = maxreward
        self.maxrewardsubtext = maxrewardsubtext
        self.safeharbor = safeharbor
        self.soloonly = soloonly

    def to_json(self):
        program_dict = {
            'name': self.name,
            'joinable': self.joinable,
            'description': self.description,
            'avgreward': self.avgreward,
            'avgrewardsubtext': self.avgrewardsubtext,
            'maxreward': self.maxreward,
            'maxrewardsubtext': self.maxrewardsubtext,
            'safeharbor': self.safeharbor,
            'soloonly': self.soloonly
        }
        return json.dumps(program_dict)
    
    def to_csv(self):
        return [self.name, self.joinable, self.description, self.avgreward, self.avgrewardsubtext, self.maxreward, self.maxrewardsubtext, self.safeharbor, self.soloonly]


# Set up options for the Chrome browser to run in headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-gpu-sandbox')
options.add_argument('--no-sandbox')

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)

# Navigate to the Bugcrowd programs page
driver.get("https://bugcrowd.com/programs?sort[]=promoted-desc")

# Wait for the page to load and the programs to appear
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "bc-panel__title")))

programs = []

while True:

    # Find react data
    react_data = driver.find_element("xpath", "//div[@data-react-class='ProgramSearchApp']")

    react_data_elements = react_data.text.split("Quick view\n")

    for i, element in enumerate(react_data_elements):
        if i == 0:
            element = element.split("Search help\n")
            element = element[1]
        attributes = element.split("\n")
        split_index = 0
        name = attributes[split_index]
        split_index +=1 
        if attributes[split_index] == "Joinable":
            joinable = "true"
            split_index +=1
        else:
            joinable = "false"
        description = attributes[split_index]
        split_index +=1
        if attributes[split_index].find("$") != -1:
            avgreward = attributes[split_index]
            split_index +=1 
            avgrewardsubtext = attributes[split_index]
            split_index +=1
        else:
            avgreward = None
            avgrewardsubtext = None
        if attributes[split_index].find("$") != -1:
            maxreward = attributes[split_index]
            split_index +=1 
            maxrewardsubtext = attributes[split_index]
            split_index +=1
        else:
            avgreward = None
            avgrewardsubtext = None
        if attributes[split_index] == "Safe harbor":
            safeharbor = "true"
            split_index +=1 
        elif attributes[split_index] == "Partial safe harbor":
            safeharbor = "partial"
            split_index +=1 
        else:
            safeharbor = "false"
        if attributes[split_index] == "Solo-Only":
            soloonly = "true"
        else:
            soloonly = "false"
        curr_attribute = Program(name, joinable, description, avgreward, avgrewardsubtext, maxreward, maxrewardsubtext, safeharbor, soloonly)
        if curr_attribute.name != "Pagination":
            programs.append(curr_attribute)
        # print(curr_attribute.to_json())
        # print("next")
    # after all elements, click next
    try:
        next_button = driver.find_element(By.XPATH, "//button[@class='bc-pagination__link' and contains(text(), 'Next')]")
        next_button.click()
        time.sleep(5)  # Wait for page to load
    except NoSuchElementException:
        # Next button no longer exists, so exit the loop
        break

# Close the Chrome driver
driver.quit()

# write to .csv
with open("programs.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Joinable', 'Description', 'Average Reward', 'Average Reward Subtext', 'Max Reward', 'Max Reward Subtext', 'Safe Harbor', 'Solo-Only'])
    # print each program
    for program in programs:
        writer.writerow(program.to_csv())