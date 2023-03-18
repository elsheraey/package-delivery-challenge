import json

from datetime import datetime, timedelta

class Carrier:
    def __init__(self, code, delivery_promise):
        self.code = code
        self.delivery_promise = delivery_promise

class Package:
    def __init__(self, id, carrier, shipping_date):
        self.id = id
        self.carrier = carrier
        self.shipping_date = datetime.strptime(shipping_date, "%Y-%m-%d")

    def calculate_expected_delivery(self, carrier):
        # NOTE: I'm not sure if the expected delivery date should be the next business day or the next day after the carrier delivery promise.
        return self.shipping_date + timedelta(days=carrier.delivery_promise + 1)

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