from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import subprocess
import time
import os

def get_connected_devices():
    """Get a list of connected Android devices using adb"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]
        devices = []
        for line in lines:
            if line.strip() and 'device' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        return devices
    except Exception as e:
        print(f"Error getting device list: {e}")
        return []

def verify_app_installed(device_id):
    """Verify if Twitter app is installed on the device"""
    try:
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'pm', 'list', 'packages', 'com.twitter.android'],
            capture_output=True,
            text=True
        )
        return 'com.twitter.android' in result.stdout
    except Exception as e:
        print(f"Error checking Twitter app installation: {e}")
        return False

def grant_permissions(device_id):
    """Grant necessary permissions to the Twitter app"""
    permissions = [
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.CAMERA"
    ]
    try:
        for permission in permissions:
            subprocess.run([
                'adb', '-s', device_id, 'shell', 
                'pm', 'grant', 'com.twitter.android', permission
            ], capture_output=True)
    except Exception as e:
        print(f"Error granting permissions: {e}")

def setup_driver(device_id=None):
    """Set up the Appium driver with enhanced error handling"""
    try:
        if not device_id:
            devices = get_connected_devices()
            if not devices:
                print("No Android devices found connected!")
                return None
            device_id = devices[0]

        
        if not verify_app_installed(device_id):
            print("Twitter app is not installed on the device!")
            return None

        
        grant_permissions(device_id)

        capabilities = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": device_id,
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
            "skipServerInstallation": False,  
            "uiautomator2ServerInstallTimeout": 120000,  
            "adbExecTimeout": 120000,
            "androidDeviceReadyTimeout": 60000,
            "avdReadyTimeout": 60000,
            "avdLaunchTimeout": 60000
        }
        
        options = UiAutomator2Options().load_capabilities(capabilities)
        
        
        ports = [4723, 4724, 4725, 4726]
        driver = None
        
        for port in ports:
            try:
                driver = webdriver.Remote(f'http://127.0.0.1:{port}', options=options)
                print(f"Successfully connected to Appium server on port {port}")
                break
            except Exception as e:
                print(f"Failed to connect on port {port}: {e}")
                continue
        
        return driver

    except Exception as e:
        print(f"Error setting up driver: {e}")
        return None

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and return it"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Element not found: {value}")
        return None

def like_post(driver):
    """Like a post with enhanced error handling"""
    try:
        like_button = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/inline_like")
        if like_button:
            like_button.click()
            print("Post liked successfully")
            time.sleep(2)
        else:
            print("Like button not found")
    except Exception as e:
        print(f"Error liking post: {e}")

def comment_on_post(driver):
    """Comment on a post with enhanced error handling"""
    try:
        comment_button = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/inline_reply")
        if comment_button:
            comment_button.click()
            print("Clicked comment button")
            time.sleep(2)

            comment_box = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/tweet_text")
            if comment_box:
                comment_box.send_keys("Great post!")
                print("Entered comment text")
                time.sleep(1)

                post_button = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/button_tweet")
                if post_button:
                    post_button.click()
                    print("Posted comment")
                    time.sleep(2)
    except Exception as e:
        print(f"Error commenting on post: {e}")

def tap_post_button_twice(driver):
    """Double tap post button with enhanced error handling"""
    try:
        new_post_button = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/composer_write")
        if new_post_button:
            new_post_button.click()
            print("First tap on post button")
            time.sleep(2)

            new_post_button.click()
            print("Second tap on post button")
            time.sleep(2)
    except Exception as e:
        print(f"Error tapping post button: {e}")

def make_new_post(driver):
    """Make a new post with enhanced error handling"""
    try:
        tweet_box = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/tweet_text")
        if tweet_box:
            tweet_box.send_keys("Hello Twitter! This is an automated post #automation")
            print("Entered tweet text")
            time.sleep(2)

            post_button = wait_for_element(driver, AppiumBy.ID, "com.twitter.android:id/button_tweet")
            if post_button:
                post_button.click()
                print("Posted tweet successfully")
                time.sleep(2)
    except Exception as e:
        print(f"Error making new post: {e}")

def open_twitter(device_id=None):
    """Main function to run Twitter automation"""
    driver = None
    try:
        print("Starting Twitter automation...")
        driver = setup_driver(device_id)
        if not driver:
            print("Failed to initialize driver")
            return None
        
        print("Twitter opened successfully")
        time.sleep(5)  
        
        like_post(driver)
        time.sleep(2)
        comment_on_post(driver)
        
        time.sleep(2)
        tap_post_button_twice(driver)
        
        time.sleep(2)
        make_new_post(driver)
        
        return True
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()
            print("Session ended")

if __name__ == "__main__":
    
    devices = get_connected_devices()
    if devices:
        print("Connected devices:")
        for i, device in enumerate(devices):
            print(f"{i + 1}. {device}")
        
        
        if len(devices) > 1:
            try:
                device_index = int(input("Select device number (or press Enter for first device): ")) - 1
                selected_device = devices[device_index]
            except (ValueError, IndexError):
                print("Invalid selection, using first device")
                selected_device = devices[0]
        else:
            selected_device = devices[0]
            
        open_twitter(selected_device)
    else:
        print("No devices found. Please connect an Android device and try again.")