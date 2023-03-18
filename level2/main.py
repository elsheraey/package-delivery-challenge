import json

from datetime import datetime, timedelta

class Carrier:
    def __init__(self, code, delivery_promise, saturday_deliveries):
        self.code = code
        self.delivery_promise = delivery_promise
        self.saturday_deliveries = saturday_deliveries

class Package:
    def __init__(self, id, carrier, shipping_date):
        self.id = id
        self.carrier = carrier
        self.shipping_date = datetime.strptime(shipping_date, "%Y-%m-%d")

    def __is_working_day(self, date, saturday_deliveries):
        # Sunday
        if date.weekday() == 6:
            return False

        # Saturday
        elif date.weekday() == 5:
            return saturday_deliveries

        return True

    def calculate_expected_delivery(self, carrier):
        days_to_add = carrier.delivery_promise + 1
        delivery_date = self.shipping_date
        
        while days_to_add > 0:
            delivery_date += timedelta(days=1)
            if self.__is_working_day(delivery_date, carrier.saturday_deliveries):
                days_to_add -= 1

        return delivery_date

    def to_dict(self, expected_delivery):
        return {"package_id": self.id, "expected_delivery": expected_delivery}

with open("data/input.json") as f:
    input_data = json.load(f)

carriers = [Carrier(**carrier) for carrier in input_data["carriers"]]
packages = [Package(**package) for package in input_data["packages"]] 
deliveries = []
for package in packages:
    carrier = next((carrier for carrier in carriers if carrier.code == package.carrier), None)
    if carrier is not None:
        expected_delivery = package.calculate_expected_delivery(carrier).strftime("%Y-%m-%d")
        deliveries.append(package.to_dict(expected_delivery))

output_data = {"deliveries": deliveries}
with open("data/output.json", "w") as f:
    json.dump(output_data, f, indent=2)