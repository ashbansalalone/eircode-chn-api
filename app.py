import asyncio
from flask import Flask, request, jsonify
from pyppeteer import launch

app = Flask(__name__)

async def get_chn_from_pyppeteer(eircode):
    print("Starting browser...")
    browser = await launch(headless=True)
    page = await browser.newPage()

    print("Navigating to the page...")
    await page.goto('https://hseareafinder.ie/')
    
    print(f"Typing in Eircode: {eircode}")
    # Use the correct XPath for the input field (from your previous code)
    await page.type('//*[@id="app"]/div/div[7]/div[1]/div[1]/input', eircode)  # Correct XPath for Eircode input
    await page.click('button[type="submit"]')  # Modify with the correct submit button selector

    print("Waiting for result...")
    await page.waitForSelector('#result')  # Modify with the correct selector for results

    print("Extracting data...")
    result = await page.evaluate('document.querySelector("#result span").textContent')  # Adjust as needed

    await browser.close()
    return result

@app.route('/get_chn', methods=['GET'])
def get_chn():
    eircode = request.args.get('eircode')
    
    try:
        # Run the async function using asyncio
        result = asyncio.run(get_chn_from_pyppeteer(eircode))
        return jsonify({"eircode": eircode, "chn": result})

    except Exception as e:
        return jsonify({
            "error": "CHN not found",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
