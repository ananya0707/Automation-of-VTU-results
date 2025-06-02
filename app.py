from selenium import webdriver
from bs4 import BeautifulSoup
import cv2
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import easyocr
from PIL import Image
import random
from CalculatePercentage import PassPercentageCalculator

reader = easyocr.Reader(['en'])

def solve_captcha():
    text = reader.readtext('temp/output_image.png', detail=0)
    if isinstance(text, list):
        for i in text:
            if len(i) == 6:
                text = i
    return text

def process_image(input_image_path):
    img = Image.open(input_image_path)
    img = img.convert('RGB')
    width, height = img.size
    new_img = Image.new('RGB', (width, height), (255, 255, 255))

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            if r == 0 and g == 0 and b == 0 or r == g == b:
                new_img.putpixel((x, y), (r, g, b))
            else:
                new_img.putpixel((x, y), (255, 255, 255))

    output_image_path = 'temp/output_image.png'
    new_img.save(output_image_path)

def get_df(content):
    soup = BeautifulSoup(content, 'html.parser')
    usn_name = soup.find('table')
    p = usn_name.find_all('td')
    usn = p[1].text.split(':')[-1]
    name = p[3].text.split(':')[-1]

    table = soup.find('div', attrs={'class': "divTableBody"})
    rows = table.find_all('div', class_='divTableRow')

    subjects = []
    for row in rows[1:]:
        cells = row.find_all('div', class_='divTableCell')
        subject_code = cells[0].get_text().strip()
        subject_name = cells[1].get_text().strip()
        internal_marks = cells[2].get_text().strip()
        external_marks = cells[3].get_text().strip()
        total = cells[4].get_text().strip()

        try:
            internal_marks = int(internal_marks)
        except:
            if internal_marks == '':
                internal_marks = 0
        
        try:
            external_marks = int(external_marks)
        except:
            if external_marks == '':
                external_marks = 0

        try:
            total = int(total)
        except:
            if total == '':
                total = 0
    
        result = cells[5].get_text().strip()

        subjects.append({
            'SubCode': subject_code,
            'SubName': subject_name,
            'Internal': internal_marks,
            'External': external_marks,
            'Total': total,
            'Result': result
        })

    columns = ['USN', 'Name']
    for subject in subjects:
        sub_code = subject['SubCode']
        sub_name = subject['SubName']
        columns.append(f"{sub_code}-{sub_name}-Internal")
        columns.append(f"{sub_code}-{sub_name}-External")
        columns.append(f"{sub_code}-{sub_name}-Total")
        columns.append(f"{sub_code}-{sub_name}-Result")
    
    
    student_data = {
        'USN': usn,
        'Name': name
    }
    

    for subject in subjects:
        sub_code = subject['SubCode']
        sub_name = subject['SubName']
        student_data[f"{sub_code}-{sub_name}-Internal"] = subject['Internal']
        student_data[f"{sub_code}-{sub_name}-External"] = subject['External']
        student_data[f"{sub_code}-{sub_name}-Total"] = subject['Total']
        student_data[f"{sub_code}-{sub_name}-Result"] = subject['Result']

    df = pd.DataFrame([student_data], columns=columns)
    return df

all_dfs = []

def generate(usn_list):
    MAX_RETRIES = 5
    error_usn = []

    for usn in usn_list:
        attempt = 0
        success = False
        while not success and attempt < MAX_RETRIES:
            attempt += 1
            try:
                driver.get(link)

            except UnexpectedAlertPresentException:
                driver.get(link)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "lns"))
            )

            driver.save_screenshot('temp/snapshot.png')

            img = cv2.imread("temp/snapshot.png")
            crop_img = img[600:750, 1460:1750]
            cv2.imwrite('temp/cap.png', crop_img)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

            process_image('temp/cap.png')
            captcha = solve_captcha()

            us = driver.find_element(By.NAME, "lns")
            cap = driver.find_element(By.NAME, "captchacode")
            us.send_keys(usn)
            cap.send_keys(captcha)

            try:
                driver.find_element(By.ID, "submit").click()
                if driver.page_source:
                    df = get_df(driver.page_source)
                    all_dfs.append(df)
                    print(usn)
                    success = True

            except TypeError:
                driver.find_element(By.ID, "ok").click()

            except Exception as e:
                if attempt == MAX_RETRIES:
                    error_usn.append(usn)
                    break
                try:
                    driver.find_element(By.ID, "ok").click()
                    time.sleep(2)
                except NoSuchElementException:
                    driver.refresh()

    if error_usn:
        print("Remaining USN's: ", error_usn)
        generate(error_usn)


link = "https://results.vtu.ac.in/JJEcbcs24/index.php"

# Input for Branch and USNs
college = input("Enter the college code\n").upper()
year = input('Enter the year\n')
branch = input('Please enter the branch\n').upper()
low = int(input('Enter starting USN\n'))
high = int(input('Enter last USN\n'))


usn_list = []

for i in range(low, high + 1):
    number = i
    if len(str(i)) == 1:
        number = "00" + str(i)
    elif len(str(i)) == 2:
        number = "0" + str(i)
    else:
        number = str(i)
    usn_list.append(college + year + branch + number)

print(usn_list)

try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    generate(usn_list)
    combined_df = pd.concat(all_dfs, ignore_index=True)
    try:
        f_name = "combined_usn_data.xlsx"
        combined_df.to_excel(f_name, index=False)
    except:
        f_name = f"{college}{year}{branch}usns{random.randint(1,100000)}.xlsx"
        combined_df.to_excel(f_name, index=False)
    
    calculator = PassPercentageCalculator(f_name)
    calculator.load_file()
    calculator.calculate_pass_percentage()
    calculator.save_file(f_name)

    print(f"{f_name} file has been created successfully!")

except:
    combined_df = pd.concat(all_dfs, ignore_index=True)
    try:
        f_name = "combined_usn_data.xlsx"
        combined_df.to_excel(f_name, index=False)
    except:
        f_name = f"{college}{year}{branch}usns{random.randint(1,100000)}.xlsx"
        combined_df.to_excel(f_name, index=False)
    
    calculator = PassPercentageCalculator(f_name)
    calculator.load_file()
    calculator.calculate_pass_percentage()
    calculator.save_file()
    print(f"{f_name} file has been created successfully!")