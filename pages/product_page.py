from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_to_basket(self):
        self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON).click()

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def get_success_message_text(self):
        return self.browser.find_element(*ProductPageLocators.SUCCESS_MESSAGE).text

    def get_basket_total_text(self):
        return self.browser.find_element(*ProductPageLocators.BASKET_TOTAL_MESSAGE).text

    def should_be_add_to_basket_button(self):
        assert self.is_element_present(*ProductPageLocators.ADD_TO_BASKET_BUTTON)

    def should_be_product_added_to_basket(self, product_name):
        assert self.is_element_present(*ProductPageLocators.SUCCESS_MESSAGE)
        actual_product_name = self.get_success_message_text()
        assert product_name == actual_product_name

    def should_be_correct_basket_total(self, product_price):
        assert self.is_element_present(*ProductPageLocators.BASKET_TOTAL_MESSAGE)
        actual_basket_total = self.get_basket_total_text()
        assert product_price == actual_basket_total

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE)

    def should_disappear_success_message(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE)