import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# Generate Chrome options
def create_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options

# Simulate human-like mouse movement
def random_mouse_move(driver):
    try:
        width = driver.execute_script("return window.innerWidth;")
        height = driver.execute_script("return window.innerHeight;")
        x = random.randint(0, width)
        y = random.randint(0, height)
        ActionChains(driver).move_by_offset(x, y).perform()
        time.sleep(random.uniform(0.3, 0.7))
    except Exception as e:
        print(f"[MouseMove Error] {e}")
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(0.5)

# List of video links
link_list = [
    "https://vidoza.net/8193axbknvto.html",
    "https://vidoza.net/49zpjy1rsjo1.html",
    "https://vidoza.net/qaa0w816elml.html",
    "https://vidoza.net/74eb28jag82j.html",
    "https://vidoza.net/6ed6ivawned3.html",
    "https://vidoza.net/dr7txnc1np5u.html",
    "https://vidoza.net/v4hvfnl6l1zs.html",
    "https://vidoza.net/vddxot92drvn.html"
]

# Randomly pick 3 links
selected_links = random.sample(link_list, 3)

# The main function to run for each link
def process_link(link, index):
    start_time = time.time()
    try:
        print(f"[{index}] Launching Chrome for: {link}")
        driver = webdriver.Chrome(options=create_chrome_options())
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get("https://www.dailymotion.com/playlist/x9dd5m")
        time.sleep(random.uniform(2, 3))

        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vplayer")))
        random_mouse_move(driver)

        try:
            play_xpath = "//button[@title='Play Video']"
            play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_xpath)))
            play_button.click()
            time.sleep(2)
            print(f"[{index}] Video started.")
        except Exception as e:
            print(f"[{index}] Play button error: {e}")

        time.sleep(40)
        print(f"[{index}] Watched video for ~40 seconds.")

        try:
            download_xpath = "//a[@class='btn btn-success btn-lg btn-download btn-download-n']"
            download_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, download_xpath)))
            download_button.click()
            print(f"[{index}] Download button clicked.")
            time.sleep(3)
        except:
            print(f"[{index}] Download button not found.")

    except Exception as e:
        print(f"[{index}] Error processing link: {e}")
    finally:
        driver.quit()
        print(f"[{index}] Chrome closed. Time spent: {int(time.time() - start_time)} seconds")

# Parallel execution manager
def run_parallel():
    print("[INFO] Starting parallel video automation.")
    start_time = time.time()
    max_duration = 20 * 60  # 20 minutes

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_link, link, idx + 1) for idx, link in enumerate(selected_links)]
        for future in as_completed(futures, timeout=max_duration):
            try:
                future.result()
            except Exception as e:
                print(f"[Thread Error] {e}")

    print(f"[INFO] All tasks completed in {int(time.time() - start_time)} seconds.")

# Run the program
if __name__ == "__main__":
    run_parallel()
