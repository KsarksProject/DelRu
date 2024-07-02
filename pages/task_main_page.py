import pytest
from Locators.main_page import Task
from pages.base import Base
from data.constants import Constants
from Locators.auth import Auth
from data.assertions import Assertions
from playwright.sync_api import Page
import allure
import re


class TaskPage(Base):
    def __init__(self, page: Page):
        super().__init__(page)
        self.assertions = Assertions(page)

    def user_login(self):
        self.open("")
        self.input(Auth.USERNAME_INPUT, Constants.login)
        self.input(Auth.PASSWORD_INPUT, Constants.password)
        self.click(Auth.LOGIN_BTN)

    @allure.feature("Task Functionality")
    @allure.story("Self Task Creation")
    @pytest.mark.parametrize("executor, deadline", [(Task.EXECUTOR, Task.DEADLINE)])
    def test_self_task(self, executor=Task.EXECUTOR, deadline=Task.DEADLINE):
        with allure.step("Нажатие на кнопку 'Создать'"):
            try:
                self.page.locator('text=Создать').nth(0).click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on 'Создать'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Ошибка при нажатии на кнопку 'Создать'")

        self.page.wait_for_timeout(1000)

        with allure.step("Выбор 'Прочее'"):
            try:
                self.page.locator('text=Прочее…').click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on 'Прочее'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Ошибка при выборе 'Прочее'")

        self.page.wait_for_timeout(1000)

        with allure.step("Поиск и выбор задачи"):
            try:
                self.page.locator('[placeholder="Искать в списке…"]').fill('Задача на исполнение поручения')
                self.page.wait_for_timeout(1000)
                self.page.locator('text=Задача на исполнение поручения').click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed task selection",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Ошибка при поиске и выборе задачи")

        try:
            form_ctrl = self.page.locator("div").filter(
                has_text=re.compile(r"^ИсполнительСрок$")
            ).get_by_role("textbox")
            form_ctrl.fill(Task.DEADLINE)
        except Exception as e:
            allure.attach(
                self.page.screenshot(),
                name="Failed filling deadline",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(str(e), name="Exception Trace")
            allure.fail("Не удалось заполнить дату")

        with allure.step("Заполнение комментария"):
            self.page.locator('textarea').nth(1).click()
            self.page.locator('textarea').nth(1).fill('PlayWright')

        try:
            form_ctrl = self.page.locator("div").filter(
                has_text=re.compile(r"^ИсполнительСрок$")
            ).get_by_role("combobox")
            form_ctrl.fill(Task.EXECUTOR)
            self.page.locator(f"text={Task.EXECUTOR}").click()
        except Exception as e:
            allure.attach(
                self.page.screenshot(),
                name="Failed filling executor",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(str(e), name="Exception Trace")
            allure.fail("Не удалось заполнить исполнителя или сохранить изменения")

        with allure.step("Отправка поручения"):
            try:
                self.page.get_by_text(Task.SEND_BTN)
                self.page.click(Task.SEND_BTN)
                self.page.locator("div").filter(has_text=re.compile(r"^Да$")).nth(1).click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed sending task",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось отправить поручение")

        with allure.step("Нажатие на кнопку информации о текущем пользователе"):
            try:
                self.page.locator("#current-user-info").get_by_role("img").click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on user info button",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось нажать на кнопку текущего пользователя")

        with allure.step("Нажатие на кнопку 'Выйти'"):
            try:
                self.page.locator("div").get_by_text("Выйти").click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on 'Выйти'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось нажать на кнопку 'Выйти'")

        with allure.step("Нажатие на кнопку 'Другой пользователь'"):
            try:
                self.page.locator("div").get_by_text("Другой пользователь").click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on 'Другой пользователь'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось нажать на кнопку 'Другой пользователь'")

        self.user_login()

        with allure.step("Переход в раздел 'На исполнение'"):
            try:
                out_link = self.page.wait_for_selector('text=На исполнение', timeout=10000)
                out_link.click()
                self.page.wait_for_load_state('domcontentloaded')  # Ожидание полной загрузки страницы
                allure.attach(
                    self.page.screenshot(),
                    name="Successful transition to 'На исполнение'",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed transition to 'На исполнение'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось перейти в раздел 'На исполнение'")

        with allure.step("Получение и клик по элементу"):
            try:
                card_element = self.page.locator("#row_0_active").get_by_text("Исполните").nth(0)
                card_element.click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed get and click on element",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось получить или кликнуть по элементу")

        with allure.step("Заполнение отчета"):
            self.page.locator('textarea').nth(1).click()
            self.page.locator('textarea').nth(1).fill('PlayWright Done')

        with allure.step("Нажатие на 'Выполнить'"):
            try:
                self.page.get_by_text("Выполнить").click()
                self.page.locator("div").filter(has_text=re.compile(r"^Да$")).nth(1).click()
            except Exception as e:
                allure.attach(
                    self.page.screenshot(),
                    name="Failed click on 'Выполнить'",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(str(e), name="Exception Trace")
                allure.fail("Не удалось нажать на кнопку 'Выполнить'")

        allure.attach(
            self.page.screenshot(),
            name="Final state",
            attachment_type=allure.attachment_type.PNG
        )

        # Добавьте ожидание или завершение теста, если необходимо
        # self.page.wait_for_timeout(1000)
        # ...


class TestTaskCreate:
    def test_task_create(self, browser):
        p = TaskPage(browser)
        p.test_self_task()
