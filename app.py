# 📌 app.py - Flask API for Render
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

# Set up ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

@app.route('/get_chn', methods=['GET'])
def get_chn():
    eircode = request.args.get('eircode')
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
    app.run(host='0.0.0.0', port=10000)  # ✅ Changed port for Render
