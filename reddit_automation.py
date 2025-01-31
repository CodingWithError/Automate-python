from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import subprocess
import time

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
    """Verify if Reddit app is installed on the device"""
    try:
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'pm', 'list', 'packages', 'com.reddit.frontpage'],
            capture_output=True,
            text=True
        )
        return 'com.reddit.frontpage' in result.stdout
    except Exception as e:
        print(f"Error checking Reddit app installation: {e}")
        return False

def grant_permissions(device_id):
    """Grant necessary permissions to the Reddit app"""
    permissions = [
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.CAMERA",
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION"
    ]
    try:
        for permission in permissions:
            subprocess.run([
                'adb', '-s', device_id, 'shell', 
                'pm', 'grant', 'com.reddit.frontpage', permission
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
            print("Reddit app is not installed on the device!")
            return None

       
        grant_permissions(device_id)

        capabilities = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": device_id,
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

def wait_for_clickable(driver, by, value, timeout=10):
    """Wait for element to be clickable and return it"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        return element
    except TimeoutException:
        print(f"Element not clickable: {value}")
        return None

def wait_for_elements(driver, by, value, timeout=10):
    """Wait for elements to be present and return them"""
    try:
        wait = WebDriverWait(driver, timeout)
        elements = wait.until(EC.presence_of_all_elements_located((by, value)))
        return elements
    except TimeoutException:
        print(f"Elements not found: {value}")
        return []

def find_and_upvote_post(driver):
    """Find and upvote the first post"""
    try:
        first_post = wait_for_element(driver, AppiumBy.XPATH, "//android.view.View[@resource-id='post_unit']")
        if first_post:
            upvote_button = first_post.find_element(AppiumBy.XPATH, 
                ".//android.view.View[@resource-id='post_footer']/android.view.View[1]")
            if upvote_button:
                upvote_button.click()
                print("Upvoted the first post successfully")
                return True
    except Exception as e:
        print(f"Error upvoting post: {e}")
    return False

def comment_on_post(driver):
    """Comment on the first post"""
    try:
        first_post = wait_for_element(driver, AppiumBy.XPATH, "//android.view.View[@resource-id='post_unit']")
        if first_post:
            comment_button = first_post.find_element(AppiumBy.XPATH, 
                ".//android.view.View[@resource-id='post_footer']/android.view.View[@resource-id='post_comment_button']")
            if comment_button:
                comment_button.click()
                print("Clicked the comment button on the first post")
                time.sleep(5)

                join_button = wait_for_clickable(driver, AppiumBy.XPATH, 
                    "//android.widget.Button[contains(@text, 'Join the conversation')]")
                if join_button:
                    join_button.click()
                    print("Clicked 'Join the conversation' button")
                    time.sleep(2)

                comment_input = wait_for_element(driver, AppiumBy.XPATH, "//android.widget.EditText")
                if comment_input:
                    comment_input.send_keys("This is an automated comment.")
                    print("Typed a comment")

                    submit_button = wait_for_clickable(driver, AppiumBy.XPATH, 
                        "//android.widget.Button[contains(@text, 'Post')]")
                    if submit_button:
                        submit_button.click()
                        print("Submitted the comment")
                        return True
    except Exception as e:
        print(f"Error commenting on post: {e}")
    return False

def find_and_message_user(driver):
    """Find a user and send them a message"""
    try:
        
        time.sleep(3)

        comments = wait_for_elements(driver, AppiumBy.XPATH, 
            "//android.view.ViewGroup[contains(@content-desc, 'comment by')]")
        if not comments:
            print("No comments found")
            return False

        skip_users = ['AltruisticDistance56', 'AutoModerator', 'Dependent-Taste-9645', 'Misaboi']#this is to ignore your accounts
      
        for comment in comments:
            try:
                username = comment.find_element(AppiumBy.XPATH, 
                    ".//android.widget.TextView[@resource-id='com.reddit.frontpage:id/author']")
                username_text = username.get_attribute('text')
                
                if username_text not in skip_users:
                    print(f"Found username: {username_text}")
                    
                    username_clickable = comment.find_element(AppiumBy.XPATH, 
                        ".//android.view.View[@resource-id='com.reddit.frontpage:id/author_clickable_target']")
                    username_clickable.click()
                    print("Clicked on username")
                                       
                    time.sleep(3)
                    start_chat = wait_for_element(driver, AppiumBy.XPATH,
                        "//android.widget.LinearLayout[@resource-id='com.reddit.frontpage:id/start_chat']")
                    if start_chat:
                        start_chat.click()
                        print("Clicked Start Chat button")
                       
                        time.sleep(3)
                       
                        message_input = wait_for_element(driver, AppiumBy.XPATH,
                            "//android.widget.EditText[@resource-id='text_message_input']")
                        if message_input:
                            message_input.click()
                            message_input.send_keys("Hey! How are you doing?")
                            print("Typed message")
                        
                            time.sleep(1)
                           
                            send_button = wait_for_element(driver, AppiumBy.XPATH,
                                "//android.view.View[@content-desc='Send message']")
                            if send_button:
                                send_button.click()
                                print("Clicked send button")
                                
                                time.sleep(3)
                                
                                page_source = driver.page_source
                                print("\nXML Structure after sending message:")
                                print(page_source)
                                return True
                    break
            except NoSuchElementException:
                continue
    except Exception as e:
        print(f"Error messaging user: {e}")
    return False

def open_reddit_and_interact(device_id=None):
    """Main function to run Reddit automation"""
    driver = None
    try:
        print("Starting Reddit automation...")
        driver = setup_driver(device_id)
        if not driver:
            print("Failed to initialize driver")
            return None
        
        print("Reddit opened successfully")
        time.sleep(5)  
        
        
        find_and_upvote_post(driver)
        time.sleep(2)
        comment_on_post(driver)
        time.sleep(2)
        find_and_message_user(driver)
        
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
            
        open_reddit_and_interact(selected_device)
    else:
        print("No devices found. Please connect an Android device and try again.")