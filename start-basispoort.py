#!/home/wbkoetsier/dev/venv-selenium/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import os
import sys
from ruamel.yaml import YAML as ruamel_yaml
from ruamel.yaml.error import YAMLError, YAMLStreamError
from pathlib import Path

# let's say, wait for 20 seconds by default
DEFAULT_WAIT = 20

# Define custom error
class StartBasispoortError(Exception):
    pass


# Fetch username and password, if absent, abort
username = os.environ.get('BASISPOORT_USERNAME')
passwd = os.environ.get('BASISPOORT_KEY')
if not username and not passwd:
    raise StartBasispoortError('Please set environment variables BASISPOORT_USERNAME and BASISPOORT_KEY')

# Read the YAML file with all the Basispoort website HTML details
basispoort_yaml_path = Path(Path(__file__).parent, 'basispoort.yaml')
try:
    yaml_file = basispoort_yaml_path.resolve()
except FileNotFoundError:
    raise StartBasispoortError('Could not find Start Basispoort configuration YAML file at {}'.format(basispoort_yaml_path))
yaml = ruamel_yaml()
with open(str(yaml_file), 'r') as yf:
    try:
        basispoort_yaml = yaml.load(yf) or {}
    except (YAMLError, YAMLStreamError) as ye:
        raise StartBasispoortError('Error loading yaml:', ye)

# Prepare browser
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(basispoort_yaml.get('url', ''))
if basispoort_yaml.get('title') not in driver.title:
    raise StartBasispoortError('Failed to load Basispoort login page')

# Log in to basispoort
loginview_yaml = basispoort_yaml.get('loginview', {})
loginview = WebDriverWait(driver, DEFAULT_WAIT).until(
    EC.presence_of_element_located((By.ID, loginview_yaml.get('id')))
)
input_username = loginview.find_element_by_id(
    loginview_yaml.get('username_box', {}).get('id', ''))
input_username.send_keys(username)
input_passwd = loginview.find_element_by_id(
    loginview_yaml.get('passwd_box', {}).get('id', ''))
input_passwd.send_keys(passwd)
login_button = loginview.find_element_by_id(
    loginview_yaml.get('login_button', {}).get('id', ''))
login_button.click()

# Follow the link as given in the message
message_yaml = basispoort_yaml.get('thuisgebruik_message', {})
message = WebDriverWait(driver, DEFAULT_WAIT).until(
    EC.presence_of_element_located((By.ID, message_yaml.get('id')))
)
link = message.find_element_by_tag_name('a')
href = link.get_attribute('href')
driver.get(href)

# Select the correct app
app_yaml = basispoort_yaml.get('start-educatieve-app-leerling', {})
child_app = WebDriverWait(driver, DEFAULT_WAIT).until(
    EC.presence_of_element_located((By.ID, app_yaml.get('id')))
)

# And now for the magic...
# The child will have to click the Play button, after which the app goes full screen. The child has to close up
# (close the browser).
child_app.click()

# So no driver.close() here. Just let script exit 0
sys.exit(0)
