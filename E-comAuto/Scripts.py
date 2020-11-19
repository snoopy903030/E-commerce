from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import os.path
import csv



global wd
wd = webdriver.Firefox(executable_path="C:\\Webdriver\\geckodriver.exe")

def OpenURL(strURL):
    if strURL == "":
        strURL = "http://live.demoguru99.com/index.php/"
    wd.get(strURL)
    wd.implicitly_wait(20)

def CheckWindowTitle(strExpectedTitle):
    # use try except to avoid when assert stop running scripts
    try:
        assert wd.title == strExpectedTitle
        print("Expected Window opened as expected: "+strExpectedTitle)
    except AssertionError:
        print("Assertion failed. Actual window title is: "+ wd.title)


def FindElement(strMethod, strEleIdentify):
    if strMethod == "id":
        Element = wd.find_elements_by_id(strEleIdentify)
    if strMethod == "class":
        Element = wd.find_elements_by_class_name(strEleIdentify)
    if strMethod == "css_selector":
        Element = wd.find_elements_by_css_selector(strEleIdentify)
    elif strMethod == "xpath":
        Element = wd.find_elements_by_xpath(strEleIdentify)

    if (len(Element)>0 ):
        #print('Find the unique object web driver element successful.')
        return Element[0]
    else:
        print("The object selected in "+strMethod+ " ,"+ strEleIdentify+ ", doesn't exist.")
        return None

#Click Button by css_selector
def ClickBtn(strBtnName,strLocName, strLocValue):
    if strLocName == "css_selector":
        btn = FindElement("css_selector",strLocValue)
    if strLocName =="id":
        btn = FindElement("id",strLocValue)
    if strLocName == "xpath":
        btn = FindElement("xpath",strLocValue)
    if strLocName == "class":
        btn = FindElement("class",strLocValue)

    if btn!= None:
        #print("Find the Button "+strBtnName+" on the web page.")
        btn.click()
        print("Button: ["+strBtnName + "] clicked.")
    else:
        print("Can't find "+strBtnName+" Button on the web page.")


def SetDropdownMenubyName():
    dropdownSortBy = FindElement("css_selector",'.sort-by [title="Sort By"]')
    if (dropdownSortBy != None):
        print("Clisk Sort By Name")
        dropdownSortBy.send_keys("Name")
    else:
        print("The dropdown button can't be located!")


# Passing the strProductName, return the Object listItem
# This function will print all the product name
def GetProductInfo(strProductName):
    gridProducts = FindElement("css_selector",'.category-products .products-grid')
    if (gridProducts!=None):
        itemLists = wd.find_elements_by_css_selector('.category-products [class="item last"]')
        itemNames = wd.find_elements_by_css_selector(".category-products li .product-name")
        print("There are: "+ str(len(itemNames))+ " Items founded in the list.")

        listProductName = []

        print("-------------Start printing products info on the list---------------")
        for i in range(len(itemNames)):
            print("The product Name is: "+itemNames[i].text)
            # add Item Name to List for future use
            listProductName.append(itemNames[i].text)

            if (itemNames[i].text.lower() == strProductName.lower()):
                    listItem = itemLists[i]
        print("-----------------End of Product List------------------")

        # # sort product name alphabetically and print
        # listProductName.sort()
        # print("-----------------Product Sorted By Name as below----------------")
        # print(listProductName)

        #return List Item Object
        return listItem

#By passing the strProductName, return the Product Price
def GetProductPrice(strProductName):

    Item = GetProductInfo(strProductName)
    if Item != None:
        strItemPrice = Item.find_element_by_css_selector(".price-box .price").text
        print("The product " + strProductName + " 's price is " + strItemPrice)
        return strItemPrice
    else:
        print("Can't get the price as Product is None.")
        return None

#Close Google Ads window
def CloseGoogleAds():
    wd.switch_to.frame("flow_close_btn_iframe")
    ClickBtn("Close","id","closeBtn")
    wd.switch_to.default_content()

#Input Qty number and click update
def SetQty(strQty):
    textQty = wd.find_element_by_xpath("//*[@id=\"shopping-cart-table\"]/tbody/tr/td[4]/input")

    if (textQty!=None):
        textQty.clear()
        textQty.send_keys("1000")
        print("Find qty textbox and set it to 1000.")
    else:
        print("Can't find text box QTY")
    ClickBtn("Update","xpath","//*[@id=\"shopping-cart-table\"]//tbody/tr/td[4]/button")

#Verify if Shown messages is same as expected
def VerifyMessage(strExpectedMsg, strCSSValue):
    SuccessMessage = FindElement("css_selector",strCSSValue)
    if SuccessMessage != None:
        strSucMsg = SuccessMessage.text
        try:
            assert strExpectedMsg == strSucMsg
            print("Message is shown as expected: "+strSucMsg)
        except AssertionError:
            print('Something went wrong in assert.')
    else:
        print("Can't find success message!")

