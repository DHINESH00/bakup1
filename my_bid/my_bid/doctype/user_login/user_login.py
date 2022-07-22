# Copyright (c) 2022, dhinesh and contributors
# For license information, please see license.txt

import random
import smtplib
import base64
from click import password_option
import frappe
from frappe.share import remove
from frappe.utils import now
from frappe.model.document import Document

class UserLogin(Document):
	pass
@frappe.whitelist(allow_guest=True)
def sigup(data):
	frappe.set_user("Administrator")
	ul=frappe.get_list("User Login")
	print("###################")
	print(data["type"],"signup")
	print(str(data["type"])=="signup")
	if(data["type"]=="signup"):
		if (frappe.get_value("User Login",data["email"])):
			return "Email exist"
		else:
			return "New User"
	elif(data["type"]=="login"):
		print(data["type"])
		user=frappe.get_value("User Login",data["email"],"password")
		if(user):
			if(user==data["password"]):
				print("true")
				return "true"
			else:
				print("false")
				return "false"
		
		else:
			print("no user")
			return "no user"
	else:
		print("null")
		return "null"

@frappe.whitelist(allow_guest=True)
def otp(data):
	frappe.set_user("Administrator")
	email=data["email"]
	s = smtplib.SMTP("smtp.gmail.com" , 587)
	s.starttls()
	s.login("mybidapp4u@gmail.com" , "byqorsmmngbvqtxt")
	otp = random.randint(1000, 9999)
	# frappe.sendmail(recipients=str(email),subject="OTP",message=otp)
	otp = str(otp)
	if frappe.get_value("otp",str(email)):
		print(otp,email)
		frappe.set_value("otp",email,"otp",otp)
		print(frappe.get_value('otp',email,"otp"))
		
	else:
		in_otp=frappe.new_doc("otp")
		in_otp.email=email
		in_otp.otp=otp
		in_otp.save()
	s.sendmail("mybidapp4u@gmail.com", email, otp)
	print("OTP sent succesfully..")
	s.quit()
	
	return "OTP sent succesfully.."
@frappe.whitelist(allow_guest=True)
def get_otp(data):
	frappe.set_user("Administrator")
	email=data["email"]
	g_otp=frappe.get_doc("otp",email)
	if(str(g_otp.otp)==str(data["otp"])):
		ud=frappe.new_doc("User Login")
		ud.email=data["email"]
		ud.password=data["password"]
		ud.save()
		return "true"

	else:
		frappe.throw("no otp")
		return "false"
	


@frappe.whitelist(allow_guest=True)
def login(data):
	frappe.set_user("Administrator")
	user=frappe.get_value("User Login",data["email"],"password")
	if(user):
		if(user==data["password"]):
			return "true"
		else:
			return "false"
		
	else:
		return "no user"

@frappe.whitelist(allow_guest=True)
def posting(data,post):
	frappe.set_user("Administrator")
	if(frappe.get_value("User Login",data["email"],"name")):
		posts=frappe.new_doc("posting")
		posts.product_name=post["post_name"]
		posts.category=post["category"]
		posts.number=post["number"]
		posts.qnt=post["qnt"]
		posts.user=data["email"]
		posts.save()
		return "sucessfull"
	else:
		return "no user"
@frappe.whitelist(allow_guest=True)
def get_posting(data):
	frappe.set_user("Administrator")
	if(frappe.get_value("User Login",data["email"],"name")):
		s=frappe.db.sql("""Select product_name as p_name,category,number,is_bid,name,qnt,is_oder_placed from `tabposting` where user=%s """,(data["email"]),as_dict=1)
		return s
	else:
		return []
@frappe.whitelist(allow_guest=True)
def shop_present(data):
	frappe.set_user("Administrator")
	shop=frappe.get_value("Shop Verification",{"user":data["email"]},["verification_done","name"])
	if(shop):
		if(shop[1]):
			if(shop[0]==1):
				return "sucessfull"
			else:
				return "in verification"
		else:
			return"new shop"
	else:
		return "new shop"
