# NOTES: 
# - I kept this solution as simple as possible and intended to not over-engineer it.
# - Even though shameless coding was recommended, you will notice that I spent more time in level1 to incrementally build it with ease.
# - This solution is not as robust as much as I would've hoped it to be as it requires input validation and testing beyond matching the expected_output.

import json
# import unittest

from datetime import datetime, timedelta

class Carrier:
    def __init__(self, code, delivery_promise, saturday_deliveries, oversea_delay_threshold):
        self.code = code
        self.delivery_promise = delivery_promise
        self.saturday_deliveries = saturday_deliveries
        self.oversea_delay_threshold = oversea_delay_threshold

class Package:
    def __init__(self, id, carrier, shipping_date, origin_country, destination_country):
        self.id = id
        self.carrier = carrier
        self.shipping_date = datetime.strptime(shipping_date, "%Y-%m-%d")
        self.origin_country = origin_country
        self.destination_country = destination_country

    def __is_working_day(self, date, saturday_deliveries):
        # Sunday
        if date.weekday() == 6:
            return False

        # Saturday
        elif date.weekday() == 5:
            return saturday_deliveries

        return True

    def calculate_expected_delivery(self, carrier, country_distance):
        oversea_delay =  country_distance.get_distance(self.origin_country, self.destination_country) // carrier.oversea_delay_threshold
        days_to_add = carrier.delivery_promise + 1 + oversea_delay
        delivery_date = self.shipping_date
        
        while days_to_add > 0:
            delivery_date += timedelta(days=1)
            if self.__is_working_day(delivery_date, carrier.saturday_deliveries):
                days_to_add -= 1

        return delivery_date, oversea_delay

    def to_dict(self, expected_delivery, oversea_delay):
        return {"package_id": self.id, "expected_delivery": expected_delivery, "oversea_delay": oversea_delay}

class CountryDistance:
    def __init__(self, data):
        self.data = data

    def get_distance(self, from_country, to_country):
        if from_country == to_country:
            return 0

        if from_country in self.data and to_country in self.data[from_country]:
            return self.data[from_country][to_country]
        
        raise ValueError("Distance between specified countries not found")

class DeliveryManager:
    def __init__(self, input_data):
        self.carriers = [Carrier(**carrier) for carrier in input_data["carriers"]]
        self.packages = [Package(**package) for package in input_data["packages"]]
        self.country_distance = CountryDistance(input_data["country_distance"])
        self.deliveries = []

    def add_delivery(self, package):
        carrier = next((carrier for carrier in self.carriers if carrier.code == package.carrier), None)
        if carrier is not None:
            expected_delivery, oversea_delay = package.calculate_expected_delivery(carrier, self.country_distance)
            expected_delivery = expected_delivery.strftime("%Y-%m-%d")
            self.deliveries.append(package.to_dict(expected_delivery, oversea_delay))

    def to_dict(self):
        return {"deliveries": self.deliveries}

if __name__ == "__main__":

    try:
        with open("data/input.json") as f:
            input_data = json.load(f)

        # TODO: Validate input data

        delivery_manager = DeliveryManager(input_data)
        for package in delivery_manager.packages:
            delivery_manager.add_delivery(package)

        output_data = delivery_manager.to_dict()
        with open("data/output.json", "w") as f:
            json.dump(output_data, f, indent=2)

    except Exception as e:
        print(e)

# TODO: Write test cases