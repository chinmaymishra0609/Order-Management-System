from ims import app, mail
from flask import render_template, redirect, flash, url_for, jsonify, request, make_response, session
from sqlalchemy import and_, or_, inspect
from flask_mail import Message
from models import *
from functools import wraps
# from werkzeug import secure_filename
import requests, json, pdfkit, os

# def loginRequired(f):
#    @wraps(f)
#    def wraps(*args, **kwargs):
#       if(('ADMIN' in session) or ('CASHIER' in session)):
#          return jsonify(status="success")         
#       else:
#          return jsonify(status="danger", statusMessage="Please login to proceed.")
#       return wraps

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @loginRequired
def index():
   return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
   return render_template('order.html')

@app.route('/dynamicCustomerName', methods=['GET', 'POST'])
def dynamicCustomerName():
   if request.method == "POST":
      info = ""
      if(None != request.form.get("orderCustomerName") or (None != request.form.get("updateCustomerName")) or (None != request.form.get("orderDetailsCustomerName"))):
         if(None != request.form.get("orderCustomerName")):
            customerName = request.form.get("orderCustomerName").upper()
         
         if(None != request.form.get("updateCustomerName")):
            customerName = request.form.get("updateCustomerName").upper()
         
         if(None != request.form.get("orderDetailsCustomerName")):
            customerName = request.form.get("orderDetailsCustomerName").upper()
         
         allCustomerName = db.session.query(Customer.customerName, Customer.customerContact).filter(Customer.customerName.like('%'+ customerName +'%')).all()
         if(0 != len(allCustomerName)):
            allCustomerName = [(customerName[0].title(), customerName[1]) for customerName in allCustomerName]
            info = jsonify(allCustomerName=allCustomerName)

      if(None != request.form.get("orderDetailsCustomerContact")):
         allCustomerName = db.session.query(Customer.customerName, Customer.customerContact).filter(Customer.customerContact.like('%'+ request.form.get("orderDetailsCustomerContact") +'%')).all()
         if(0 != len(allCustomerName)):
            allCustomerName = [(customerName[0].title(), customerName[1]) for customerName in allCustomerName]
            info = jsonify(allCustomerName=allCustomerName)

      if(None != request.form.get("orderDetailsCustomerEmail")):
         allCustomerEmail = db.session.query(Customer.customerEmail).filter(Customer.customerEmail.like('%'+ request.form.get("orderDetailsCustomerEmail").upper() +'%')).all()
         if(0 != len(allCustomerEmail)):
            allCustomerName = [(customerEmail[0].lower()) for customerEmail in allCustomerEmail]
            info = jsonify(allCustomerName=allCustomerName)

      if(None != request.form.get("searchReceptionistName")):
         allReceptionistName = db.session.query(Receptionist.receptionistName, Receptionist.receptionistContact).filter(Receptionist.receptionistName.like('%'+ request.form.get("searchReceptionistName").upper() +'%')).all()
         if(None != allReceptionistName):
            allReceptionistName = [(receptionistName[0].title(), receptionistName[1]) for receptionistName in allReceptionistName]
            info = jsonify(allReceptionistName=allReceptionistName)
      return info

