from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time

def setup_driver():
    capabilities = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "16e80a2e",  # Your device ID
        "appPackage": "com.twitter.android",
        "appActivity": ".StartActivity",  
        "noReset": True,
        "autoGrantPermissions": True,
        "ignoreHiddenApiPolicyError": True,
        "disableWindowAnimation": True,
        "newCommandTimeout": 6000,
        "androidInstallTimeout": 90000,
        "systemPort": 8201,
        "skipDeviceInitialization": True,
        "skipServerInstallation": True
    }
    
    options = UiAutomator2Options().load_capabilities(capabilities)
    driver = None
    try:
        driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
        return driver
    except Exception as e:
        print(f"Error setting up driver: {e}")
        if driver:
            driver.quit()
        return None

def like_post(driver):
    try:
        like_button = driver.find_element(AppiumBy.ID, "com.twitter.android:id/inline_like")
        like_button.click()
        print("Post liked successfully")
        time.sleep(2)  
    except Exception as e:
        print(f"Error liking post: {e}")

def comment_on_post(driver):
    try:
        comment_button = driver.find_element(AppiumBy.ID, "com.twitter.android:id/inline_reply")
        comment_button.click()
        print("Clicked comment button")
        time.sleep(2)

        comment_box = driver.find_element(AppiumBy.ID, "com.twitter.android:id/tweet_text")
        comment_box.send_keys("Great post!")
        print("Entered comment text")
        time.sleep(1)

        post_button = driver.find_element(AppiumBy.ID, "com.twitter.android:id/button_tweet")
        post_button.click()
        print("Posted comment")
        time.sleep(2)
    except Exception as e:
        print(f"Error commenting on post: {e}")

def tap_post_button_twice(driver):
    try:
        new_post_button = driver.find_element(AppiumBy.ID, "com.twitter.android:id/composer_write")
        new_post_button.click()
        print("First tap on post button")
        time.sleep(2)

        new_post_button.click()
        print("Second tap on post button")
        time.sleep(2)
    except Exception as e:
        print(f"Error tapping post button: {e}")

def make_new_post(driver):
    try:
        tweet_box = driver.find_element(AppiumBy.ID, "com.twitter.android:id/tweet_text")
        tweet_box.send_keys("Hello Twitter! This is an automated post #automation")
        print("Entered tweet text")
        time.sleep(2)

        post_button = driver.find_element(AppiumBy.ID, "com.twitter.android:id/button_tweet")
        post_button.click()
        print("Posted tweet successfully")
        time.sleep(2)
    except Exception as e:
        print(f"Error making new post: {e}")

def open_twitter():
    driver = None
    try:
        print("Starting Twitter automation...")
        driver = setup_driver()
        if not driver:
            print("Failed to initialize driver")
            return None
        
        time.sleep(5)
        print("Twitter opened successfully")
       
        time.sleep(3)  
        like_post(driver)
        time.sleep(2)
        comment_on_post(driver)
        
        time.sleep(2)
        tap_post_button_twice(driver)
        
        time.sleep(2)
        make_new_post(driver)
        
        xml_layout = driver.page_source
        print("XML Layout:")
        print(xml_layout)
        
        return xml_layout
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("Session ended")

if __name__ == "__main__":
    open_twitter()