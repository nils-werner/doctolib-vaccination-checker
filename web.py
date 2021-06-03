import time
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Option(Enum):
    ModernaFirst = 6936
    BiontechFirst = 6768
    AZFirst = 7109
    JanssenFirst = 7978
    ModernaSecond = 6936
    BiontechSecond = 6869
    AZSecond = 7110


def url(
    location,
    Prio1=False,
    Prio2=False,
    Prio3=False,
    Prio4=False,
    Bavaria=False,
    BadenWurttemberg=False,
    Berlin=False,
    **kwargs
):
    if Prio1 | Prio2 | Prio3 | Bavaria | BadenWurttemberg | Berlin:
        kwargs['ModernaFirst'] = True
        kwargs['BiontechFirst'] = True
        kwargs['AZFirst'] = True
        kwargs['JanssenFirst'] = True

    if Prio4:
        kwargs['AZFirst'] = True

    options = [f"ref_visit_motive_ids[]={Option[k].value}" for k, v in kwargs.items() if v]
    options = "&".join(options)

    base = "https://www.doctolib.de/impfung-covid-19-corona/"

    return f"{base}{location}?{options}"


def poll(url, remote=False):
    if remote:
        driver = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)

    driver.get(url)

    html = driver.find_element_by_tag_name('html')

    for i in range(3):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    near = driver.find_elements_by_class_name("availabilities-slot")
    far = driver.find_elements_by_class_name("availabilities-next-slot")

    driver.close()
    return len(near), len(far)