@frappe.whitelist(allow_guest=True)
def shop_verfication(**shop_details):
	frappe.set_user("Administrator")
	shop=frappe.new_doc("Shop Verification")
	shop.name1=shop_details["name"]
	shop.email=shop_details["email"]
	shop.number=shop_details["number"]
	shop.shop_adress=shop_details["shop_adress"]
	shop.gst_number=shop_details["gst_number"]
	shop.category1=shop_details["category1"]
	shop.user=shop_details["user"]
	shop.save(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def shop_datas(shop_data):
	frappe.set_user("Administrator")
	if(frappe.db.get_value("Shop Data",shop_data["user"])):
		shop_e=frappe.get_doc("Shop Data",shop_data["user"])
		shop_e.append("product_data",{
		"product_name":shop_data["product_name"],
		"category":shop_data["category"],
		"mrp":shop_data["mrp"],

	})
		shop_e.save()
	else:
		shop_e=frappe.new_doc("Shop Data")
		shop_e.user=shop_data["user"]
		
		shop_e.append("product_data",{
		"product_name":shop_data["product_name"],
		"category":shop_data["category"],
		"mrp":shop_data["mrp"],

	})
		shop_e.save()
	return "Done"
@frappe.whitelist(allow_guest=True)
def shop_data_see(shop_data):
	frappe.set_user("Administrator")
	if(frappe.db.get_value("Shop Data",shop_data["user"])):
		s=frappe.db.sql("select product_name, category, mrp from `tabproduct Data` where parent=%s",(shop_data["user"]),as_dict=1)
		return s
	return "No Data"
@frappe.whitelist(allow_guest=True)
def shop_user_post_see(shop_data):
	frappe.set_user("Administrator")
	
	if(frappe.db.get_value("Shop Data",shop_data["user"])):
		c=frappe.db.get_value("Shop Verification",shop_data["user"],"category1",)
		s=frappe.db.sql("""Select product_name as p_name,category,name,qnt from `tabposting` where user != %s  and is_bid= 1  and  is_oder_placed= 0 and category= %s """,(shop_data["user"],c),as_dict=1)
		return s
	return "no user"
@frappe.whitelist(allow_guest=True)
def is_bid(user_product):
	frappe.set_user("Administrator")
	if(frappe.db.get_value("posting",{"user":user_product["user"]})):
		p=frappe.get_doc("posting",user_product["name"])
		p.is_bid=1
		p.save()
		return "Done"
@frappe.whitelist(allow_guest=True)
def Same_post(product):
	frappe.set_user("Administrator")
	s=frappe.db.sql("select product_name, category, mrp,parent from `tabproduct Data` where LOWER(product_name)=%s",(product["name"].lower()),as_dict=1)
	return s
@frappe.whitelist(allow_guest=True)
def bid(post_name):
	frappe.set_user("Administrator")
	s=frappe.db.sql("select shop, mrp, time from `tabbid` where parent=%s",(post_name["name"]),as_dict=1)
	return s
@frappe.whitelist(allow_guest=True)
def update_bid(post_name):
	frappe.set_user("Administrator")
	bid=frappe.get_doc("posting",post_name["name"])
	for d in bid.bid:
		if(d.shop==post_name["shop"]):
			bid.remove(d)
	bid.save()
	bid.append(
		"bid",{
			"shop":str(post_name["shop"]),
			"mrp":post_name["mrp"],
			"time":post_name["time"]

			
		}
	)
	bid.save()
@frappe.whitelist(allow_guest=True)
def add_adress(post_data):
	frappe.set_user("Administrator")
	bid=frappe.get_doc("posting",post_data["name"])
	mrp=0

	for d in bid.bid:
		if(d.shop==post_data["shop"]):
			d.is_used=1
			mrp=d.mrp
	bid.save()
	bid.adress=str(post_data["adress"])+str(post_data["city"])+str(post_data["pincode"])
	bid.is_oder_placed=1
	bid.save()
	shop_number=frappe.db.get_value("Shop Verification",post_data["shop"],"number")
	adress=("""%s <br> %s  %s"""%(post_data["adress"],post_data["city"],post_data["pincode"]))
	message1=("""Hi %s <br> Your Order: %s  Quantity: %s  Topay: %sRs <br>Will be delivered <br>
			    <br>  Shop Contact %s"""%(bid.user,bid.product_name,bid.qnt,mrp,shop_number))
	message2=("""Hi %s <br> Order: %s  Quantity: %s  User Need Topay: %sRs <br>Need To  be delivered <br>
			    Address %s<br>  User Contact %s"""%(post_data["shop"],bid.product_name,bid.qnt,mrp,adress,bid.number))
	frappe.sendmail(recipients=[bid.user],
			message=str(message1),
			subject=str(post_data["name"])+"Order Is Placed",
			reference_doctype="posting",
			reference_name=post_data["name"],
			)
	frappe.sendmail(recipients=[post_data["shop"]],
			message=str(message2),
			subject=str(post_data["name"])+"Order  Need To  be delivered",
			reference_doctype="posting",
			reference_name=post_data["name"],
			)