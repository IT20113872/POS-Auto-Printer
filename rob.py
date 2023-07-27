import time
import requests
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import re
from urllib.parse import urlparse
import threading
import win32api
from selenium.webdriver.common.keys import Keys
import PyPDF2

import aspose.pdf as ap

# Set to store unique URLs
visited_urls = set()

pdf_save_path = "sample.pdf"
output_pdf = "out.pdf"

def monitor_requests(driver, base_url):
    while True:
        for request in driver.requests:
            if request.response and request.url.startswith(base_url):
                if request.url not in visited_urls:
                    visited_urls.add(request.url)
                    print(request.url)

                    response = requests.get(request.url)

                    if response.status_code == 200:
                        html_code = response.text
                        pattern = r'data="(.+?\.pdf)"'
                        pdf_links = re.findall(pattern, html_code)

                        if pdf_links:
                            pdf_url = pdf_links[0]
                            # print(pdf_url)

                            # Extract the base URL from the original URL
                            parsed_url = urlparse(request.url)
                            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

                            # Combine the base URL with the PDF link
                            combined_pdf_url = base_url + pdf_url
                            print(combined_pdf_url)

                            # Download and print the PDF
                            download_pdf_from_link(
                                combined_pdf_url, pdf_save_path)
                            # os.startfile(pdf_save_path, 'print')
                                                
                          
        
                            # os.startfile(pdf_save_path, 'print')
                            # def print_pdf(pdf_save_path):
                            #     win32api.ShellExecute(0, "print", pdf_save_path, None, ".", 0)

                            # # Call the function to print the PDF with default settings

                            # print_pdf(pdf_save_path)
                            # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'p')

                            win32api.ShellExecute(0, "print", pdf_save_path, None, ".", 0)
                            # Switch to the newly opened tab (index 1)
                            driver.switch_to.window(driver.window_handles[1])
                            driver.close()

                    else:
                        print("Failed to fetch HTML. Status code:",
                              response.status_code)

        time.sleep(1)  # Adjust the sleep duration as needed


def download_pdf_from_link(url, save_path):
    try:
        response = requests.get(url, stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"PDF downloaded and saved to: {save_path}")
        else:
            print(
                f"Failed to download PDF. Status code: {response.status_code}")

    except Exception as e:
        print("Error occurred while downloading the PDF:", e)


# Configure Chrome options
chrome_options = Options()

chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_argument(
     '--user-data-dir=C:\\Users\\Ishan The Ghost\\AppData\\Local\\Google\\Chrome\\User Data\\')



# Executable Path	C:\Program Files\Google\Chrome\Application\chrome.exe
# Profile Path	C:\Users\Eshan Nimsara\AppData\Local\Google\Chrome\User Data\Default


# Create the Selenium Wire-enabled Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Define the base URL without the invoice number
# base_url = "http://pharmacy.demo.apps.cipherlabz.com/POSDashboard/GetPdf?reportName=POSInvoice"
# base_url = "http://familycare.apps.cipherlabz.com"
base_url = "http://familycare.apps.cipherlabz.com/POSDashboard/GetPdf"

# http://familycare.apps.cipherlabz.com/POSDashboard/GetPdf?reportName=POSInvoice.rpt&currentLoggedInUser=BUDDHIKA%20B&cashierName=BUDDHIKA&terminalNumber=Terminal%20004&invoiceNumber=MAI4000059
# http://familycare.apps.cipherlabz.com/Downloads/Temp_BUDDHIKA%20B_MAI4000059.pdf
# Start the request monitoring thread
request_monitor_thread = threading.Thread(
    target=monitor_requests, args=(driver, base_url))
request_monitor_thread.start()

# Access the browser and perform your actions
# driver.get('http://pharmacy.demo.apps.cipherlabz.com')
driver.get('http://familycare.apps.cipherlabz.com')
# ...do more actions...

# Wait for the browser interactions to complete
request_monitor_thread.join()
