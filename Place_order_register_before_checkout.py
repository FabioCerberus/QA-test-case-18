#1. Launch browser
#2. Navigate to url 'http://automationexercise.com'
#3. Verify that home page is visible successfully
#4. Click 'Signup / Login' button
#5. Fill all details in Signup and create account
#6. Verify 'ACCOUNT CREATED!' and click 'Continue' button
#7. Verify ' Logged in as username' at top
#8. Add products to cart
#9. Click 'Cart' button
#10. Verify that cart page is displayed
#11. Click Proceed To Checkout
#12. Verify Address Details and Review Your Order
#13. Enter description in comment text area and click 'Place Order'
#14. Enter payment details: Name on Card, Card Number, CVC, Expiration date
#15. Click 'Pay and Confirm Order' button
#16. Verify success message 'Your order has been placed successfully!'
#17. Click 'Delete Account' button
#18. Verify 'ACCOUNT DELETED!' and click 'Continue' button

from QAStudy.Create_account import create_account
from playwright.sync_api import sync_playwright, expect

def test_place_order_register_before_checkout():
    with (sync_playwright() as p):
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()


        page.goto("https://automationexercise.com")
        expect(page).to_have_title("Automation Exercise")

        create_account(page)

        page.goto("https://automationexercise.com")


        # Choose which product to test
        product_index = 3

        # Save product card based on the chosen index
        product = page.locator(".single-products").nth(product_index)

        # Capture product ID to find the same product later in the cart
        product_id = product.locator(".productinfo a.add-to-cart").get_attribute("data-product-id")

        # Hover over selected product and click 'Add to cart'
        product.scroll_into_view_if_needed()
        product.hover()
        product.locator(".product-overlay a.add-to-cart").click()

        expect(page.locator("#cartModal")).to_be_visible()
        expect(page.locator("#cartModal").get_by_text("Added!")).to_be_visible()
        page.locator("#cartModal").get_by_role("button", name="Continue Shopping").click()

        page.locator("#header").get_by_role("link", name="Cart" ).click()

        expect(page).to_have_title("Automation Exercise - Checkout")

        page.locator("#do_action").locator(".check_out").click()

        expect(page.locator("#address_delivery").locator(".address_country_name")).to_contain_text("United States")

        expect(page.locator(f'a[href="/product_details/{product_id}"]')).to_be_visible()

        page.locator('[name="message"]').fill("Test Test")

        page.locator("#cart_items").get_by_role("link", name="Place Order").click()

        # 16. Enter payment details: Name on Card, Card Number, CVC, Expiration date
        page.locator('[data-qa="name-on-card"]').fill("Fabio Lacerda")
        page.locator('[data-qa="card-number"]').fill("123456789")
        page.locator('[data-qa="cvc"]').fill("123")
        page.locator('[data-qa="expiry-month"]').fill("12")
        page.locator('[data-qa="expiry-year"]').fill("2030")
        # 17. Click 'Pay and Confirm Order' button
        page.locator('[data-qa="pay-button"]').click()
        # 18. Verify success message 'Your order has been placed successfully!'
        expect(page.get_by_text("Congratulations! Your order has been confirmed!")).to_be_visible()

        # Use delete code from previous lesson
        page.get_by_role("link", name="Delete Account").click()

        # 18. Verify that 'ACCOUNT DELETED!' is visible and click 'Continue' button
        expect(page.get_by_text("Account Deleted!")).to_be_visible()
        page.locator('[data-qa="continue-button"]').click()

        browser.close()