@app.route('/dataOrderNumber', methods=['GET', 'POST'])
def dataOrderNumber():
   if request.method == "POST":
      if(None != request.form.get("orderNumber")):
         orderDetails = {}
         query = db.session.query(Customer, Order.orderDate, Order.orderTotal, Order.orderNetPaid, Order.orderStatus, OrderProduct.productQuantity, Product.productName, Product.productSellPrice, Product.productDiscount).join(Order, Customer.customerID==Order.customerID).join(OrderProduct, Order.orderID==OrderProduct.orderID).join(Product, OrderProduct.productID==Product.productID).filter(and_(Customer.customerID==Order.customerID, Order.orderID==OrderProduct.orderID, Order.orderID==request.form.get('orderNumber'))).all()
         if(0 != len(query)):
            orderDetails['orderDetailsCustomerName'] = (query[0].Customer.customerName).title()
            orderDetails['orderDetailsCustomerEmail'] = (query[0].Customer.customerEmail).lower()
            orderDetails['orderDetailsCustomerContact'] = query[0].Customer.customerContact
            orderDetails['orderDetailsCustomerZip'] = query[0].Customer.customerZip
            orderDetails['orderDetailsCustomerCity'] = (query[0].Customer.customerCity).title()
            orderDetails['orderDetailsCustomerDistrict'] = (query[0].Customer.customerDistrict).title()
            orderDetails['orderDetailsCustomerState'] = (query[0].Customer.customerState).title()
            orderDetails['orderDetailsCustomerCountry'] = (query[0].Customer.customerCountry).title()
            orderDetails['orderDetailsCustomerDues'] = str(query[0].Customer.customerDues)
            orderDetails['orderDetailsCustomerDiscount'] = str(query[0].Customer.customerDiscount)
            orderDetails['orderDetailsOrderDate'] = str(query[0].orderDate)
            orderDetails['orderDetailsNetPaid'] = str(query[0].orderNetPaid)
            orderDetails['orderDetailsOrderStatus'] = query[0].orderStatus.title()
            orderDetails['productDetails'] = []
            for que in query:
               orderDetails['productDetails'].append({"productName" : que.productName.title(), "productQuantity" : que.productQuantity, "productSellPrice" : str(que.productSellPrice), "productDiscount" : str(que.productDiscount), "productNetPrice" : str(float(que.productSellPrice)  - float(que.productDiscount))})
            return jsonify(orderDetails=orderDetails)
         else:
            return jsonify(statusMessage=f"Order number {request.form.get('orderNumber')} is not available.", status="danger")
      
      if(None != request.form.get("dueOrderNumber")):
         dueClearDetails = {}
         query = db.session.query(Customer.customerDues, CashReceipt).join(Order).join(CashReceipt).filter(CashReceipt.dueOrderID==request.form.get("dueOrderNumber")).all()
         if(None != query):
            dueClearDetails['customerDues'] = str(query[0].customerDues)
            dueClearDetails['cashReceiptID'] = str(query[0].CashReceipt.cashReceiptID)
            dueClearDetails['duePaidDate'] = str(query[0].CashReceipt.duePaidDate)
            dueClearDetails['duePaidAmount'] = str(query[0].CashReceipt.duePaidAmount)
            dueClearDetails['duePaidMode'] = str(query[0].CashReceipt.duePaidMode)
            dueClearDetails['dueReceivedFrom'] = str(query[0].CashReceipt.dueReceivedFrom)
            dueClearDetails['dueReceivedBy'] = str(query[0].CashReceipt.dueReceivedBy)
            dueClearDetails['digitalSign'] = str(query[0].CashReceipt.digitalSign)            
            return jsonify(dueClearDetails=dueClearDetails)

