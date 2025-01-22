### --- Strategy Pattern --- ###

# Strategy Pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one, 
# and makes them interchangeable.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

class Notifier(ABC):
		@abstractmethod
		def send_confirmation(self, customer_data):
				...
											
class EmailNotifier(Notifier):
		def send_confirmation(self, customer_data):
				msg = {}
				msg["Subject"] = "Payment Confirmation"
				msg["From"] = "no-reply@example.com"
				msg["To"] = customer_data["contact_info"]["email"]

				print("Email sent to", customer_data["contact_info"]["email"])
                                
class SMSNotifier(Notifier):
		def send_confirmation(self, customer_data):
				phone_number = customer_data["contact_info"]["phone"]
				sms_gateway = "the custom SMS Gateway"
				print(f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment.")

@dataclass
class PaymentService:
			notifier: Notifier

			def process_transaction(self, customer_data):
					# Process the transaction
					# Send the confirmation
					self.notifier.send_confirmation(customer_data)

def set_notifier(customer_data) -> Notifier:
		if "email" in customer_data["contact_info"]:
				return EmailNotifier()
		
		if "phone" in customer_data["contact_info"]:
				return SMSNotifier()
		
		raise ValueError("Invalid contact info")
		
if __name__ == "__main__":
		customer_data_with_email = {
				"name": "John Doe",
				"contact_info": {"email": "e@mail.com"},
		}
		customer_data_with_phone = {
				"name": "Python SPR",
				"contact_info": {"phone": "1234567890"},
		}

		payment_service = PaymentService(set_notifier(customer_data_with_email))
		payment_service.process_transaction(customer_data_with_email)

		payment_service = PaymentService(set_notifier(customer_data_with_phone))
		payment_service.process_transaction(customer_data_with_phone)
		