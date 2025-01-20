### --- Interface Segregation Principle --- ###

# A client should not be forced to implement an interface that it does not use.

# Benefits:
# - Improves cohesion and reduces coupling
# - Components are more reusable and maintainable
# - Changes in one component do not affect other components
# - Unit testing is easier

# Signals to use:
# - Interfaces with many irrelevant methods
# - Classes that do not use all methods of an interface
# - Changes to the interface affect many classes

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from b_srp import CustomerValidation, PaymentDataValidation, TransactionLogger

# A new method is added to the PaymentProcessor class
# if a class that implements the PaymentProcessor interface does not need to implement the new method, 
# it will be forced to do so that violates the Interface Segregation Principle.
class PaymentProcessorIspViolation(ABC):
        @abstractmethod
        def process_transaction(self, customer_data, payment_data):
                ...     

        @abstractmethod
        def refund_transaction(self, customer_data, payment_data):
                ...

### --- Fixes ISP violation  --- ###   
# The PaymentProcessor interface is divided into two interfaces: PaymentProcessor and RefundProcessor

class PaymentProcessor(ABC):
        @abstractmethod
        def process_transaction(self, customer_data, payment_data):
                ...

class RefundProcessor(ABC):
        @abstractmethod
        def refund_transaction(self):
                ...

@dataclass
class CreditCardPaymentProcessor(PaymentProcessor, RefundProcessor):
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
    
    def refund_transaction(self):
           print("Refund processed")

@dataclass
class TransferTransactionProcessor(PaymentProcessor):
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

# This way the client can implement the PaymentProcessor interface without being forced to implement the refund_transaction method
