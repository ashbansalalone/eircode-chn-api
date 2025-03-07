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

app = Flask(__name__)

# 📌 Install Google Chrome & ChromeDriver inside Render
def install_chrome():
    os.system("wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -")
    os.system("echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list")
    os.system("apt-get update")
    os.system("apt-get install -y google-chrome-stable")

    os.system("wget -N https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/linux64/chromedriver-linux64.zip")
    os.system("unzip -o chromedriver-linux64.zip")
    os.system("mv chromedriver-linux64/chromedriver /usr/bin/chromedriver")
    os.system("chmod +x /usr/bin/chromedriver")

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

    service = Service('/usr/bin/chromedriver')  # ✅ Correct ChromeDriver path
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
        return jsonify({"error": "CHN not found", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
