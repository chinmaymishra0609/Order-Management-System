from datetime import datetime
from ims import db

class Customer(db.Model):
   __tablename__ = 'customers'
   customerID = db.Column(db.Integer(), primary_key=True)
   customerName = db.Column(db.String(64), nullable=False)
   customerEmail = db.Column(db.String(128), unique=True, nullable=False)
   customerContact = db.Column(db.String(11), nullable=False)
   customerZip = db.Column(db.String(10), nullable=False)
   customerCity = db.Column(db.String(20), nullable=False)
   customerDistrict = db.Column(db.String(20), nullable=False)
   customerState = db.Column(db.String(20), nullable=False)
   customerCountry = db.Column(db.String(20), nullable=False)
   customerDues = db.Column(db.Numeric(12, 2), nullable=True, default=0)
   customerDiscount = db.Column(db.Numeric(12, 2), nullable=True, default=0)

class Product(db.Model):
   __tablename__ = 'products'
   productID = db.Column(db.Integer(), primary_key=True)
   productName = db.Column(db.String(64), nullable=False)
   productCostPrice = db.Column(db.Numeric(12, 2), nullable=False)
   productSellPrice = db.Column(db.Numeric(12, 2), nullable=False)
   productQuantity = db.Column(db.Integer(), nullable=False, default=0)
   productDiscount = db.Column(db.Numeric(12, 2), nullable=True, default=0)

class Order(db.Model):
   __tablename__ = 'orders'
   orderID = db.Column(db.Integer(), primary_key=True)
   customerID = db.Column(db.Integer(), db.ForeignKey('customers.customerID'))
   orderDate = db.Column(db.Date(), default=datetime.utcnow, nullable=True)
   orderDiscount = db.Column(db.Numeric(12, 2), nullable=True, default=0)
   orderTotal = db.Column(db.Numeric(12, 2), nullable=False)
   orderNetPaid = db.Column(db.Numeric(12, 2), nullable=False)
   orderStatus = db.Column(db.String(20), nullable=True)
  
class OrderProduct(db.Model):
   __tablename__ = 'orderProducts'
   orderProductID = db.Column(db.Integer(), primary_key=True)
   orderID = db.Column(db.Integer(), db.ForeignKey('orders.orderID'))
   productID = db.Column(db.Integer(), db.ForeignKey('products.productID'))
   productQuantity = db.Column(db.Integer(), nullable=False, default=0)
   productStatus = db.Column(db.String(20), nullable=True)

class Receptionist(db.Model):
   __tablename__ = 'receptionists'
   receptionistID = db.Column(db.Integer(), primary_key=True)
   receptionistName = db.Column(db.String(64), nullable=False)
   receptionistEmail = db.Column(db.String(128), unique=True, nullable=False)
   receptionistContact = db.Column(db.String(11), nullable=False)
   receptionistPassword = db.Column(db.String(128), nullable=False)
   receptionistDigitalSign = db.Column(db.String(64), nullable=False)
   receptionistRole = db.Column(db.String(64), nullable=False, default='CASHIER')
   receptionistStatus = db.Column(db.String(64), nullable=False, default='DEACTIVE')
   
class CashReceipt(db.Model):
   __tablename__ = 'cashReceipts'
   cashReceiptID = db.Column(db.Integer(), primary_key=True)
   dueOrderID = db.Column(db.Integer(), db.ForeignKey('orders.orderID'))
   receptionistID = db.Column(db.Integer(), db.ForeignKey('receptionists.receptionistID'))
   duePaidDate = db.Column(db.Date(), default=datetime.utcnow, nullable=True)   
   duePaidAmount = db.Column(db.Numeric(12, 2), nullable=False)
   duePaidMode = db.Column(db.String(16), nullable=False)
   dueReceivedFrom = db.Column(db.String(64), nullable=False)