@app.route('/customerDetailsFill', methods=['GET', 'POST'])
def customerDetailsFill():
   if request.method == "POST":
      customerDetails = {}
      if(None != request.form.get("orderCustomerName")):
         customerInfo = Customer.query.filter(and_(Customer.customerName==request.form.get('orderCustomerName').upper(), Customer.customerContact==request.form.get('orderCustomerContact'))).first()
         if(None != customerInfo):
            customerDetails['oldCustomerName'] = (customerInfo.customerName).title()
            customerDetails['oldCustomerEmail'] = (customerInfo.customerEmail).lower()
            customerDetails['oldCustomerContact'] = (customerInfo.customerContact).title()
            customerDetails['oldCustomerZip'] = (customerInfo.customerZip).title()
            customerDetails['oldCustomerCity'] = (customerInfo.customerCity).title()
            customerDetails['oldCustomerDistrict'] = (customerInfo.customerDistrict).title()
            customerDetails['oldCustomerState'] = (customerInfo.customerState).title()
            customerDetails['oldCustomerCountry'] = (customerInfo.customerCountry).title()
            customerDetails['oldCustomerDues'] = str(customerInfo.customerDues)
            customerDetails['oldCustomerDiscount'] = str(customerInfo.customerDiscount)
            return jsonify(customerDetails=customerDetails)
         else:
            return jsonify(statusMessage=f"Customer {request.form.get('orderCustomerName').title()} is not available.", status="danger")
      
      if(None != request.form.get("updateCustomerName")):
         customerInfo = Customer.query.filter(and_(Customer.customerName==request.form.get('updateCustomerName').upper(), Customer.customerContact==request.form.get('updateCustomerContact'))).first()
         if(None != customerInfo):
            customerDetails['updateCustomerName'] = (customerInfo.customerName).title()
            customerDetails['updateCustomerEmail'] = (customerInfo.customerEmail).lower()
            customerDetails['updateCustomerContact'] = (customerInfo.customerContact).title()
            customerDetails['updateCustomerZip'] = (customerInfo.customerZip).title()
            customerDetails['updateCustomerCity'] = (customerInfo.customerCity).title()
            customerDetails['updateCustomerDistrict'] = (customerInfo.customerDistrict).title()
            customerDetails['updateCustomerState'] = (customerInfo.customerState).title()
            customerDetails['updateCustomerCountry'] = (customerInfo.customerCountry).title()
            return jsonify(customerDetails=customerDetails)
         else:
            return jsonify(statusMessage=f"Customer {request.form.get('updateCustomerName').title()} is not available.", status="danger")

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == "POST":
      if(None != request.form.get('newCustomerName')):
         customerExist = Customer.query.filter_by(customerEmail=request.form.get('newCustomerEmail').upper()).first()
         if (None == customerExist):
            newCustomer = Customer(
               customerName = request.form.get('newCustomerName').upper(),
               customerEmail = request.form.get('newCustomerEmail').upper(),
               customerContact = request.form.get('newCustomerContact'),
               customerZip = request.form.get('newCustomerZip'),
               customerCity = request.form.get('newCustomerCity').upper(),
               customerDistrict = request.form.get('newCustomerDistrict').upper(),
               customerState = request.form.get('newCustomerState').upper(),
               customerCountry = request.form.get('newCustomerCountry').upper()
            )
            db.session.add(newCustomer)
            db.session.commit()
            return jsonify(statusMessage=f"Hi {request.form.get('newCustomerName').title()}! Registration successfully completed.", status="success")
         else:
            return jsonify(statusMessage=f"Customer is alereay exist with email address {request.form.get('newCustomerEmail').upper()}.", status="danger")
      
      if(None != request.form.get('datalistUpdateCustomerName')):
         updateCustomerInfo = Customer.query.filter(and_(Customer.customerName==request.form.get('datalistUpdateCustomerName'), Customer.customerContact==request.form.get('customerContact'))).first()
         if(None != updateCustomerInfo):
            emailExist = Customer.query.filter(and_(Customer.customerEmail==request.form.get('updateCustomerEmail').upper(), Customer.customerName!=request.form.get('datalistUpdateCustomerName'), Customer.customerContact!=request.form.get('customerContact'))).first()
            if(None == emailExist):
               updateCustomerInfo.customerName = request.form.get('updateCustomerName').upper(),
               updateCustomerInfo.customerEmail = request.form.get('updateCustomerEmail').upper(),
               updateCustomerInfo.customerContact = request.form.get('updateCustomerContact'),
               updateCustomerInfo.customerZip = request.form.get('updateCustomerZip'),
               updateCustomerInfo.customerCity = request.form.get('updateCustomerCity').upper(),
               updateCustomerInfo.customerDistrict = request.form.get('updateCustomerDistrict').upper(),
               updateCustomerInfo.customerState = request.form.get('updateCustomerState').upper(),
               updateCustomerInfo.customerCountry = request.form.get('updateCustomerCountry').upper()
               db.session.commit()

               customerDetails = {}
               customerDetails['updateCustomerName'] = updateCustomerInfo.customerName.title()
               customerDetails['updateCustomerEmail'] = updateCustomerInfo.customerEmail.lower()
               customerDetails['updateCustomerContact'] = updateCustomerInfo.customerContact
               customerDetails['updateCustomerZip'] = updateCustomerInfo.customerZip.title()
               customerDetails['updateCustomerCity'] = updateCustomerInfo.customerCity.title()
               customerDetails['updateCustomerDistrict'] = updateCustomerInfo.customerDistrict.title()
               customerDetails['updateCustomerState'] = updateCustomerInfo.customerState.title()
               customerDetails['updateCustomerCountry'] = updateCustomerInfo.customerCountry.title()
               return jsonify(statusMessage=f"Hi {updateCustomerInfo.customerName.title()}! Information successfully updated.", status="success", customerDetails=customerDetails)
            else:
               return jsonify(statusMessage=f"Customer is alereay exist with email address {request.form.get('updateCustomerEmail').upper()}.", status="danger")
         else:
            return jsonify(statusMessage=f"Customer {request.form.get('datalistUpdateCustomerName').title()} is not available.", status="danger")

@app.route('/pincode', methods=['GET', 'POST'])
def pincode():
   if request.method == "POST":
      pincode = request.form.get('pincode')
      url = f"http://postalpincode.in/api/pincode/{pincode}"
      resp = requests.get(url)
      return jsonify({'result' : resp.json()})

@app.route('/product', methods=['GET', 'POST'])
def product():
   if request.method == "POST":
      newProduct = Product(
         productName = request.form.get('newProductName').upper(),
         productCostPrice = request.form.get('newProductCostPrice'),
         productSellPrice = request.form.get('newProductSellPrice'),
         productQuantity = request.form.get('newProductQuantity')
      )
      productExist = Product.query.filter_by(productName=request.form.get('newProductName').upper()).first()
      if (None != productExist):
         flash(f"{request.form.get('newProductName')} is already available.", "warning")
         return redirect(url_for('product'))
      else:
         db.session.add(newProduct)
         db.session.commit()
         flash(f"{request.form.get('newProductName')} added successfully.", "success")
         return redirect(url_for('product'))
   return render_template('product.html')

@app.route('/dynamicProductName', methods=['GET', 'POST'])
def dynamicProductName():   
   if request.method == "POST":
      if(None != request.form.get("orderProductName")):
         productName = request.form.get("orderProductName").upper()
      
      if(None != request.form.get("updateProductName")):
         productName = request.form.get("updateProductName").upper()
   
      allProductName = db.session.query(Product.productName).filter(Product.productName.like('%'+ productName +'%')).all()
      allProductName = [productName[0].title() for productName in allProductName]
      return jsonify(allProductName=allProductName)

