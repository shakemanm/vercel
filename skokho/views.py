from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from django.conf import settings
from fake_useragent import UserAgent

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import contextmanager
from selenium.common.exceptions import NoSuchWindowException

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException



from .forms import ContactForm, OptForm

from .models import Client, generate_filename


def take_screenshot(driver, screenshot_name):
    try:
        media_root = settings.MEDIA_ROOT
        screenshot_path = os.path.join(media_root, "screenshots", screenshot_name)

        if not os.path.exists(os.path.dirname(screenshot_path)):
            os.makedirs(os.path.dirname(screenshot_path))

        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")
    except Exception as e:
        print(f"An error occurred while taking a screenshot: {str(e)}")


# Function to inject Zone.js into the webpage
def inject_zone_js(driver):
    zone_js_script = """
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://unpkg.com/zone.js';
        document.head.appendChild(script);
    """
    driver.execute_script(zone_js_script)

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

driver = None


@contextmanager
def initialize():
    global driver
    if driver is None or not driver_is_valid(driver):
        if driver:
            driver.quit()  # Quit the existing driver if it's not valid
        driver = create_new_driver()
    try:
        yield driver
    finally:
        # Clean up resources here if needed
        pass

def driver_is_valid(driver):
    try:
        # Execute a simple command to check if the driver is still responsive
        driver.execute_script("return document.readyState;")
        return True
    except Exception:
        # An exception occurred, indicating that the driver is not valid
        return False





custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.225 Safari/537.36"
def create_new_driver():
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={custom_user_agent}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    new_driver = webdriver.Chrome(options=chrome_options)
   
    
    new_driver.get("https://www.mtn.co.za/business/ebu-prepaid/")
    # ... (configure chrome options if needed)
    
    return new_driver

def driver_is_valid(driver):
    try:
        # Execute a simple command to check if the driver is still responsive
        driver.execute_script("return document.readyState;")
        return True
    except Exception:
        # An exception occurred, indicating that the driver is not valid
        return False





def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def save_to_session(request, key, value):
    request.session[key] = value


def get_from_session(request, key):
    return request.session.get(key)


def Home(request):
    
        return render(request, "main.html")
    
    




def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def find_clickable_element(driver, locator, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            scroll_into_view(driver, element)  # Scroll into view before clicking
            element.click()
            return element
        except ElementClickInterceptedException:
            attempts += 1
            print(f"Attempt {attempts} to click the element failed. Retrying...")
        except TimeoutException:
            attempts += 1
            print(f"Attempt {attempts} to find the element failed. Retrying...")

    raise TimeoutException("Max attempts reached. Element not found.")




    
    
    

def Register(request):
    
    contact_form = ContactForm()
    with initialize() as driver:
        if request.method == "POST":
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                phone_number = contact_form.cleaned_data["phone"]
                save_to_session(request, "phone_number", phone_number)

                try:
                    radio_button_label = find_clickable_element(driver, (By.XPATH, '//label[@for="mtn-radio-3"]'))
                    scroll_into_view(driver, radio_button_label)
                    radio_button_label.click()

                    input_number_field = find_clickable_element(driver, (By.CSS_SELECTOR, ".mtn-input-number_field_container") )
                
                    scroll_into_view(driver, input_number_field)
                    input_number_field.click()
                    
                    agent_code_input = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.CLASS_NAME, "mtn-input-number_control")
                        )
                    )
                    scroll_into_view(driver, agent_code_input)
                    agent_code_input.send_keys("PMG23382")
                    time.sleep(3)
                    element = (
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    "/html/body/mtn-main/mtn-home/div/mtn-agent-info/div/div/div/mtn-card-input/div/mtn-card-input-bottom/button",
                                )
                            )
                        )
                    ).click()

                    phone_number_field = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, ".mtn-input-number_field_container")
                        )
                    )
                    scroll_into_view(driver, phone_number_field)
                    phone_number_field.click()

                    phone_number_inputs = WebDriverWait(driver, 5).until(
                        EC.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "mtn-input-number_control")
                        )
                    )
                    partial_phone_number = phone_number[1:]

                    for index, digit in enumerate(partial_phone_number):
                        phone_number_inputs[index + 1].send_keys(digit)

                    time.sleep(3)

                    element = (
                        WebDriverWait(driver, 10)
                        .until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    "/html/body/mtn-main/mtn-home/div/mtn-sign-up/div/div/div/div/mtn-card-input/div/mtn-card-input-bottom/button",
                                )
                            )
                        )
                        .click()
                    )
                    
                  
                except TimeoutException:
                    return redirect("otp", phone_number=phone_number)

    return render(request, "skokho/register.html", {"contact_form": contact_form})


def Otp(request, phone_number):
    otp_form = OptForm()

    if request.method == "POST":
        otp_form = OptForm(request.POST)
        if otp_form.is_valid():
            otp = otp_form.cleaned_data["otp"]
            phone_number = get_from_session(request, "phone_number")

            # Perform background processing with phone_number and otp
            with initialize() as driver:
                background_processing(phone_number, otp)

            # Clear the session after using the values
            request.session.pop("phone_number", None)

            return redirect("register")

    return render(request, "skokho/otp.html", {"otp_form": otp_form})


