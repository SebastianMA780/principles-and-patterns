### --- Open Closed Principle --- ###

# software should be open for extension but closed for modification

# Open for extension means:
# It allows us to add new features without modifying existing code
# we can achieve this by using abstract class, interfaces, inheritance and polymorphism.

# Closed means:
# avoid changing existing code that has been tested and works
# It promotes encapsulation and stability of the system



### --- 
# See b_srp.py where ocp is not applied for  Notifier and PaymentProcessor classes
# and compare with te code below to see the improvement.
# --- ###

# abc module provides the ABC class which is used to create abstract classes,
# In Python an abstract class is a class that can have abstract methods and methods that are implemented.
# This class can have attributes and states as well.
# Python does not have interfaces like other languages, instead ABC is a way to achieve interfaces functionalities and abstract classes.

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from b_srp import CustomerValidation, PaymentDataValidation, TransactionLogger


class PaymentProcessor(ABC):
# - @abstractmethod has following functions:
# - Prevents instantiation: Does not allow creating instances of the abstract base class
# - Forces implementation: Requires child classes to implement the method
# - Documentation: Clearly communicates that this method must be implemented
		@abstractmethod
		def process_transaction(self, customer_data, payment_data):
				...

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
				print(
						f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
				)
                                
                            
@dataclass
class CreditCardPaymentProcessor(PaymentProcessor):
    def process_transaction(self, customer_data, payment_data):
        try:
            charge = {
                "amount": payment_data["amount"],
                "currency": "usd",
                "source": payment_data["source"],
                "description": customer_data["name"],
                "status": "succeeded",
            }
            print("Payment successful")
        except Exception as e:
            print("Payment failed:", e)
            raise e

        return charge
    
@dataclass
class PaymentService:
        customer_validator = CustomerValidation()
        payment_validator = PaymentDataValidation()
        logger = TransactionLogger()
        payment_processor: PaymentProcessor = field(default_factory=CreditCardPaymentProcessor)
        notifier: Notifier = field(default_factory=EmailNotifier)
        
        def process_transaction(self, customer_data, payment_data):
                try:
                    self.customer_validator.validate(customer_data)
                except ValueError as e:
                     raise e

                try:
                    self.payment_validator.validate(payment_data)
                except ValueError as e:
                    raise e

                try:
                    charge = self.payment_processor.process_transaction(
                        customer_data, payment_data
                    )
                    self.notifier.send_confirmation(customer_data)
                    self.logger.log(customer_data, payment_data, charge)
                    return charge
                except ValueError as e:
                     raise e
                
if __name__ == "__main__":

    payment_processor_with_email = PaymentService()
    payment_processor_with_phone = PaymentService(notifier=SMSNotifier())

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }
    customer_data_with_phone = {
        "name": "Python SPR",
        "contact_info": {"phone": "1234567890"},
    }

    payment_data = {"amount": 500, "source": "tok_mastercard", "cvv": 123}

    payment_processor_with_email.process_transaction(customer_data_with_email, payment_data)
    payment_processor_with_phone.process_transaction(customer_data_with_phone, payment_data)
    