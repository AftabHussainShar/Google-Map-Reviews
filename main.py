import os
import pickle
import undetected_chromedriver as uc
from selenium import webdriver as webdriver12 
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def main(url_location, review_text_location, rating_value):
    # proxy = 'geo.iproyal.com:12321:zv06uqa6KwM6oH4l:Diego1409200610_country-es_city-barcelona'
    # proxy_parts = proxy.split(":")
    
    if file_location_entry.get() == '':
        messagebox.showinfo('Error', 'Please select URL file location first!')
        return 
    if file_location_entry2.get() == '':
        messagebox.showinfo('Error', 'Please select reviews text file location first!')
        return 
    if rating_entry.get() == '':
        messagebox.showinfo('Error', 'Please select enter a rating value!')
        return
    if rating_entry.get().isdigit() == False:
        messagebox.showinfo('Error', 'Rating value must be a number')
        return
    if rating_entry.get() < '1' or rating_entry.get() > '5':
        messagebox.showinfo('Error', 'Rating value can only be from 1-5')
        return

    
    
    # if os.path.exists("cookies.pkl") == False:
        
    fileopen = open('credentials.txt','r')
    data = fileopen.read()
    fileopen.close()
    data = data.split('\n')
    data.reverse()
    for creds in data:
        updated_data = creds.split(',')
    
    email = updated_data[0]
    password = updated_data[1]
    print(email)
    print(password)
    

    options = webdriver12.ChromeOptions()
    #options.add_argument('proxy-server=106.122.8.54:3128')
    #options.add_argument(r'--user-data-dir=C:\Users\suppo\AppData\Local\Google\Chrome\User Data\Default')
    # options.add_argument('--proxy-server=http://{}:{}@{}'.format(proxy_parts[2], proxy_parts[3], proxy_parts[0]))

    browser = uc.Chrome()
    browser.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    browser.find_element(By.ID, 'identifierId').send_keys(email)

    browser.find_element(
        By.CSS_SELECTOR, '#identifierNext > div > button > span').click()

    password_selector = "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

    browser.find_element(
        By.CSS_SELECTOR, password_selector).send_keys(password)

    browser.find_element(
        By.CSS_SELECTOR, '#passwordNext > div > button > span').click()

    time.sleep(5)
    browser.get('https://www.google.com/')

    cookies = browser.get_cookies()

    pickle.dump(cookies, open("cookies.pkl", "wb"))    

    browser.quit()
        
    options = {
        'proxy': {
            'http': 'http://zv06uqa6KwM6oH4l:Diego1409200610_country-es_city-barcelona@geo.iproyal.com:12321',
            # 'https': 'http://username:password@geo.iproyal.com:12321',
        }
    }

    driver = webdriver.Chrome(seleniumwire_options=options)
    driver.maximize_window()
    driver.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    cookies = pickle.load(open("cookies.pkl", "rb"))

    
    # review_text = "This is a very good place!"
    for cookie in cookies:
        
        cookie['domain'] = ".google.com"
        
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print('cookie not added ',cookie)
            print(e)

    fileopen_urls = open(url_location,'r')
    data = fileopen_urls.read()
    fileopen_urls.close()

    cleaned_urls = data.split('\n')

    fileopen_review_text = open(review_text_location,'r')
    data = fileopen_review_text.read()
    fileopen_review_text.close()

    cleaned_review_texts = data.split('\n')

    for url, review_text in zip(cleaned_urls, cleaned_review_texts):
            
        driver.get(url)
        time.sleep(3)
        pyautogui.click(x=1060, y=958)
        driver.get(url)
        time.sleep(5)

        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]').click()
        time.sleep(5)

        try:
            driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[4]/div/button').click()
            time.sleep(5)
        except:
            driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[5]/div/button').click()
            time.sleep(5)
        
        time.sleep(5)
        x=725
        y=473 # first click
        pyautogui.click(x=x, y=y)
        time.sleep(2)
        if rating_value == '1':
            x=864
            y=457 # rating 1
            pyautogui.click(x=x, y=y)
            
        elif rating_value == '2':
            x=912
            y=457 # rating 2
            pyautogui.click(x=x, y=y)
        elif rating_value == '3':
            x=961
            y=457 # rating 3
            pyautogui.click(x=x, y=y)
        elif rating_value == '4':
            x=1007
            y=457 # rating 4
            pyautogui.click(x=x, y=y)
        elif rating_value == '5':
            x=1056
            y=457 # rating 5
            pyautogui.click(x=x, y=y)

        time.sleep(2)

        pyautogui.click(x=775, y=548) # click in text area of review box

        for text in review_text:
            pyautogui.typewrite(text)

        time.sleep(2)

        pyautogui.click(x=1186, y=807) # click on post button

        time.sleep(4)

    driver.quit()
    
    
def browse_file_location(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)



app = tk.Tk()
app.title("Google Maps Review Bot")
app.configure(background='#f0f0f0')  # Set application background color

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#4CAF50", foreground="white", font=("Arial", 12))  # Increase button text size
style.configure("TEntry", foreground="black", font=("Arial", 12))  # Increase entry text size

# Heading
heading = ttk.Label(app, text="Google Maps Review Bot", font=("Arial", 20, "bold"), background='#f0f0f0')
heading.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# First row
file_location_label = ttk.Label(app, text="URLs File location:", background='#f0f0f0')  # Set label background color
file_location_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

file_location_entry = ttk.Entry(app, width=50)
file_location_entry.grid(row=1, column=1, padx=10, pady=5)

file_location_button = ttk.Button(app, text="Browse", command=lambda: browse_file_location(file_location_entry))
file_location_button.grid(row=1, column=2, padx=10, pady=5)

# Second row
file_location_label2 = ttk.Label(app, text="Reviews File location:", background='#f0f0f0')  # Set label background color
file_location_label2.grid(row=2, column=0, padx=10, pady=5, sticky="e")

file_location_entry2 = ttk.Entry(app, width=50)
file_location_entry2.grid(row=2, column=1, padx=10, pady=5)

file_location_button2 = ttk.Button(app, text="Browse", command=lambda: browse_file_location(file_location_entry2))
file_location_button2.grid(row=2, column=2, padx=10, pady=5)

# Third row
rating_label = ttk.Label(app, text="Rating :", background='#f0f0f0')  # Set label background color
rating_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

rating_entry = ttk.Entry(app, width=10)
rating_entry.grid(row=3, column=1, padx=10, pady=5)

# Start button
start_button = ttk.Button(app, text="Start", command=lambda: main(file_location_entry.get(), file_location_entry2.get(), rating_entry.get()))
start_button.grid(row=4, column=0, columnspan=3, pady=(20, 10))

app.mainloop()