@app.route('/productAdd', methods=['GET', 'POST'])
def productAdd():
   if request.method == "POST":
      productDetails = {}      
      if(None != request.form.get('newProductName')):
         productExist = Product.query.filter_by(productName=request.form.get('newProductName').upper()).first()
         if (None != productExist):
            return jsonify(statusMessage=f"{request.form.get('newProductName').title()} is already stored.", status="danger")
         else:
            newProduct = Product(
               productName=request.form.get('newProductName').upper(),
               productCostPrice=request.form.get('newProductCostPrice'),
               productSellPrice=request.form.get('newProductSellPrice'),
               productQuantity=request.form.get('newProductQuantity'),
               productDiscount=request.form.get('newProductDiscount')
            )
            db.session.add(newProduct)
            db.session.commit()
            return jsonify(statusMessage=f"{request.form.get('newProductName').title()} successfully stored.", status="success")
      
      if((None != request.form.get('updateProductName')) and (None == request.form.get('datalistProductName'))):
         updateProduct = Product.query.filter_by(productName=request.form.get('updateProductName').upper()).first()
         if (None != updateProduct):
            productDetails["updateProductName"] = updateProduct.productName.title()
            productDetails["updateProductCostPrice"] = str(updateProduct.productCostPrice)
            productDetails["updateProductSellPrice"] = str(updateProduct.productSellPrice)
            productDetails["updateProductQuantity"] = str(updateProduct.productQuantity)
            productDetails["updateProductDiscount"] = str(updateProduct.productDiscount)
            return jsonify(productDetails=productDetails)
         else:
            return jsonify(statusMessage=f"Product {request.form.get('updateProductName').title()} is not avaialble.", status="danger")
      
      if((None != request.form.get('updateProductName')) and (None != request.form.get('datalistProductName'))):
         appendProduct = Product.query.filter_by(productName=request.form.get('datalistProductName').upper()).first()
         if (None != appendProduct):
            appendProduct.productName=request.form.get('updateProductName').upper(),
            appendProduct.productCostPrice=request.form.get('updateProductCostPrice'),
            appendProduct.productSellPrice=request.form.get('updateProductSellPrice'),
            appendProduct.productQuantity=request.form.get('updateProductQuantity'),
            appendProduct.productDiscount=request.form.get('updateProductDiscount')
            db.session.commit()
            
            productDetails["updateProductName"] = appendProduct.productName.title()
            productDetails["updateProductCostPrice"] = str(appendProduct.productCostPrice)
            productDetails["updateProductSellPrice"] = str(appendProduct.productSellPrice)
            productDetails["updateProductQuantity"] = str(appendProduct.productQuantity)
            productDetails["updateProductDiscount"] = str(appendProduct.productDiscount)
            return jsonify(statusMessage=f"{appendProduct.productName.title()} information successfully updated.", status="success", productDetails=productDetails)
         else:
            return jsonify(statusMessage=f"Product {request.form.get('datalistProductName').title()} is not avaialble.", status="danger")

@app.route('/orderAdd', methods=['GET', 'POST'])
def orderAdd():
   if request.method == "POST":
      if(None != request.form.get('orderProductName')):
         orderProduct = Product.query.filter_by(productName=request.form.get('orderProductName').upper()).first()
         if(None != orderProduct):
            productDetails = {}
            productDetails['productSellPrice'] = str(orderProduct.productSellPrice)
            productDetails['productDiscount'] = str(orderProduct.productDiscount)      
            return jsonify(productDetails=productDetails)
         else:
            return jsonify(statusMessage=f"Product {request.form.get('orderProductName').title()} is not available in stock.", status="danger")

@app.route('/orderBuy', methods=['GET', 'POST'])
def orderBuy():
   if request.method == "POST":
      productJSON = json.loads(request.form.get("productJSON"))      
      customerInfo = Customer.query.filter(and_(Customer.customerName==productJSON["printPageOrderCustomerName"], Customer.customerContact==productJSON["printPageOrderCustomerContact"])).first()      
      if(None != customerInfo):
         customerInfo.customerDues = productJSON["dueAmount"]
         customerInfo.customerDiscount = float(customerInfo.customerDiscount) + float(productJSON["orderDiscount"])
         db.session.commit()
      
      if (float(productJSON["orderNetPaid"]) == (float(productJSON["orderTotal"]) - float(productJSON["orderDiscount"]))):
         status = "COMPLETED"
      elif (float(productJSON["orderNetPaid"]) != (float(productJSON["orderTotal"]) - float(productJSON["orderDiscount"]))):
         status = "PENDING"
         
      newOrder = Order(
         customerID = customerInfo.customerID,
         orderDiscount = productJSON["orderDiscount"],
         orderTotal = float(productJSON["orderTotal"]),
         orderNetPaid = float(productJSON["orderNetPaid"]),
         orderStatus = status
      )
      db.session.add(newOrder)
      db.session.commit()
      orderNumber = newOrder.orderID
      addInCartProduct = []

      for i in range(len(productJSON["productName"])):
         product = "product" + str(i+1)
         productInfo = Product.query.filter_by(productName=productJSON["productName"][product][0]).first()
         if(None != productInfo):
            productInfo.productQuantity = int(productInfo.productQuantity) - int(productJSON["productName"][product][1])
            db.session.commit()
   
         orderProduct = product
         orderProduct = OrderProduct(
            orderID = orderNumber,
            productID = productInfo.productID,
            productQuantity = productJSON["productName"][product][1],
            productStatus = "COMPLETED"
         )
         addInCartProduct.append(orderProduct)
      db.session.bulk_save_objects(addInCartProduct)
      db.session.commit()      
      return jsonify(orderNumber=orderNumber, status=status.title())

