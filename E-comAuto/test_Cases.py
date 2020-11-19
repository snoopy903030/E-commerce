import pytest
from Scripts import *
from selenium.webdriver.common.keys import Keys

class Test_Ecomcases:

    def setup_method(self):
        OpenURL("")

    #Varify items in Mobile list Page can be sorted by "Name“
    def test_Day1(self):
        CheckWindowTitle("Home page")
        ClickBtn("Mobile", "css_selector", '[href *="mobile.html"]')
        CheckWindowTitle("Mobile")   # Check window title has been switch to "Mobile"
        SetDropdownMenubyName()
        # Verify all product are sorted by Name

    #Varify the cost of product in list page and details page are equal
    def test_Day2(self):
        ClickBtn("Mobile", "css_selector", '[href *="mobile.html"]')
        strItemPrice = GetProductPrice("Sony Xperia")  # Get price and save

        # Click Product Name to go to details page
        ItemList = GetProductInfo("Sony Xperia")
        ItemList.find_element_by_css_selector('.product-image').click()

        # Check the window title of the details page
        CheckWindowTitle("Sony Xperia - Mobile")

        # Read the XPeria mobile price from details page
        DetailsPage_Pirce = FindElement("css_selector", ".price")
        print("The price on details page is " + DetailsPage_Pirce.text)
        try:
            assert DetailsPage_Pirce.text == strItemPrice
        except AssertionError:
            print("Something went wrong!")

    #Verify that you cannot add more product in cart than the product available in store
    def test_Day3(self):
        ClickBtn("Mobile", "css_selector", '[href *="mobile.html"]')

        #Click Add to Cart for Sony
        ItemList = GetProductInfo("Sony Xperia")
        CloseGoogleAds()  # Close Google Ads window
        ItemList.find_element_by_css_selector('button[title="Add to Cart"]').click()

        SetQty("1000")
        VerifyMessage("Some of the products cannot be ordered in requested quantity.",'.error-msg span')

        CloseGoogleAds() # Close Google Ads window

        # Click Button Empty Cart
        ClickBtn("Empty Cart", "id", "empty_cart_button")

        # Verify if the shopping cart is empty
        try:
            assert wd.find_element_by_class_name(
                "cart-empty").text == "You have no items in your shopping cart.\n" + "Click here to continue shopping."
            print("You shopping cart is empty now.")
        except AssertionError:
            print("something went wrong.")

    def test_Day4(self):
        ClickBtn("Mobile", "css_selector", '[href *="mobile.html"]')
        CloseGoogleAds()
        AddtoCompare("SONY XPERIA")
        CloseGoogleAds()
        AddtoCompare("IPHONE")
        ClickBtn("Compare", "css_selector", ".main .block .actions .button")

        time.sleep(5)
        main_window = wd.current_window_handle

        # switch to New Window
        for handle in wd.window_handles:
            wd.switch_to.window(handle)
            print(wd.title)
            if 'Products Comparison List' in wd.title:
                CheckWindowTitle("Products Comparison List - Magento Commerce")
                break
        ClickBtn("Close Window", "css_selector", 'button[title="Close Window"]')
        wd.switch_to.window(main_window)


    def test_Day5(self):

        # Login to My Account and verify if login successful
        LoginMyAccount('cathywhver@gmail.com', '903030')

        # Go to Tv Page, Add LG LCD to Wish list
        ClickBtn("TV", "css_selector", '#nav [class="level0 nav-2 last"]')
        AddtoWishlist("LG LCD")
        ClickBtn("Share wish list", "css_selector", 'button[title="Share Wishlist"]')

        # In the new page, input email address and messages and click button 'Share Wishlist
        TypetoInputBox("css_selector", '.input-box #email_address', 'cathywhver@gmail.com')
        TypetoInputBox("css_selector", '.input-box #message', "This is a test for wish list.")
        ClickBtn("Share Wishlist", "css_selector", 'button[title="Share Wishlist"]')

        VerifyMessage('Your Wish list has been shared.', '.messages .success-msg')

    def test_Day6(self):
        LoginMyAccount('cathywhver@gmail.com', '903030')
        strPrice = AddAllWishlishToCart()
        PutBillingInfo('ABC Street', 'New York', 'New York', "43", '542396', 'US', '12345678')
        strShippingCost = VerifyShippingCost(5)

        SetPaymentMethod("Money")
        CalculateTotalCost(strPrice, strShippingCost)
        time.sleep(5)
        VerifyGeneratedOrder()

    def test_Day7(self):
        LoginMyAccount('cathywhver@gmail.com', '903030')
        SelectSidebarMenu("My Orders")
        GetPreviousOrderStatus('100013211', 'Pending', 'View Order')
        ClickBtn("Print Order", "css_selector", '.link-print')
        time.sleep(5)
        main_window = wd.current_window_handle

        # switch to New Window
        for handle in wd.window_handles:
            wd.switch_to.window(handle)
            if 'Print Order' in wd.title:
                CheckWindowTitle("Print Order # " + '100013211')
                break
        wd.close()
        wd.switch_to.window(main_window)

    def test_Day8(self):
        ClickBtn("Mobile", "css_selector", '[href *="mobile.html"]')

        # Add  Iphone to Cart
        ItemList = GetProductInfo("Iphone")
        ItemList.find_element_by_css_selector('button[title="Add to Cart"]').click()
        TypetoInputBox('css_selector', '#coupon_code', 'GURU50')
        ClickBtn("Apply", 'css_selector', 'button[title="Apply"]')
        Items = wd.find_elements_by_css_selector('.cart-totals tbody tr td')
        strWholePrice = Items[1].text.replace('$', '')

        if Items[2].text.startswith('DISCOUNT'):
            print('Found Discount rows.')

        strDisAmount = Items[3].text.replace("-$", "")
        assert float(strWholePrice) * float(0.05) == float(strDisAmount)

class Test_Ecom_Backend:

    #Export csv file and read in console
    def test_Day9(self):

        # Login to backend
        OpenURL("http://live.demoguru99.com/index.php/backendlogin/index/index/key/878beb4c9acc9346cd394145d8b2c01c/")
        TypetoInputBox('id', 'username', 'user01')
        TypetoInputBox('id', 'login', 'guru99com')
        ClickBtn("Login", 'css_selector', '.form-button[title="Login"]')

        # Close popup messages
        FindElement('css_selector', '[onclick="closeMessagePopup(); return false;"]').click()

        # Go to Sales->Order
        ClickMenuItem('Sales', 'Orders')

        # Export Orders as CSV file
        Format = FindElement('id', 'sales_order_grid_export')
        selectFormat = Select(Format)
        selectFormat.select_by_visible_text("CSV")
        ClickBtn("Export", 'css_selector', 'button[title="Export"]')

        #Handle system dialog
        action = ActionChains(wd)
        action.send_keys(Keys.ALT, "s").perform()
        action.send_keys(Keys.ENTER).perform()

        #Read CSV file in console
        # CheckFileExists('C:\\Users\\cathy\\Downloads\\orders.csv')
        # ReadCSVFile('C:\\Users\\cathy\\Downloads\\orders.csv')