import pytest
from playwright.sync_api import sync_playwright
import allure
from allure import fail

# Функция для проверки разделов согласно чек-листу и списка поручений
@allure.feature('Делопроизводство')
@allure.story('Проверка раздела и списка поручений')
@pytest.mark.allure
def test_check_delo_and_tasks():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://deloros.centrvd.ru/client/#/')
        page.pause()

        try:
            # Авторизация
            page.fill('#login-user-id', 'a.bardashevich')
            page.fill('#login-password-id', 'sYSTEM99!')
            page.click('#loggin-button-id')
            page.wait_for_load_state('networkidle')
            page.pause()

            # Переход в раздел "Общие папки"
            with allure.step("Переход в раздел 'Общие папки'"):
                share_link = page.wait_for_selector('text=Общие папки', timeout=10000)
                share_link.click()
                page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                page.locator("#current-context").get_by_text("Общие папки").nth(1)
                print("Ссылка 'Общие папки' найдена")

            # Переход в раздел "Избранное"
            with allure.step("Переход в раздел 'Избранное'"):
                favor_link = page.wait_for_selector('text=Избранное', timeout=10000)
                favor_link.click()
                page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                print("Ссылка 'Избранное' найдена")

            # Дополнительные шаги навигации
            with allure.step("Открытие страницы 'Входящие'"):
                page.get_by_role("link", name="Входящие").click()

            with allure.step("Открытие страницы 'На исполнение'"):
                page.get_by_role("link", name="На исполнение").click()

            with allure.step("Открытие страницы 'Исходящие'"):
                page.get_by_role("link", name="Исходящие").click()

            with allure.step("Открытие страницы 'Избранное'"):
                page.get_by_role("link", name="Избранное").click()

            with allure.step("Клик по элементу с id '#favorites-folder-view'"):
                page.locator("#favorites-folder-view").click()

            with allure.step("Клик по ссылке 'Замещение'"):
                page.locator("a").filter(has_text="Замещение").click()

            with allure.step("Открытие страницы 'Д Делопроизводство'"):
                page.get_by_role("link", name="Д Делопроизводство").click()

            with allure.step("Открытие страницы 'С Совещания'"):
                page.get_by_role("link", name="С Совещания").click()

            # Переход в раздел "Исходящие"
            with allure.step("Переход в раздел 'Исходящие'"):
                out_link = page.wait_for_selector('text=Исходящие', timeout=10000)
                out_link.click()
                page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                print("Ссылка 'Исходящие' найдена")

            # Переход в раздел "Делопроизводство"
            with allure.step("Переход в раздел 'Делопроизводство'"):
                delo_link = page.wait_for_selector('text=Делопроизводство', timeout=10000)
                delo_link.click()
                page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                print("Ссылка 'Делопроизводство' найдена")

            # Переход в раздел "Поручения"
            with allure.step("Переход в раздел 'Поручения'"):
                poruchenia_link = page.wait_for_selector('text=Поручения', timeout=10000)
                poruchenia_link.click()
                page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                print("Ссылка 'Поручения' найдена")

            # Получение списка поручений и их количества
            with allure.step("Получение количества поручений"):
                task_counter = page.wait_for_selector('#grid-rows-counter', timeout=10000)
                task_count = task_counter.inner_text()
                allure.attach(task_count, name="Общее количество поручений", attachment_type=allure.attachment_type.TEXT)
                print(f"Общее количество поручений: {task_count}")

            page.wait_for_timeout(5000)

        except Exception as e:
            screenshot = page.screenshot(path="screenshot.png")  # Сохранение скриншота
            fail("Произошла ошибка при выполнении теста", screenshot=screenshot, exception_trace=str(e))

        finally:
            browser.close()

# Запуск тестов с использованием pytest и генерацией отчета Allure
if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-result"])
