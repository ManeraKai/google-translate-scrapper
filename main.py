from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service

from colorama import Fore, Style


def main():
    lang_from = input("Translate From (lang code): ")
    lang_to = input("Translate To (lang code): ")
    ser = Service("./geckodriver")
    driver = webdriver.Firefox(service=ser)
    driver.get("https://translate.google.com/?sl=" + lang_from + "&tl=" + lang_to + "&op=translate")

    def check_exists(by_what, my_class):
        try:
            driver.find_element(by_what, my_class).text
            return True
        except:
            return False

    item = driver.find_element(
        By.XPATH, "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")

    while True:
        text = input("Enter Text: ")
        while True:
            if not check_exists(By.CLASS_NAME, "J0lOec"):
                break
        item.send_keys(text)

        while True:
            if check_exists(By.CLASS_NAME, "J0lOec"):
                if check_exists(By.CLASS_NAME, "VK4HE"):
                    for more_translations in driver.find_elements(By.CLASS_NAME, "VK4HE"):
                        more_translations.click()
                translated_text = driver.find_element(By.CLASS_NAME, "J0lOec").text
                print(Fore.BLUE + "Translated Text: " + Style.RESET_ALL + translated_text[:-2])

                if check_exists(By.CLASS_NAME, "Dwvecf"):
                    boxes = driver.find_elements(By.CLASS_NAME, "Dwvecf")
                    for box in boxes:
                        unknown = box.find_element(By.CLASS_NAME, "nYkDR")
                        if "Definitions of" in unknown.text:

                            # nYkDR = Definitions of `word`
                            # eqNifb = definition_boxes
                            # luGxAd = definition_box number
                            # fw3eif = definition
                            # PG9puc = dictionary type
                            # MZgjEb = use in sentence

                            print(Fore.BLUE + unknown.text + ":" + Style.RESET_ALL)
                            definition_types = box.find_elements(By.CLASS_NAME, "KWoJId")
                            definition_boxes = box.find_elements(By.CLASS_NAME, "eqNifb")

                            for i in range(0, len(definition_types)):
                                print(Fore.GREEN + definition_types[i].text + Style.RESET_ALL)
                                previous_number = -1
                                cycle = 0
                                for definition_box in definition_boxes:
                                    number = definition_box.find_element(By.CLASS_NAME, "luGxAd")
                                    if previous_number > int(number.text):
                                        cycle += 1
                                    previous_number = int(definition_box.find_element(By.CLASS_NAME, "luGxAd").text)
                                    if cycle == i:
                                        try:
                                            dictionary = definition_box.find_element(By.CLASS_NAME, "PG9puc")
                                            print(Fore.BLUE + "From " + dictionary.text + Style.RESET_ALL,
                                                  end=" ")
                                        except:
                                            pass
                                        definition = definition_box.find_element(By.CLASS_NAME, "fw3eif")
                                        print(Fore.BLUE + number.text + ". " + Style.RESET_ALL + definition.text)
                                        try:
                                            use_in_sentences = definition_box.find_element(By.CLASS_NAME, "MZgjEb")
                                            print(Fore.RED + "  \"" + use_in_sentences.text + "\"" + Style.RESET_ALL)
                                        except:
                                            pass
                                        try:
                                            definition_box.find_element(By.CLASS_NAME, "NJUGtd")
                                            print(Fore.BLUE + "  Synonyms:" + Style.RESET_ALL)
                                            for synonym_type_box in definition_box.find_elements(By.CLASS_NAME,
                                                                                                 "NJUGtd"):
                                                try:
                                                    synonym_type = synonym_type_box.find_element(By.CLASS_NAME,
                                                                                                 "BL1djf")
                                                    print("  " + synonym_type.text)
                                                except:
                                                    pass
                                                try:
                                                    for z in synonym_type_box.find_elements(By.CLASS_NAME, "PsfnLc"):
                                                        print("    - " + z.text)
                                                except:
                                                    pass
                                        except:
                                            pass

                        elif "Translations of" in unknown.text:
                            print(Fore.BLUE + unknown.text + ":" + Style.RESET_ALL)
                            try:
                                definition_types = box.find_elements(By.CLASS_NAME, "G8Go6b")
                                borders = box.find_elements(By.CLASS_NAME, "U87jab")

                                for i in range(0, len(borders)):
                                    print(Fore.BLUE + definition_types[i].text + ": " + Style.RESET_ALL)
                                    row = borders[i].find_elements(By.CLASS_NAME, "TKwHGb")
                                    for x in row:

                                        first_letter = x.find_element(By.CLASS_NAME, "j7bWb").text
                                        if first_letter != "":
                                            first_letter += " "
                                        alternative = x.find_element(By.CLASS_NAME, "kgnlhe").text
                                        print(Fore.CYAN + first_letter + Fore.BLUE + alternative + Style.RESET_ALL,
                                              end=": ")
                                        for z in x.find_elements(By.CLASS_NAME, "MtFg0"):
                                            print(z.text, end=" ")
                                        frequency = x.find_element(By.CLASS_NAME, "ROtxYd")
                                        buttons = frequency.find_elements(By.CLASS_NAME, "ksE5nf")
                                        times = 0
                                        for t in buttons:
                                            color = t.value_of_css_property('background-color')
                                            if color == "rgb(26, 115, 232)":
                                                times += 1
                                        print(Fore.BLUE + "Frequency is: " + Style.RESET_ALL + str(times) + "/3")
                                        print()
                            except:
                                pass
                break
        item.send_keys(Keys.CONTROL + "a")
        item.send_keys(Keys.DELETE)


if __name__ == "__main__":
    main()
 
