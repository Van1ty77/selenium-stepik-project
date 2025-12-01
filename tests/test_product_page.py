import pytest
import time
from pages.product_page import ProductPage
from pages.basket_page import BasketPage
from pages.login_page import LoginPage
from pages.locators import ProductPageLocators

LINK = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
PRODUCT_LINK = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"


class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        link = "http://selenium1py.pythonanywhere.com/accounts/login/"
        page = LoginPage(browser, link)
        page.open()
        email = str(time.time()) + "@fakemail.org"
        password = str(time.time())
        page.register_new_user(email, password)
        page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, LINK)
        page.open()
        page.should_not_be_success_message()

    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, LINK)
        page.open()
        product_name = page.get_product_name()
        product_price = page.get_product_price()
        page.should_be_add_to_basket_button()
        page.add_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_product_added_to_basket(product_name)
        page.should_be_correct_basket_total(product_price)


@pytest.mark.parametrize('promo_offer', [
    "offer0",
    "offer1",
    "offer2",
    "offer3",
    "offer4",
    "offer5",
    "offer6",
    "offer7",
    "offer8",
    "offer9"
])
def test_guest_can_add_product_to_basket(browser, promo_offer):
    link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo={promo_offer}"
    page = ProductPage(browser, link)
    page.open()
    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.should_be_add_to_basket_button()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_product_added_to_basket(product_name)
    page.should_be_correct_basket_total(product_price)


@pytest.mark.parametrize('promo_offer', [
    "offer0",
    "offer1",
    "offer2",
    "offer3",
    "offer4",
    "offer5",
    "offer6",
    pytest.param("offer7", marks=pytest.mark.xfail),
    "offer8",
    "offer9"
])
def test_guest_can_add_product_to_basket_with_xfail(browser, promo_offer):
    link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo={promo_offer}"
    page = ProductPage(browser, link)
    page.open()
    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_product_added_to_basket(product_name)
    page.should_be_correct_basket_total(product_price)


def test_find_bug_explicitly(browser):
    results = {}
    for promo_num in range(10):
        promo_offer = f"offer{promo_num}"
        link = f"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo={promo_offer}"
        print(f"Testing {promo_offer}...")
        page = ProductPage(browser, link)
        page.open()
        product_name = page.get_product_name()
        product_price = page.get_product_price()
        page.add_to_basket()
        page.solve_quiz_and_get_code()
        try:
            assert page.is_element_present(*ProductPageLocators.SUCCESS_MESSAGE)
            actual_name = page.get_success_message_text()
            assert product_name == actual_name
            assert page.is_element_present(*ProductPageLocators.BASKET_TOTAL_MESSAGE)
            actual_price = page.get_basket_total_text()
            assert product_price == actual_price
            results[promo_offer] = "PASS"
            print(f"{promo_offer}: PASS")
        except AssertionError as e:
            results[promo_offer] = f"FAIL - {str(e)}"
            print(f"{promo_offer}: FAIL - {e}")
    print("FINAL RESULTS:")
    for promo, result in results.items():
        print(f"{promo}: {result}")
    bugged_promos = [promo for promo, result in results.items() if "FAIL" in result]
    if bugged_promos:
        print(f"BUG FOUND ON PROMO: {', '.join(bugged_promos)}")
        for promo in bugged_promos:
            print(f"Bug link: http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo={promo}")
    else:
        print("NO BUGS FOUND")


@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.add_to_basket()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.should_not_be_success_message()


@pytest.mark.xfail
def test_message_disappeared_after_adding_product_to_basket(browser):
    page = ProductPage(browser, LINK)
    page.open()
    page.add_to_basket()
    page.should_disappear_success_message()


def test_guest_should_see_login_link_on_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.should_be_login_link()


def test_guest_can_go_to_login_page_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.should_be_login_link()
    page.go_to_login_page()


def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    page = ProductPage(browser, PRODUCT_LINK)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()