def background_processing(phone_number, otp):
    client = Client.objects.first()
    first_name_variable = client.first_name
    client_middle_variable = client.middle_name
    surname_variable = client.surname
    business_name_variable = client.business_name
    passport_number_variable = client.passport_number
    business_number_variable = client.business_number
    stored_otp = otp  # Store the OTP

    print(stored_otp)  # You can print it or use it as needed

    time.sleep(5)
    submit_button = None
    try:
        otp_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input"))
        )
        
        scroll_into_view(driver, otp_input)
        
        otp_input.send_keys(stored_otp)  # Use the stored OTP
      

        submit_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button"))
        )
        
        scroll_into_view(driver, submit_button)
        submit_button.click()
       
    
    

        radio_label_xpath = '//label[@class="radio_label mt-2 font-weight-semi-bold"]'
        radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, radio_label_xpath))
        )
        scroll_into_view(driver, radio_button)
        radio_button.click()

        button_locator = ".m-button.mtn-digital-card_button.mtn-button_secondary2"
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_locator))
        )
        scroll_into_view(driver, button_element)
        button_element.click()

        time.sleep(3)

        first_name_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//input[@formcontrolname="firstName"]')
            )
        )
        scroll_into_view(driver, first_name_input)
        
        
        
        if client_middle_variable is not None:
            full_name = f"{first_name_variable} {client_middle_variable}"
        else:
            full_name = first_name_variable
        
        first_name_input.send_keys(full_name)
        time.sleep(3)

        surname_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//input[@formcontrolname="surName"]')
            )
        )
        
        scroll_into_view(driver, surname_input)
        surname_input.send_keys(surname_variable)

        time.sleep(3)

        radio_button_xpath = "/html/body/mtn-main/mtn-dashboard/div/div[2]/div/div[2]/div/mtn-business/div/div/mtn-stepper/section/div/mtn-step[1]/div/mtn-personal-details/div[1]/div[5]/mtn-radio-button-group/mtn-radio-button[2]/div/label/span[1]"
        radio_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, radio_button_xpath))
        )
        scroll_into_view(driver, radio_button)
        radio_button.click()

        time.sleep(3)

        passport_number_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".mtn-input-number_field_container")
            )
        )
        scroll_into_view(driver, passport_number_field)
        passport_number_field.click()

        time.sleep(3)
        passport_number_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "mtn-input-number_control")
            )
        )
        scroll_into_view(driver, passport_number_input)
        passport_number_input.send_keys(passport_number_variable)

        time.sleep(3)

        next_button_locator = ".m-button.mtn-digital-card_button.mtn-button_secondary2"
        next_button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_locator))
        )
        scroll_into_view(driver, next_button_element)
        next_button_element.click()

        time.sleep(3)

        business_name_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/mtn-main/mtn-dashboard/div/div[2]/div/div[2]/div/mtn-business/div/div/mtn-stepper/section/div/mtn-step[2]/div/mtn-business-details/div/div[2]/div[1]/div[1]/mtn-input/div/div[1]/input",
                )
            )
        )
        scroll_into_view(driver, business_name_input)
        business_name_input.send_keys(business_name_variable)
        time.sleep(3)

        business_number_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[2]/mtn-input-number/div/div"))
        )
        scroll_into_view(driver, business_number_field)
        business_number_field.click()
        time.sleep(5)

        business_number_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[2]/mtn-input-number/div/div/div/div/div/input",
                )
            )
        )
        scroll_into_view(driver, business_number_input)
        business_number_input.send_keys(business_number_variable)
        time.sleep(6)

        upload_locator = '.mtn-file-upload input[type="file"]'
        upload_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, upload_locator))
        )

        file_paths = [
            os.path.join(
                settings.MEDIA_ROOT,
                generate_filename(client, "image1.jpg", "passport_image"),
            ),
            os.path.join(
                settings.MEDIA_ROOT,
                generate_filename(client, "image2.jpg", "ck_image"),
            ),
        ]

        for i, element in enumerate(upload_elements):
            element.send_keys(file_paths[i])
            time.sleep(10)

        checkbox_locator = ".mtn-checkbox-button__control"
        checkbox_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox_locator))
        )
        scroll_into_view(driver, checkbox_element)
        time.sleep(20)
        checkbox_element.click()

        time.sleep(10)

        buttons = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    '//button[@class="m-button mtn-digital-card_button mtn-button_secondary2"]',
                )
            )
        )
        second_button = buttons[1]
        driver.execute_script("arguments[0].scrollIntoView();", second_button)
        second_button.click()
        time.sleep(10)

        buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    '//button[@class="m-button mtn-digital-card_button mtn-button_secondary2"]',
                )
            )
        )
        last_button = buttons[0]
        driver.execute_script("arguments[0].scrollIntoView();", last_button)
        time.sleep(5)
        
        last_button.click()
       
        take_screenshot(driver, "screenshot.png")

        # Update client after successful registration
        current_client = Client.objects.first()
        current_client.registration_count += 1
        current_client.save()

        if current_client.registration_count >= 7:
            # Move to the next client
            next_client = Client.objects.filter(registration_count=0).first()
            if next_client:
                return driver.quit()
    finally:
        # Close the browser in the finally block
        if driver:
            driver.quit()
            
    # finally:
    #     if driver:
    #         try:
    #             driver.quit()
    #         except WebDriverException:
    #             pass


  

        
    