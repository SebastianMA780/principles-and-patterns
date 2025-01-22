### --- Liskov Substitution Principle --- ###

# Propose by Barbara Liskov in 1987

# The subclases should be substitutable for their base classes

# Importance:
# - It avoids misbehavior when use subclasses.

# Characteristics:
# - The subclass should respect the contract of the base class
# - Maintains interfaces and types compatibility
# - It do not introduce unexpected exceptions

# Benefits:
# - Reusable code
# - Maintain interfaces and types compatibility
# - Reduces errors in executing time.
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

class Notifier(ABC):
		@abstractmethod
		def send_confirmation(self, customer_data):
				...

class SMSNotifier(Notifier):
		def send_confirmation(self, customer_data):
				phone_number = customer_data["contact_info"]["phone"]
				sms_gateway = "the custom SMS Gateway"
				print(
						f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
				)

class EmailNotifier(Notifier):
		# The method send_confirmation is violating the Liskov Substitution Principle because it is not respecting the contract of the base class,
		#then will be errors if any substitution is made.
		def send_confirmation(self, customer_data, sms_gateway):
				print(f"send the sms using {sms_gateway}: SMS sent to {customer_data['contact_info']['phone']}: Thank you for your payment.")

### --- Correct EmailNotifier --- ###
@dataclass
class EmailNotifier(Notifier):
		sms_gateway: str

		#this way the method respects the contract of the base class and the Liskov Substitution Principle.
		def send_confirmation(self, customer_data):
				print(f"send the sms using {self.sms_gateway}: SMS sent to {customer_data['contact_info']['phone']}: Thank you for your payment.")