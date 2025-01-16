### --- Single Responsibility Principle --- ###

# A class should have only one job.
# A class should have only one reason to change.

# Benefits:
# - More maintainable code
# - Reusability of code
# - More testable code
# - Less coupling between classes

# When to use:
# - Many reasons to change a class
# - High complexity in a class and maintainability is difficult
# - It is hard to make unit tests
# - Code duplication

from dataclasses import dataclass

@dataclass
class PaymentProcessor:
    def process_transaction(self, customer_data, payment_data):
        # 1. Validation Responsibility
        if not customer_data.get("name"):
            print("Invalid customer data: missing name")
            raise ValueError("Invalid customer data: missing name")

        if not customer_data.get("contact_info"):
            print("Invalid customer data: missing contact info")
            raise ValueError("Invalid customer data: missing contact info")

        if not payment_data.get("source"):
            print("Invalid payment data")
            raise ValueError("Invalid payment data")

				#2. Payment Responsibility
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

				# 3. Notification Responsibility
        if "email" in customer_data["contact_info"]:
            # import smtplib
            from email.mime.text import MIMEText

            msg = MIMEText("Thank you for your payment.")
            msg["Subject"] = "Payment Confirmation"
            msg["From"] = "no-reply@example.com"
            msg["To"] = customer_data["contact_info"]["email"]

            # server = smtplib.SMTP("localhost")
            # server.send_message(msg)
            # server.quit()
            print("Email sent to", customer_data["contact_info"]["email"])

        elif "phone" in customer_data["contact_info"]:
            phone_number = customer_data["contact_info"]["phone"]
            sms_gateway = "the custom SMS Gateway"
            print(
                f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
            )

        else:
            print("No valid contact information for notification")
            return charge

				# 4. Logging Responsibility
        with open("transactions.log", "a") as log_file:
            log_file.write(f"{customer_data['name']} paid {payment_data['amount']}\n")
            log_file.write(f"Payment status: {charge['status']}\n")

        return charge
				# This class violates the Single Responsibility Principle because as you can see, it has multiple responsibilities.
                
### -- Refactor previous class in order to apply the Single Responsibility Principle -- ###

# Validation Responsibility
@dataclass
class CustomerValidator:
		def validate(self, customer_data):
				if not customer_data.get("name"):
						print("Invalid customer data: missing name")
						raise ValueError("Invalid customer data: missing name")

				if not customer_data.get("contact_info"):
						print("Invalid customer data: missing contact info")
						raise ValueError("Invalid customer data: missing contact info")

# Validation Responsibility                          
@dataclass
class PaymentDataValidator:
		def validate(self, payment_data):
				if not payment_data.get("source"):
						print("Invalid payment data")
						raise ValueError("Invalid payment data")
                                

# Notification Responsibility
@dataclass
class Notifier:
        def send_confirmation(self, customer_data):
            if "email" in customer_data["contact_info"]:
                # import smtplib
                from email.mime.text import MIMEText

                msg = MIMEText("Thank you for your payment.")
                msg["Subject"] = "Payment Confirmation"
                msg["From"] = "no-reply@example.com"
                msg["To"] = customer_data["contact_info"]["email"]

                # server = smtplib.SMTP("localhost")
                # server.send_message(msg)
                # server.quit()
                print("Email sent to", customer_data["contact_info"]["email"])

            elif "phone" in customer_data["contact_info"]:
                phone_number = customer_data["contact_info"]["phone"]
                sms_gateway = "the custom SMS Gateway"
                print(
                    f"send the sms using {sms_gateway}: SMS sent to {phone_number}: Thank you for your payment."
                )

# Logging Responsibility
@dataclass
class TransactionLogger:
        def log(self, customer_data, payment_data, charge):
            with open("transactions.log", "a") as log_file:
                log_file.write(f"{customer_data['name']} paid {payment_data['amount']}\n")
                log_file.write(f"Payment status: {charge['status']}\n")


# Payment Responsibility
@dataclass
class PaymentProcessorV2:
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

# Payment Service    
@dataclass
class PaymentService:
        payment_processor = PaymentProcessorV2()
        notifier = Notifier()
        logger = TransactionLogger()
        customer_validator: CustomerValidator()
        payment_data_validator: PaymentDataValidator()

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
    payment_processor = PaymentProcessor()

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }
    customer_data_with_phone = {
        "name": "Python SPR",
        "contact_info": {"phone": "1234567890"},
    }

    payment_data = {"amount": 500, "source": "tok_mastercard", "cvv": 123}

    payment_processor.process_transaction(customer_data_with_email, payment_data)
    payment_processor.process_transaction(customer_data_with_phone, payment_data)