from decimal import Decimal

class CheapPaymentGateway:
    @staticmethod
    def process_payment(total: Decimal):
        return f"Successfully processed a budget friendly payment of ₱{total:.2f}. Thank you for your purchase!"

class ExpensivePaymentGateway:
    @staticmethod
    def process_payment(total: Decimal):
        return f"Successfully processed a expensive payment of ₱{total:.2f}. Thank you for your purchase!"

def process_payment(total: Decimal):
    if total < Decimal("10.00"):
        return CheapPaymentGateway.process_payment(total)
    else:
        return ExpensivePaymentGateway.process_payment(total)
