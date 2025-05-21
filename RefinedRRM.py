import random
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

def random_delay(min_ms=3000, max_ms=5000):
    return random.randint(min_ms, max_ms)

with sync_playwright() as p:
    
    # To capture the expected reference

    browser = p.chromium.launch(headless=False, slow_mo=25) # Opens browser and search for Bing
    context = browser.new_context()
    page = browser.new_page()
    page.goto('https://bing.com')
    page.wait_for_timeout(3000)
   
    page.click("[aria-label=\"0 characters out of 2000\"]") 
    page.keyboard.type("Rocket Raccoon - Marvel", delay=25) # To search the assigned character
    page.keyboard.press("Enter")
    page.wait_for_selector("li.b_algo h2 a", timeout=10000) 

    first_result = page.locator("li.b_algo h2 a").first
    href = first_result.get_attribute("href")  # Acquires URL of the first result to avoid opening a new tab
    
    print(f"Navigating to: {href}") # Proceed to the acquired URL of the first result and initiate snapshot for the expected.png
    page.goto(href)
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.screenshot(path="expected.png")

    # To capture the actual reference

    page.goto('https://bing.com') # Opens browser and search for Bing
    page.wait_for_timeout(3000)
    
    page.click("[aria-label=\"0 characters out of 2000\"]") 
    page.keyboard.type("Rocket Raccoon - Marvel", delay=25) # To search the assigned character once again
    page.keyboard.press("Enter")
    page.wait_for_selector("li.b_algo h2 a", timeout=10000)

    first_result = page.locator("li.b_algo h2 a").first
    href = first_result.get_attribute("href") # Acquires URL of the first result to avoid opening a new tab
    
    print(f"Navigating to: {href}") # Proceed to the acquired URL of the first result and initiate snapshot for the expected.png
    page.goto(href)
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.screenshot(path="actual.png")
    context.close()
    browser.close()

    # To verify that the actual matches the expected reference

    expected = Image.open("expected.png")
    actual = Image.open("actual.png")

    diff = ImageChops.difference(expected, actual)

    if diff.getbbox():
        print("Verified that the actual.png does not match the expected reference")
        diff.show()
    else:
        print("Verified that the actual.png matches the expected reference")

