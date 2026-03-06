from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def get_attendance(username, password):

    chrome_options = Options()
    

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    service = Service(ChromeDriverManager().install())


    driver = webdriver.Chrome(service=service,  options=chrome_options)


    
    wait = WebDriverWait(driver, 50)

    driver.get("https://webprosindia.com/vignanit/Default.aspx")

    # login
    wait.until(EC.presence_of_element_located((By.NAME, "txtId2"))).send_keys(username)
    driver.find_element(By.NAME, "txtPwd2").send_keys(password)
    driver.find_element(By.NAME, "imgBtn2").click()

    # click attendance
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "ATTENDANCE"))).click()

    # switch to iframe where content loads
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # wait for radio buttons
    radios = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@type='radio']"))
    )

    # select "Till now"
    radios[2].click()

    # click show
    show_button = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@value,'Show')]"))
    )

    driver.execute_script("arguments[0].click();", show_button)

    # wait for attendance table
    table = wait.until(
        
        
        EC.presence_of_element_located((By.XPATH, "//table[contains(.,'TOTAL')]"))
    )

    rows = table.find_elements(By.TAG_NAME, "tr")

    data = []
    for r in rows:
        cols = r.find_elements(By.TAG_NAME, "td")
        row = [c.text.strip() for c in cols if c.text.strip()]
        if row:
            data.append(row)

    driver.quit()
    return data