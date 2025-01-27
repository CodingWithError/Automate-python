# Python Automation for Reddit and Twitter Using Appium
### This project demonstrates automation for Reddit and Twitter using Appium with Python. The automation covers actions like upvoting posts, commenting, liking, and making new posts on both platforms. It works on Android devices, including emulators, and uses the Appium framework for interaction with mobile applications.

## Prerequisites
## 1. Python Installation
### Ensure Python 3.x is installed on your system. You can download it from Python's official website.

## 2. Appium Installation
### Appium is the core framework used for mobile automation. Install Appium globally using npm (Node.js package manager):

### npm install -g appium


## You can verify the installation by running:
### appium --version

## 3. Java Development Kit (JDK)
### Appium relies on the Java Development Kit (JDK). Ensure you have JDK installed. You can download it from Oracle's JDK page.

## 4. Android Studio
### You need Android Studio for the Android Emulator and the required SDKs. Follow these steps to install Android Studio:
### Download and install Android Studio from here.
### Install the necessary SDKs and the Android Emulator.
### Set up a virtual device (AVD) for testing the automation.

## 5. Appium Python Client
### Install the Appium Python client using pip:
### pip install Appium-Python-Client

## 6. Selenium WebDriver
### Since Appium uses Selenium WebDriver for browser-like interactions, install Selenium:
### pip install selenium

## 7. Device Setup
### You can use either a physical Android device or an Android Emulator. If you're using an emulator, make sure to configure it properly in Android Studio.
### Emulator Setup: Open Android Studio → Tools → AVD Manager → Create a new virtual device (e.g., Pixel 3).
### Ensure USB debugging is enabled on your physical device if you're using one.

## 8. Appium Server
### Start the Appium server before running the script. You can start it by running the following command:

### appium
### Ensure that the Appium server is running on http://127.0.0.1:4723.

# Project Structure

.
├── README.md
├── reddit_automation.py    # Script for Reddit automation
└── twitter_automation.py   # Script for Twitter automation
### reddit_automation.py
### This script automates Reddit interactions such as upvoting, commenting, and submitting a comment.

### twitter_automation.py
### This script automates Twitter interactions such as liking a post, commenting, posting a tweet, and tapping the post button twice.

## Code Explanation
### 1. Imports

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time
webdriver: This is used to create a connection to the Appium server.
AppiumBy: Provides different locator strategies for interacting with elements.
WebDriverWait and expected_conditions: Used to wait for specific elements to load before interacting with them.
UiAutomator2Options: Configures Android-specific options for the Appium driver.
time: Used for adding delays between actions.

### 2. Setup Driver
The setup_driver() function configures the Appium driver with the required capabilities for Android automation. It connects to the Appium server running on http://127.0.0.1:4723.


def setup_driver():
    capabilities = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "16e80a2e",  # Your device ID
        "appPackage": "com.reddit.frontpage",  # For Reddit
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
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)  # Make sure the Appium server is running
    return driver
### 3. Reddit Automation (reddit_automation.py)
The open_reddit_and_interact() function automates Reddit by:

Opening the Reddit app.
Upvoting the first post.
Commenting on the post.
Submitting a comment.

### 4. Twitter Automation (twitter_automation.py)
The open_twitter() function automates Twitter by:
Liking a post.
Commenting on a post.
Tapping the post button twice.
Making a new tweet.

### 5. Error Handling
Each function is wrapped in try-except blocks to handle errors gracefully, ensuring the driver quits at the end of the session.

Running the Script
Start Appium Server: Before running the script, ensure that the Appium server is running:


### appium
### Run the Script:

## For Reddit automation:

### python reddit_automation.py
### For Twitter automation:


## python twitter_automation.py

# Notes
### Replace "deviceName": "16e80a2e" with the actual device ID of your connected Android device or emulator.
### Ensure that the required app packages (com.reddit.frontpage for Reddit and com.twitter.android for Twitter) are correct for the specific versions of the apps you are automating.
### The code uses xpath to find elements. You may need to adjust the xpath selectors if the app layout changes in future versions.
### Troubleshooting
### Appium Server Not Starting: Ensure that all dependencies (Node.js, Appium, Java) are installed correctly and the Appium server is running.

### Element Not Found: If elements are not found, try updating the xpath or use other locator strategies like ID or Class Name.

### Driver Initialization Issues: Ensure that the Android emulator or device is running and accessible by Appium.

# Conclusion
### This project demonstrates how to automate Reddit and Twitter using Appium and Python. It provides a solid foundation for automating other Android apps with similar logic.

# DriveVideoLink:-https://drive.google.com/file/d/1FcvWZskD2nj7drGx5rmF9ibvnv1j__J-/view?usp=sharing