@app.route('/orderCancel', methods=['GET', 'POST'])
def orderCancel():
   if request.method == "POST":
         productJSON = json.loads(request.form.get("productJSON"))      
         customerInfo = Customer.query.filter(and_(Customer.customerName==productJSON["printPageOrderCustomerName"], Customer.customerContact==productJSON["printPageOrderCustomerContact"])).first()      
         if(None != customerInfo):
            customerInfo.customerDues = float(customerInfo.customerDues) - ((float(productJSON["orderTotal"]) - float(productJSON["orderDiscount"]) - float(productJSON["orderNetPaid"])))
            customerInfo.customerDiscount = float(customerInfo.customerDiscount) - float(productJSON["orderDiscount"])
            db.session.commit()

            orderInfo = Order.query.filter(Order.orderID==productJSON["orderNumber"]).first()
            if(None != orderInfo):
               orderInfo.orderStatus = "CANCELLED"
               db.session.commit()

               for i in range(len(productJSON["productName"])):
                  product = "product" + str(i+1)
                  productInfo = Product.query.filter_by(productName=productJSON["productName"][product][0]).first()
                  if(None != productInfo):
                     productInfo.productQuantity = int(productInfo.productQuantity) + int(productJSON["productName"][product][1])
                     db.session.commit()
            
                  orderProductInfo = OrderProduct.query.filter_by(orderID=productJSON["orderNumber"]).all()
                  if(None != orderProductInfo):
                     for ordProductInfo in orderProductInfo:
                        ordProductInfo.productStatus = "CANCELLED"
                        db.session.commit()      
               return jsonify(status="success", statusMessage="Order successfully cancelled.")

@app.route('/orderCancelDetails', methods=['GET', 'POST'])
def orderCancelDetails():
   if request.method == "POST":
      if((None != request.form.get('cancelOrderNumber')) and (None == request.form.get("cancelProductName")) and (None == request.form.get('cancelProductQuantity'))):
         orderCancelQuery = db.session.query(Customer.customerName, Customer.customerContact, Customer.customerZip, Customer.customerCity, Customer.customerState, Order.orderDate, Order.orderStatus, OrderProduct.productQuantity, Product.productName, Product.productSellPrice, Product.productDiscount).join(Order, Customer.customerID==Order.customerID).join(OrderProduct, Order.orderID==OrderProduct.orderID).join(Product, OrderProduct.productID==Product.productID).filter(Order.orderID==request.form.get("cancelOrderNumber")).all()
         if(0 != len(orderCancelQuery)):
            orderCancelDetails = {}
            orderCancelDetails['customerName'] = orderCancelQuery[0].customerName
            orderCancelDetails['customerContact'] = orderCancelQuery[0].customerContact
            orderCancelDetails['customerZip'] = orderCancelQuery[0].customerZip
            orderCancelDetails['customerCity'] = orderCancelQuery[0].customerCity.title()
            orderCancelDetails['customerState'] = orderCancelQuery[0].customerState.title()
            orderCancelDetails['orderDate'] = str(orderCancelQuery[0].orderDate).title()
            orderCancelDetails['orderStatus'] = str(orderCancelQuery[0].orderStatus).title()
            orderCancelDetails['productDetails'] = []
            for orderCancelQue in orderCancelQuery:
               orderCancelDetails['productDetails'].append({"productName" : orderCancelQue.productName.title(), "productQuantity" : orderCancelQue.productQuantity, "productSellPrice" : str(orderCancelQue.productSellPrice), "productDiscount" : str(orderCancelQue.productDiscount), "productNetPrice" : str(float(orderCancelQue.productSellPrice)  - float(orderCancelQue.productDiscount))})
            cancelOrderNumber = ""
            return jsonify(orderCancelDetails=orderCancelDetails)
         else:
            return jsonify(status='danger', statusMessage="No recored found for this order number.")                        

      if((None != request.form.get('cancelOrderNumber')) and (None != request.form.get("cancelProductName")) and (None != request.form.get('cancelProductQuantity'))):
         cancelProductQuantityDetails = db.session.query(OrderProduct.productQuantity, Product.productName).join(Product, Product.productID==OrderProduct.productID).join(Order, Order.orderID==OrderProduct.productID).filter(and_(Product.productName==request.form.get("cancelProductName").upper(), Order.orderID==request.form.get('cancelOrderNumber'))).all()
         if(0 != len(cancelProductQuantityDetails)):
            if(cancelProductQuantityDetails[0].productQuantity < int(request.form.get('cancelProductQuantity'))):
               return jsonify(status="danger", statusMessage="Cancel product quantity must not be greater than purchased product quantity.", purchasedQuantity=cancelProductQuantityDetails[0].productQuantity)
            if(0 == int(request.form.get('cancelProductQuantity'))):
               return jsonify(status="danger", statusMessage="Cancel product quantity must not be 0.", purchasedQuantity=cancelProductQuantityDetails[0].productQuantity)

