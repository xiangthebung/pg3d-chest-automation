import re
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


webstore_url = "https://store.pixelgun3d.com/"
account_button = '//*[@class="header__user-account header-line__user-account"]'
user_id_input = '//input[@id="user-id-input"]'
obtain_chest_button = '//button[@data-button-type="free" and {}]'
free_chest_button = obtain_chest_button.format(1)
free_chest_button_clickable = obtain_chest_button.format('not(@disabled)')
free_chest_button_disabled = obtain_chest_button.format('@disabled')



def does_existance_now(driver: webdriver.Edge, by: By, path: str):
    try:
        loadWait(driver, 0).until(expected_conditions.presence_of_element_located((by,path)))
        return True
    except: 
        return False
    
def loadWait(driver: webdriver.Edge, time: int = 3):
    return WebDriverWait(driver, time)

def user_logged_in(driver: webdriver.Edge):
    login_dropdown = driver.find_element(By.XPATH,
                                         account_button + '/child::*[last()]')

    login_type = login_dropdown.get_attribute("class")

    if "login-button" in login_type:
        return False
    elif "logout" in login_type:
        return True
    else:
        raise Exception("Login info not found")


def user_logout(driver: webdriver.Edge):
    driver.find_element(By.XPATH, account_button).click()
    driver.find_element(
        By.XPATH,
        account_button + '//button[contains(@class,"logout-button")]').click()


def log_user_in(driver: webdriver.Edge, user_id: str):
    if user_logged_in(driver):
        user_logout(driver)
        driver.refresh()

    # Login with user_id
    driver.find_element(By.XPATH, account_button).click()
    driver.find_element(By.XPATH, user_id_input).send_keys(user_id + Keys.ENTER)
    # Wait for login attempt
    loadWait(driver).until_not(expected_conditions.presence_of_element_located((By.XPATH, '//button[contains(@class, "loading")]')))

    # User account does not exist
    if does_existance_now(driver, By.XPATH, '//*[@data-error-type="not-found"]'):
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        raise Exception("Invalid user id")
    
    # Wait for popup to close after pressing esc
    loadWait(driver).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@data-id="user-id-modal" and @hidden]')))
    
        
def get_free_chest(driver: webdriver.Edge):
    chest_button = driver.find_element(By.XPATH, free_chest_button)
    # try:
    #     wait_for_available = loadWait(driver,1).until(expected_conditions.presence_of_element_located((By.XPATH, free_chest_button_clickable + '/span[@data-id = "get-free"]')))
    # except:
    #     pass
    time.sleep(0.5)
    
    # If eligible for for chest
    if does_existance_now(driver, By.XPATH, free_chest_button_clickable):
        # Close gdpr banner because it covers the button
        if does_existance_now(driver, By.XPATH, '//*[contains(@class,"gdpr-container")]'): #gdpr banner
            driver.find_element(By.XPATH, '//button[contains(@class,"gdpr-close")]').click() #close banner

        # Click chest
        chest_button.click()
        loadWait(driver).until(expected_conditions.presence_of_element_located((By.XPATH, '//button[text()="Back to store"]')))
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        loadWait(driver).until(expected_conditions.presence_of_element_located((By.XPATH, free_chest_button_disabled)))
        
    elif does_existance_now(driver,By.XPATH, free_chest_button_disabled):
        pass
    
    else:
        raise Exception("Chest button availability not found")
    

if __name__ == "__main__":
    options = webdriver.EdgeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Edge(options)
    driver.maximize_window()
    driver.get(webstore_url) 
    
    for i in range(325892610,325894305):  
        try:
            log_user_in(driver, str(i))
            get_free_chest(driver)
        except Exception as e:
            print(e)

