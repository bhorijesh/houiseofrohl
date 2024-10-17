from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load CSV data
csv_data = pd.read_csv('final.csv')

# Initialize WebDriver
driver = webdriver.Firefox()

scraped_data = []

for index, row in csv_data.iterrows():
    if index >= 100:  # Limit to first 5 rows for testing
        break

    url = row['links']
    driver.get(url)

    try:
        # Product name, SKU, and UPC extraction
        product_name = driver.find_element(By.XPATH, '//h1').text
        sku = driver.find_element(By.CLASS_NAME, 'js-product-sku').text
        upc = driver.find_element(By.CLASS_NAME, 'js-product-upc').text

        # Feature extraction
        feature_list = []
        feat_elements = driver.find_elements(By.ID, 'pdp-features')
        for li in feat_elements:
            feature_list.append(li.text)

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        product_name, sku, upc = None, None, None
        feature_list = []

    try:
        # Slide content extraction
        slide_content = []
        slider = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'slick-slider'))
        )
        print("Slider found.")

        # Extract content of the first slide
        first_slide = driver.find_element(By.CLASS_NAME, 'slick-slide.slick-active')
        slide_content.append(first_slide.text)

        # Click through the next slides and extract their content
        next_button = driver.find_element(By.CLASS_NAME, 'slick-next')

        for _ in range(3):  # Get content from 3 slides
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Allow slide transition

            current_slide = driver.find_element(By.CLASS_NAME, 'slick-slide.slick-active')
            slide_content.append(current_slide.text)

    except Exception as e:
        print(f"Error navigating slider: {e}")
        slide_content = []

    # Append the data to the list
    scraped_data.append({
        'URL': url,
        'Product Name': product_name,
        'SKU': sku,
        'UPC': upc,
        'Features': feature_list,
        'Slides': slide_content
    })

# Quit the WebDriver
driver.quit()

# Save the scraped data to a new CSV file
scraped_df = pd.DataFrame(scraped_data)
scraped_df.to_csv('trial.csv', index=False)

print("Scraping completed!")