@app.route('/receptionist', methods=['GET', 'POST'])
def receptionist():
   return render_template('receptionist.html')

@app.route('/receptionistDetails', methods=['GET', 'POST'])
def receptionistDetails():
   if request.method == "POST":
      if((None != request.form.get("receptionistName")) and (None != request.form.get("receptionistEmail")) and (None != request.form.get("receptionistContact")) and (None != request.form.get("receptionistPassword")) and (None != request.form.get("receptionistRole")) and (None != request.form.get("receptionistStatus")) and (None != request.form.get("receptionistDigitalSign"))):
         receptionistExist = db.session.query(Receptionist.receptionistEmail).filter(Receptionist.receptionistEmail==request.form.get("receptionistEmail").upper()).all()         
         if(0 == len(receptionistExist)):
            newrRceptionist = Receptionist(
               receptionistName = request.form.get("receptionistName").upper(),
               receptionistEmail = request.form.get("receptionistEmail").upper(),
               receptionistContact = request.form.get("receptionistContact"),
               receptionistPassword = request.form.get("receptionistPassword"),
               receptionistDigitalSign =  request.form.get("receptionistDigitalSign"),
               receptionistRole = request.form.get("receptionistRole").upper(),
               receptionistStatus = request.form.get("receptionistStatus").upper()            
            )
            db.session.add(newrRceptionist)
            db.session.commit()
            return jsonify(status="success", statusMessage=f"Hi Receptionist {request.form.get('receptionistName').title()}! Registration successfully completed.")
         else:
            return jsonify(status="danger", statusMessage=f"Receptionist already registered with email address {request.form.get('receptionistEmail').upper()}.")
      if((None != request.form.get("searchReceptionistName")) and (None != request.form.get("searchReceptionistContact"))):
         newReceptionistQuery = Receptionist.query.filter(and_(Receptionist.receptionistName==request.form.get("searchReceptionistName").upper()), Receptionist.receptionistContact==request.form.get("searchReceptionistContact")).all()
         if(0 != len(newReceptionistQuery)):
            newReceptionistDetails = {}
            newReceptionistDetails["receptionistName"] = newReceptionistQuery[0].receptionistName.title()
            newReceptionistDetails["receptionistEmail"] = newReceptionistQuery[0].receptionistEmail.lower()
            newReceptionistDetails["receptionistContact"] = newReceptionistQuery[0].receptionistContact
            newReceptionistDetails["receptionistPassword"] = newReceptionistQuery[0].receptionistPassword
            newReceptionistDetails["receptionistConfirmPassword"] = newReceptionistQuery[0].receptionistPassword
            newReceptionistDetails["receptionistDigitalSign"] = newReceptionistQuery[0].receptionistDigitalSign
            newReceptionistDetails["receptionistRole"] = newReceptionistQuery[0].receptionistRole.lower()
            newReceptionistDetails["receptionistStatus"] = newReceptionistQuery[0].receptionistStatus.lower()
            return jsonify(newReceptionistDetails=newReceptionistDetails)
         else:
            return jsonify(status="danger", statusMessage=f'Receptionist {request.form.get("searchReceptionistName")} is not available.')
      if((None != request.form.get("datalistReceptionistName")) and (None != request.form.get("datalistReceptionistContact"))):
         updateReceptionistQuery = Receptionist.query.filter(and_(Receptionist.receptionistName==request.form.get("datalistReceptionistName").upper()), Receptionist.receptionistContact==request.form.get("datalistReceptionistContact")).all()
         if(0 != len(updateReceptionistQuery)):
            updateReceptionistQuery[0].receptionistName = request.form.get("receptionistName").upper()
            updateReceptionistQuery[0].receptionistEmail = request.form.get("receptionistEmail").upper().lower()
            updateReceptionistQuery[0].receptionistContact = request.form.get("receptionistContact")
            updateReceptionistQuery[0].receptionistPassword = request.form.get("receptionistPassword")
            updateReceptionistQuery[0].receptionistRole = request.form.get("receptionistRole").upper()
            updateReceptionistQuery[0].receptionistStatus = request.form.get("receptionistStatus").upper()
            db.session.commit()

            updateReceptionistDetails = {}
            updateReceptionistDetails["receptionistName"] = updateReceptionistQuery[0].receptionistName.title()
            updateReceptionistDetails["receptionistEmail"] = updateReceptionistQuery[0].receptionistEmail.lower()
            updateReceptionistDetails["receptionistContact"] = updateReceptionistQuery[0].receptionistContact
            updateReceptionistDetails["receptionistPassword"] = updateReceptionistQuery[0].receptionistPassword
            updateReceptionistDetails["receptionistRole"] = updateReceptionistQuery[0].receptionistRole.lower()
            updateReceptionistDetails["receptionistStatus"] = updateReceptionistQuery[0].receptionistStatus.lower()
            return jsonify(updateReceptionistDetails=updateReceptionistDetails, status="success", statusMessage=f'Hi {request.form.get("receptionistName").title()}! Record successfully updated.')

