import asyncio
from flask import Flask, request, jsonify
from pyppeteer import launch

app = Flask(__name__)

async def get_chn_from_pyppeteer(eircode):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://hseareafinder.ie/')

    # Find the input field and type the Eircode
    await page.type('input#eircode', eircode)  # Adjust the selector based on actual input field
    await page.click('button[type="submit"]')  # Adjust with the actual submit button
    await page.waitForSelector('#result')  # Adjust to wait for the result to load

    # Extract the CHN info after page loads
    result = await page.evaluate('document.querySelector("#result span").textContent')  # Modify the selector accordingly

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
