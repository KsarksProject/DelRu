import pytest
from pages.task_main_page import TaskPage

@pytest.mark.regression
@pytest.mark.usefixtures('user_login')
class TestTaskCreate:
    def test_task_create(self, browser):
        p = TaskPage(browser)
        p.test_self_task()