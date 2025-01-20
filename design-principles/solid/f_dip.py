### --- Dependency Inversion Principle (DIP) --- ###

# High-level modules should not depend on low-level modules. Both should depend on abstractions.
# Abstractions should not depend on details. Details should depend on abstractions.
# High-level modules are modules that contain the primary logic of the application.
# Low-level modules are modules that contain the implementation details of the application.

# Benefits:
# - Improves modularity and maintainability.
# - Flexibility to change the implementation details without affecting the high-level modules.
from b_srp import CustomerValidation, PaymentDataValidation, TransactionLogger
from c_ocp import PaymentProcessor, Notifier, CreditCardPaymentProcessor, EmailNotifier
from dataclasses import dataclass

# See b_srp and c_ocp to understand the problem with the code.
# In those modules, PaymentService, though it follows most of the DIP rules, 
# is still instantiating the concrete classes of its dependencies.

@dataclass
class PaymentService:
        customer_validator: CustomerValidation
        payment_validator: PaymentDataValidation
        logger: TransactionLogger
        payment_processor: PaymentProcessor
        notifier: Notifier
        
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
    customer_validator = CustomerValidation()
    payment_validator = PaymentDataValidation()
    logger = TransactionLogger()
    payment_processor = CreditCardPaymentProcessor()
    email_notifier = EmailNotifier()

    payment_processor_with_email = PaymentService(
         customer_validator=customer_validator,
         payment_validator=payment_validator,
         logger=logger,
         payment_processor=payment_processor,
         notifier=email_notifier
		)

    customer_data_with_email = {
        "name": "John Doe",
        "contact_info": {"email": "e@mail.com"},
    }
    payment_data = {"amount": 500, "source": "tok_mastercard", "cvv": 123}

    payment_processor_with_email.process_transaction(customer_data_with_email, payment_data)
    