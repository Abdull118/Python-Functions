from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Paths to Brave and ChromeDriver
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Update with your Brave browser binary path
CHROMEDRIVER_PATH = "/Users/arashnaimi/Downloads/chromedriver-mac-x64/chromedriver"  # Update with your ChromeDriver path

# Setting up the Brave browser options
options = webdriver.ChromeOptions()
options.binary_location = BRAVE_PATH

# Use the default Brave user profile
# Replace 'Default' with your specific Brave profile folder if needed
options.add_argument("user-data-dir=~/Library/Application Support/BraveSoftware/Brave-Browser/Default")

# Initialize the WebDriver for Brave
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to ChatGPT
    driver.get("https://chat.openai.com")

    # Allow time for the page to load
    time.sleep(5)

    # Find the input field and enter your prompt
    prompt = "Based on the information from Binder CS.pdf ONLY, can you use data from it ONLY and use the wording it uses to answer the following: {objective}"
    input_field = driver.find_element(By.TAG_NAME, "textarea")
    input_field.send_keys(prompt)
    input_field.send_keys(Keys.RETURN)

    # Allow time to observe the output
    time.sleep(10)

finally:
    # Quit the browser
    driver.quit()
