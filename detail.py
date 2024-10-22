from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


csv_data = pd.read_csv('final.csv')

driver =  webdriver.Firefox()

scraped_data = []



for index, row in csv_data.iterrows():
    if index >=20:
        break
    url = row['links']
    driver.get(url)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    # time.sleep(2)
    try:
        feature_list =[]
        product_name = driver.find_element(By.XPATH,'//h1').text 
        sku =  driver.find_element(By.CLASS_NAME , 'js-product-sku').text
        upc =  driver.find_element(By.CLASS_NAME, 'js-product-upc').text
        feat = driver.find_elements(By.ID,'pdp-features')
        for li in feat:
            featu = li.text
            feature_list.append(featu)
        # Wait a moment to see the slide change
        time.sleep(2)
        # price = driver.find_element_by_xpath('//span[@class="price"]').text  
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        product_name = None
        sku = None
        

    try:
        slide_content = []
        slider = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'slick-slider'))
        )
        print("Slider found.")

        # Extract the first slide's content
        first_slide = driver.find_element(By.CLASS_NAME, 'slick-slide.slick-active')
        slide_content.append(first_slide.text)

        # Locate the 'Next' button and click it using JavaScript to avoid click interception
        next_button = driver.find_element(By.CLASS_NAME, 'slick-next')

        for i in range(3):  
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # Wait for slide transition

            current_slide = driver.find_element(By.CLASS_NAME, 'slick-slide.slick-active')
            slide_content.append(current_slide.text)

    except Exception as e:
        print(f"Error navigating slider: {e}")
        slide_content =[]
        
    try:
        images = driver.find_element(By.CSS_SELECTOR, 'img.plmr-c-product-info__image.js-product-img--default')
        image_url = images.get_attribute('src')

    except Exception as e:
        print(f"Error fetching images from {url}: {e}")
        image_url = None
        
    try:
        specification_container = driver.find_element(By.CLASS_NAME, 'plmr-c-additional-product-specs')
        boxes = specification_container.find_elements(By.CLASS_NAME, 'plmr-c-featured-product-specs__item')
        specification = {box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-text').text.strip(): 
                         box.find_element(By.CLASS_NAME, 'plmr-c-featured-product-specs__item-name').text.strip() 
                         for box in boxes}
    except Exception as e :
        print(f"Error fetching specifications from {url}: {e}")

    # Append the data to the list
    scraped_data.append({
        'URL': url,
        'Product Name': product_name,
        'SKU' : sku,
        'UPC' : upc,
        'Features':feature_list,
        'slide':slide_content,
        'Images' : image_url,
        'Specifications': specification
        # 'Price': price
    })

driver.quit()

# Save the scraped data to a new CSV file
scraped_df = pd.DataFrame(scraped_data)
scraped_df.to_csv('details.csv', index=False)  

print("Scraping completed!")

driver.quit()