def AddtoCompare(strItemName):
    compareItem = GetProductInfo(strItemName)
    if compareItem != None:
        compareItem.find_element_by_css_selector(".link-compare").click()
    else:
        print("The item needs to add to compare is none.")

def TypetoInputBox(strLocName, StrLocValue, strType):
    InputBox = FindElement(strLocName, StrLocValue)
    if InputBox!= None:
        InputBox.send_keys(strType)
    else:
        print("Can't find InputBox!")

def AddtoWishlist(strItemName):
    wishlistItem = GetProductInfo(strItemName)
    if wishlistItem != None:
        wishlistItem.find_element_by_css_selector(".link-wishlist").click()
    else:
        print("The item needs to add to wishlist is none.")


# Login to My Account and verify if login successful
# Click My Account -> Login, input username and password
# Verify the Login Page window title
def LoginMyAccount(strUsername,strPassword):
    ClickBtn("My Account", "css_selector", '.account-cart-wrapper .skip-link')
    ClickBtn("Login", "css_selector", '#header-account li[class=" last"]')
    CheckWindowTitle("Customer Login")
    TypetoInputBox("css_selector", 'input[name="login[username]"]', strUsername)
    TypetoInputBox("css_selector", 'input[name="login[password]"]', strPassword)
    ClickBtn("Login", "css_selector", 'button[type="submit"][title="Login"]')
    CheckWindowTitle("My Account")

#Add all products in My Wishlist to shopping Cart and Click Proceed To Checkout
#Save the Total price without shipping fee for future use
def AddAllWishlishToCart():
    ClickBtn("My Account", "css_selector", '.account-cart-wrapper .skip-link')
    ClickBtn("My Wishlist", "css_selector", '#header-account [title*="My Wishlist"]')
    ClickBtn("Add All to Cart","css_selector",'button[title="Add All to Cart"]')
    # Save  cost without shipping fee
    strPrice = FindElement("css_selector",'.cart-totals .price').text
    print("Your Cart Total Price(without shipping fee) is "+strPrice)
    ClickBtn("Proceed to Checkout","css_selector",'button[title="Proceed to Checkout"]')
    return strPrice

#Filling Billing Info
def PutBillingInfo(strStreet,strCity,strRegion,strRegionCode,strZipcode,strCountry,strTele):
    # set to put new address
    radioAddress = FindElement("css_selector",'#billing-address-select')
    i=0
    if radioAddress!=None:
        selectAddress = Select(radioAddress)
        selectAddress.select_by_value('')
        i=1

    TypetoInputBox("css_selector",'#billing\:street1',strStreet)
    TypetoInputBox("css_selector",'#billing\:city',strCity)
    if i==0:
        TypetoInputBox("css_selector",'#billing\:region',strRegion)
    else:
        if (FindElement("css_selector", '#billing\:region_id') != None):
            selectRegion = Select(FindElement("css_selector", '#billing\:region_id'))
            selectRegion.select_by_value(strRegionCode) #43 Stands for new york

    TypetoInputBox("css_selector",'#billing\:postcode',strZipcode)
    CloseGoogleAds()

    if(FindElement("css_selector",'#billing\:country_id')!=None):
        selectCountry = Select(FindElement("css_selector",'#billing\:country_id'))
        selectCountry.select_by_value(strCountry)

    TypetoInputBox("css_selector",'#billing\:telephone',strTele)

    ClickBtn("Continue","css_selector",'#billing-buttons-container button[title="Continue"]')

#Get Shipping cost and verify if it's correct
#Return strShippingCost
def VerifyShippingCost(strExpectedCost):
    itemShippingCost = FindElement("css_selector",'#opc-shipping_method .price')
    if itemShippingCost != None:
        strShippingCost = itemShippingCost.text.replace('$','')
        print("The calculated shipping cost is: $"+strShippingCost)

        try:
            assert float(strShippingCost) == float(strExpectedCost)
            print("The shipping cost is correct.")

        except AssertionError:
            print("something went wrong in assert.")

    else:
        print("Can't find item ShippingCost.")
        return None

    ClickBtn("Continue","css_selector",'button[onclick="shippingMethod.save()"]')
    return strShippingCost

#Set Payment Method by Credit or Money
def SetPaymentMethod(strMethod):
    if strMethod.lower() == "credit":
        PaymentMethod = FindElement("css_selector",'.radio[name="payment[method]"][title*="Credit"]')
    if strMethod.lower() == "money":
        PaymentMethod = FindElement("css_selector", '.radio[name="payment[method]"][title*="Money"]')

    if PaymentMethod != None:
        PaymentMethod.click()
    else:
        print("Can't find radio Credit Payment Method.")

    ClickBtn("Continue","css_selector",'button[onclick="payment.save()"]')

