import os
import subprocess
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

app = Flask(__name__)

# 📌 Install Google Chrome & ChromeDriver inside Render
def install_chrome():
    os.system("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")
    os.system("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list")
    os.system("apt-get update")
    os.system("apt-get install -y google-chrome-stable")

    os.system("wget -N https://chromedriver.storage.googleapis.com/113.0.5672.63/chromedriver_linux64.zip")
    os.system("unzip -o chromedriver_linux64.zip -d ./chromedriver")  # Save chromedriver to a local directory
    os.system("chmod +x ./chromedriver/chromedriver")  # Ensure it's executable

# 📌 Run Chrome installation
install_chrome()

@app.route('/get_chn', methods=['GET'])
def get_chn():
    eircode = request.args.get('eircode')

    # ✅ Set up ChromeDriver with the correct path
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Specify the Chrome binary location in Render
    options.binary_location = "/usr/bin/google-chrome-stable"  # Add Chrome binary location here

    # Use local path to chromedriver (as it was installed in the current directory)
    service = Service('./chromedriver/chromedriver')  # Point to the local chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://hseareafinder.ie/')

    try:
        search_box = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[7]/div[1]/div[1]/input')
        search_box.send_keys(eircode)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[7]/div[1]/div[2]/div/div'))
        ).click()

        chn_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[7]/div[1]/div[2]/p/span[2]'))
        )

        return jsonify({"eircode": eircode, "chn": chn_element.text.strip()})

    except Exception as e:
        # Log error details for debugging
        return jsonify({
            "error": "CHN not found",
            "message": str(e),
            "traceback": traceback.format_exc()
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