@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
   session.clear()
   gc.collect()
   return jsonify(status="success", statusMessage="You have logout successfully.")

@app.route('/receptionistLogin', methods=['GET', 'POST'])
def receptionistLogin():
   if request.method == "POST":
      if((None != request.form.get("receptionistEmail")) and (None != request.form.get("receptionistPassword"))):
         query = db.session.query(Receptionist.receptionistEmail, Receptionist.receptionistPassword, Receptionist.receptionistRole).filter(and_(Receptionist.receptionistEmail==request.form.get("receptionistEmail").upper(), Receptionist.receptionistPassword== request.form.get("receptionistPassword").upper())).all()
         if(0 != len(query)):
            if("ADMIN" == query[0].receptionistRole):
               session['ADMIN'] = "ADMIN"
            elif("CASHIER" == query[0].receptionistRole):
               session['CASHIER'] = "CASHIER"
            return jsonify(status="success")
         else:         
            return jsonify(status="danger", statusMessage=f"Invalid credentials.")

@app.route('/dueClear', methods=['GET', 'POST'])
def dueClear():
   return render_template('dueClear.html')

@app.route('/orderInformation', methods=['GET', 'POST'])
def orderInformation():
   if request.method == "POST":
      if(("" != request.form.get("orderInformationCustomerName")) and ("" != request.form.get("orderInformationCustomerContact")) and ("" == request.form.get("orderInformationOrderNumber"))):
         customer = db.session.query(Customer.customerID).filter(and_(Customer.customerName==request.form.get("orderInformationCustomerName").upper(), Customer.customerContact==request.form.get("orderInformationCustomerContact"))).subquery('s')
         orderInformation = db.session.query(Customer.customerName, Customer.customerContact, Order.orderID, Order.orderTotal, Order.orderNetPaid, Order.orderDiscount, Order.orderStatus, Product.productName).join(Order, Customer.customerID==Order.customerID).join(OrderProduct, Order.orderID==OrderProduct.orderID).join(Product, OrderProduct.productID==Product.productID).filter(and_(customer.c.customerID==Order.customerID, Order.orderID==OrderProduct.orderID, Product.productID==OrderProduct.productID, Order.orderStatus=="PENDING")).all()

      if(("" == request.form.get("orderInformationCustomerName")) and ("" == request.form.get("orderInformationCustomerContact")) and ("" != request.form.get("orderInformationOrderNumber"))):
         orderInformation = db.session.query(Customer.customerName, Customer.customerContact, Order.orderID, Order.orderTotal, Order.orderNetPaid, Order.orderStatus, Order.orderDiscount, Product.productName).join(Order, Customer.customerID==Order.customerID).join(OrderProduct, Order.orderID==OrderProduct.orderID).join(Product, OrderProduct.productID==Product.productID).filter(and_(Customer.customerID==Order.customerID, Order.orderID==OrderProduct.orderID, Product.productID==OrderProduct.productID, Order.orderID==request.form.get("orderInformationOrderNumber"), Order.orderStatus=="PENDING")).all()
      
      if(0 != len(orderInformation)):
         orderDetails = []
         k = 1
         while (k <= len(orderInformation)):
            orderInfo = {}
            orderInfo['customerName'] = orderInformation[0].customerName.title(),
            orderInfo['customerContact'] =  orderInformation[0].customerContact,
            orderInfo['orderID'] = orderInformation[0].orderID
            orderInfo['orderTotal'] = str(orderInformation[0].orderTotal)
            orderInfo['orderNetPaid'] = str(orderInformation[0].orderNetPaid)
            orderInfo['orderDiscount'] = str(orderInformation[0].orderDiscount)
            orderInfo['orderStatus'] = orderInformation[0].orderStatus.title()
            orderInfo['productDetails'] = {}
            i = 1
            while (k <= len(orderInformation)):
               if (orderInformation[0].orderID==orderInfo['orderID']):
                  orderInfo['productDetails']["product" + str(i)] = orderInformation[0].productName.title()
                  i = i + 1
                  orderInformation.remove(orderInformation[0])
               else:
                  break
            orderDetails.append(orderInfo)
         return jsonify(orderDetails=orderDetails)
      if(0 == len(orderInformation)):
         return jsonify(status="danger", statusMessage="No data found.")

