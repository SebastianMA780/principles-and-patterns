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