#Work out total cost and place order
def CalculateTotalCost(strPricewoShipping, strShippingCost):

    print("The Total Product price is: "+ strPricewoShipping)
    print("The Shipping cost is: $" + strShippingCost)

    strPricewoShipping = strPricewoShipping.replace('$', '')

    strTotalPrice = FindElement("css_selector",'[class="a-right last"] strong .price').text.replace('$','')
    try:
        assert float(strPricewoShipping) + float(strShippingCost) == float(strTotalPrice)
        print("Calculated Total Price is: "+ strTotalPrice)
    except AssertionError:
        print("Something went wrong when check total price.")

    #Click Place Order
    ClickBtn("Place Order","css_selector",'button[title="Place Order"]')

#Verify order has been generated
def VerifyGeneratedOrder():
    strPageTitle = FindElement("css_selector",'.page-title').text
    if strPageTitle.lower() == "Your order has been received.".lower():
        itemOrderNo = wd.find_element_by_css_selector('.main p a')
        if itemOrderNo != None:
            print("The Order No is: "+itemOrderNo.text)
            return itemOrderNo.text
        else:
            print("Can't find item Order No. ")
    else:
        print("Can't find page title: Your order has been received. The actual one is: "+ strPageTitle)

def SelectSidebarMenu(strSelectedMenu):
    MenuBlock = FindElement("css_selector",'[class="block block-account"]')
    if MenuBlock!= None:
        MenuItems = MenuBlock.find_elements_by_css_selector('li')
        for i in range(len(MenuItems)):
            if ((MenuItems[i].text).lower() == strSelectedMenu.lower()):
                MenuItems[i].click()
                print("Menu Item "+ strSelectedMenu + " clicked.")
                return True
        print("Can't find Menu "+strSelectedMenu + " to click")
        return False
    else:
        print("Can't find Sidebar Menu.")
        return False

#In Recent Orders Table, Check Previous Order No, Status, and Click Button "View Orders" or "Reorder"
def GetPreviousOrderStatus(strOrderNo,strExpectedStatus,LinkBtnToClick):
    OrderTable = FindElement('css_selector','#my-orders-table')
    OrderNumber = FindElement('css_selector','#my-orders-table tbody .number')

    try:
        assert OrderNumber.text == strOrderNo
        print('Found Order Number: '+strOrderNo)
        OrderStatus = FindElement('css_selector', '#my-orders-table tbody .status')
        try:
            assert OrderStatus.text == strExpectedStatus
            print("Order Status is "+strExpectedStatus)
        except AssertionError:
            print('something went wrong when checking order status.')
    except AssertionError:
        print('something went wrong when checking order number.')

    if LinkBtnToClick == "View Order":
        LinkBtn = OrderTable.find_elements_by_css_selector('#my-orders-table tbody a')[0]
    if LinkBtnToClick == " Reorder":
        LinkBtn = OrderTable.find_elements_by_css_selector('#my-orders-table tbody a')[1]
    LinkBtn.click()


#Click Menu Items or SubMenuItem
#When only click the Menu Item, passing strSubMenuItem as None
def ClickMenuItem(strMenuItem, strSubMenuItem):
    Menuitems = wd.find_elements_by_css_selector('#nav [class*="parent level0"]')
    print('the length of the Menu is: %s' % len(Menuitems))
    for i in range(len(Menuitems)):
        MenuItemName = Menuitems[i].text
        if MenuItemName == strMenuItem:
            action = ActionChains(wd)
            action.move_to_element(Menuitems[i]).perform()
            if strSubMenuItem == None:
                Menuitems[i].click()
                return True
            SubMenuItems = wd.find_elements_by_css_selector('#nav li a span')
            if SubMenuItems != None:
                print("The length of Sub Menu Items: %s" % len(SubMenuItems))
                for a in range(len(SubMenuItems)):
                        print ("a is %s" % a)
                        SubMenuItemsName = SubMenuItems[a].text
                        print(SubMenuItemsName)
                        if SubMenuItemsName == strSubMenuItem:
                            SubMenuItems[a].click()
                            return True
                else:
                    print('Cannot find Sub Menu Item: '+ strSubMenuItem)
                    return False
            else:
                print('There is no Sub Menu Items object.')
                return False
    else:
        print('Cannot find Menu Item '+ strMenuItem)
        return False

#Read download file and display all info in console windows
def CheckFileExists(strFilePath):
    blResult = os.path.exists(strFilePath)
    if blResult == True:
        print("The file: "+ strFilePath+" is exist.")
    else:
        print("The file: "+ strFilePath+" is not exist.")

# # read csv file and print in console
# # add encoding = 'uft-8' to avoid the unicode decode error
def ReadCSVFile(strFilePath):
    with open(strFilePath, newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csv_reader:
            print(' '.join(row))




