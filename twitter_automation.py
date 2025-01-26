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
       "deviceName": "emulator-5554",
       "appPackage": "com.google.android.apps.nexuslauncher",
       "appActivity": "com.google.android.apps.nexuslauncher.NexusLauncherActivity",
       "noReset": True
   }
   options = UiAutomator2Options().load_capabilities(capabilities)
   driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
   return driver

def like_post(driver, wait):
   try:
       like_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.twitter.android:id/inline_like")
       ))
       like_button.click()
       print("Liked post")
       time.sleep(2)
       return True
   except Exception as e:
       print(f"Error liking post: {e}")
       return False

def write_comment(driver, wait):
   try:
       comment_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.twitter.android:id/inline_reply")
       ))
       comment_button.click()
       print("Clicked comment button")
       time.sleep(2)
       
       comment_box = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.twitter.android:id/tweet_text")
       ))
       comment_box.send_keys("hi")
       print("Wrote comment")
       time.sleep(1)
       
       post_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.twitter.android:id/button_tweet")
       ))
       post_button.click()
       print("Posted comment")
       time.sleep(2)
       return True
   except Exception as e:
       print(f"Error commenting: {e}")
       return False

def interact_with_twitter():
   driver = setup_driver()
   wait = WebDriverWait(driver, 30)
   try:
       time.sleep(5)
       x_app = wait.until(EC.presence_of_element_located(
           (AppiumBy.XPATH, "//android.widget.TextView[@text='X']")
       ))
       x_app.click()
       print("Opened X app")
       time.sleep(10)
       
       like_post(driver, wait)
       write_comment(driver, wait)
       
       print("Page source after operations:")
       print(driver.page_source)

   except Exception as e:
       print(f"Error: {e}")
   finally:
       driver.quit()
       print("Session ended")

if __name__ == "__main__":
   interact_with_twitter()