@app.route('/duePaid', methods=['GET', 'POST'])
def duePaid():
   if request.method == "POST":
      if(None != request.form.get("dueOrderNumber")):
         orderDetails = {}      
         query = db.session.query(Customer, Order).join(Order).filter(Order.orderID==request.form.get("dueOrderNumber")).first()
         if(0 != len(query)):
            query.Customer.customerDues = float(query.Customer.customerDues) - float(request.form.get("duePaidAmount"))
            query.Order.orderNetPaid = query.Order.orderTotal
            query.Order.orderStatus = "COMPLETED"
            db.session.commit()

            newCashReceipt = CashReceipt(
               dueOrderID = request.form.get("dueOrderNumber"),
               duePaidAmount = request.form.get("duePaidAmount"),
               duePaidMode = request.form.get("duePaidMode").upper(),
               dueReceivedFrom = request.form.get("dueReceivedFrom").upper(),
               receptionistID = 1
            )
            db.session.add(newCashReceipt)
            db.session.commit()
            
            query = Order.query.filter_by(orderID=request.form.get("dueOrderNumber")).first()
            if(None != query):
               orderDetails["orderTotal"] = str(query.orderTotal)
               orderDetails["orderNetPaid"] = str(query.orderNetPaid)
               orderDetails["orderStatus"] = query.orderStatus.title()
            return jsonify(status="success", statusMessage="Order completed successfully.", orderDetails=orderDetails)

      if(None != request.form.get("cashReceiptOrderNumber")):
         cashReceiptDetails = {}
         customerQuery = db.session.query(Customer.customerDues).join(Order, Customer.customerID==Order.customerID).filter(Order.orderID==request.form.get("cashReceiptOrderNumber")).first()
         if(0 != len(customerQuery)):         
            cashReceiptQuery = db.session.query(Receptionist.receptionistName, Receptionist.receptionistDigitalSign, CashReceipt.cashReceiptID, CashReceipt.duePaidDate, CashReceipt.duePaidAmount, CashReceipt.duePaidMode, CashReceipt.dueReceivedFrom).join(CashReceipt).filter(Receptionist.receptionistID==CashReceipt.receptionistID, CashReceipt.dueOrderID==request.form.get("cashReceiptOrderNumber")).first()
            if(0 != len(cashReceiptQuery)):
                  cashReceiptDetails["customerDues"] = str(customerQuery.customerDues)
                  cashReceiptDetails["cashReceiptID"] = str(cashReceiptQuery.cashReceiptID)
                  cashReceiptDetails["duePaidDate"] = str(cashReceiptQuery.duePaidDate)
                  cashReceiptDetails["duePaidAmount"] = str(cashReceiptQuery.duePaidAmount)
                  cashReceiptDetails["duePaidMode"] = cashReceiptQuery.duePaidMode.lower()
                  cashReceiptDetails["dueReceivedFrom"] = cashReceiptQuery.dueReceivedFrom.title()
                  cashReceiptDetails["dueReceivedBy"] = cashReceiptQuery.receptionistName.title()
                  cashReceiptDetails["receptionistDigitalSign"] = cashReceiptQuery.receptionistDigitalSign
                  return jsonify(statufroms="success", statusMessage="Order completed successfully.", cashReceiptDetails=cashReceiptDetails)

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():
   return True

@app.route('/about', methods=['GET', 'POST'])
def about():
   return render_template('about.html')
   
@app.route('/admin', methods=['GET', 'POST'])
def admin():
   return render_template('admin.html')

@app.route('/digitalSignUpload', methods=['GET', 'POST'])
def digitalSignUpload():
   if request.method=="POST":
      f = request.files["digitalSign"]
      f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
      return jsonify(status='success', statusMessage="Digital sign successfully uploaded.")

# @app.route('/emailValidation', methods=['GET', 'POST'])
# def emailValidation():
#    if request.method == "POST":

@app.route('/sendDynamicPDF')
def sendDynamicPDF():
   path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
   config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
   rendered = render_template('index.html')
   pdf = pdfkit.from_string(rendered, False, configuration=config)
   # response = make_response(pdf)
   # response.headers["Content-Type"] = "application/pdf"
   # response.headers["Content-Disposition"] = "inline; filename=orderDetails.pdf"
   # return response
   # print(f"OCN: {request.form.get('orderCustomerName').upper()}")
   # orderCustomerName = Customer.query.filter_by(customerName=request.form.get('orderCustomerName').upper())
   
   msg = Message('Collect your pdf order details.', sender='chinmaymishra.falna@gmail.com', recipients=['chinmaymishra.falna@gmail.com'])
   msg.attach("orderDetails.pdf", "application/pdf", pdf)
   mail.send(msg)
   return jsonify(statusMessage="Collect your pdf order details from your email.", status="success")
