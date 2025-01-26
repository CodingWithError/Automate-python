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

def upvote_post(driver, wait):
   try:
       upvote_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.XPATH, "//android.view.View[@resource-id='post_footer']//android.view.View[1]")
       ))
       upvote_button.click()
       print("Upvoted post")
       time.sleep(2)
       return True
   except Exception as e:
       print(f"Error upvoting post: {e}")
       return False

def open_comments(driver, wait):
   try:
       comment_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.XPATH, "//android.view.View[@resource-id='post_comment_button']")
       ))
       comment_button.click()
       print("Opened comments")
       time.sleep(2)
       
       print("Page source after opening comments:")
       print(driver.page_source)
       return True
   except Exception as e:
       print(f"Error opening comments: {e}")
       return False

def write_and_post_comment(driver, wait):
   try:
       comment_box = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.reddit.frontpage:id/reply_text")
       ))
       comment_box.send_keys("hi")
       print("Wrote comment")
       time.sleep(1)
       
       post_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.reddit.frontpage:id/menu_item_text")
       ))
       post_button.click()
       print("Posted comment")
       time.sleep(2)
       return True
   except Exception as e:
       print(f"Error posting comment: {e}")
       return False
       
def join_conversation(driver, wait):
   try:
       join_button = wait.until(EC.presence_of_element_located(
           (AppiumBy.ID, "com.reddit.frontpage:id/reply_text_view")
       ))
       join_button.click()
       print("Opened comment box")
       time.sleep(2)
       
       write_and_post_comment(driver, wait)
       
       print("Page source after opening comment box:")
       print(driver.page_source)
       return True
   except Exception as e:
       print(f"Error opening comment box: {e}")
       return False

def open_reddit():
   driver = setup_driver()
   wait = WebDriverWait(driver, 30)
   try:
       time.sleep(5)
       reddit_app = wait.until(EC.presence_of_element_located(
           (AppiumBy.XPATH, "//android.widget.TextView[@text='Reddit']")
       ))
       reddit_app.click()
       print("Opened Reddit app")
       time.sleep(10)
       
       upvote_post(driver, wait)
       open_comments(driver, wait)
       join_conversation(driver, wait)
       
   except Exception as e:
       print(f"Error: {e}")
   finally:
       driver.quit()
       print("Session ended")

if __name__ == "__main__":
   open_reddit()