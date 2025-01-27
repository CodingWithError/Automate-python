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
        "appPackage": "com.reddit.frontpage",
        "appActivity": "com.reddit.launch.main.MainActivity",  
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
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options) #Make sure of checking the server
    return driver

def open_reddit_and_interact():
    driver = None
    try:
        print("Starting Reddit automation...")
        driver = setup_driver()
        
        time.sleep(5)
        print("Reddit opened successfully")
        
        first_post = driver.find_element(AppiumBy.XPATH, "//android.view.View[@resource-id='post_unit']")
        
        upvote_button = first_post.find_element(AppiumBy.XPATH, ".//android.view.View[@resource-id='post_footer']/android.view.View[1]")
      
        upvote_button.click()
        print("Upvoted the first post successfully")
       
        comment_button = first_post.find_element(AppiumBy.XPATH, ".//android.view.View[@resource-id='post_footer']/android.view.View[@resource-id='post_comment_button']")
        
        comment_button.click()
        print("Clicked the comment button on the first post")
        
        time.sleep(5)
        
        join_button = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Join the conversation')]")
        join_button.click()
        print("Clicked 'Join the conversation' button")
      
        time.sleep(2)
  
        comment_input = driver.find_element(AppiumBy.XPATH, "//android.widget.EditText")
        comment_input.send_keys("This is an automated comment.")
        print("Typed a comment")
        
        submit_button = driver.find_element(AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Post')]")
        submit_button.click()
        print("Submitted the comment")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            print("Session ended")

if __name__ == "__main__":
    open_reddit_and_interact()
