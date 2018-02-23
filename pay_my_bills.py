from splinter import Browser
from selenium.webdriver.common.keys import Keys

with Browser() as browser:
	# visit url
	url = "https://www.venmo.com"
	browser.visit(url)
	browser.cookies.delete()

	# credentials
	my_name = "John Smith" # your name on venmo
	my_number = "5555555555" # phone number used to log in
	my_password = "YOUR_PASSWORD" # password

	# bills
	bills = [{
		"payment_type": "CHARGE", # or "PAY"
		"venmo_username": "venmo-user-007",
		"venmo_name": "Venmo Name",
		"amount": "0.01",
		"details": "this is a test"
	},
	{
		"payment_type": "PAY",
		"venmo_username": "friendo-numero-uno",
		"venmo_name": "Friend One",
		"amount": "0.01",
		"details": "this is another test"
	}];

	# sign in flow
	if browser.is_text_not_present(my_name):
		print("Not logged in, performing sign in flow ...")
		sign_in_link = browser.find_link_by_text("Sign In").first
		sign_in_link.click()
		browser.find_by_name("phoneEmailUsername").fill(my_number)
		browser.find_by_name("password").fill(my_password + "/n")
		buttons = browser.find_by_tag("button")
		sign_in_button = buttons.first.find_by_text("Sign In")
		sign_in_button.click()
		# DO LATER: handle 2FA
		# if MFA_TRIGGERED:
			# verification_code = raw_input("Please enter verification code")
			# browser.find_by_name("verify").fill(verification_code)
			# buttons = browser.find_by_tag("button")
			# verify_button = buttons.first.find_by_text("Enter")
			# verify_button.click()
	# create a charge for each bill
	for bill in bills:
		# select pay or charge
		if browser.is_element_present_by_id('onebox_pay_toggle', 20):
			if bill['payment_type'] == "PAY":
				print("Creating a payment to: " + bill['venmo_username'] + " (" + bill['venmo_name'] + ")")
				payment_type_button = browser.find_by_id("onebox_pay_toggle").first
			elif bill['payment_type'] == "CHARGE": 
					print("Creating a charge to: " + bill['venmo_username'] + " (" + bill['venmo_name'] + ")")
					payment_type_button = browser.find_by_id("onebox_charge_toggle").first
			payment_type_button.click()
			# select user
			venmo_user_search = browser.find_by_id("onebox_typeahead").first
			venmo_user_search.fill(bill['venmo_username'] + "\n");
			user_dropdown = browser.find_by_css(".ac-renderer").first
			select_user = user_dropdown.find_by_text(bill['venmo_username']).first
			select_user.click()
			# fill out amount and details
			browser.find_by_id("onebox_details").fill(bill['amount'] + " " + bill['details'])
			print("$" + bill['amount'] + " - " + bill['details'])
			send_button = browser.find_by_id("onebox_send_button")
			send_button.click()
			# set text to check based on payment type
			if bill['payment_type'] == "PAY":
				text_to_check = "Paid $%s and notified %s of your payment."%(bill['amount'], bill['venmo_name'])
			elif bill['payment_type'] == "CHARGE": 
				text_to_check = "Requested $%s from %s."%(bill['amount'], bill['venmo_name'])
			# if success message not present, print error and exit
			if not browser.is_text_present(text_to_check, 15):
				api_response = browser.find_by_id("js_messaging_message").first.text
				print(api_response)
				print("Something went wrong, please check Venmo account.")
				quit()
			else:
				print("Success!")
				# refresh
				browser.visit(url)
	print("fin")