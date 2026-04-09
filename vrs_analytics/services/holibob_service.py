import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

import config.global_config as gc

load_dotenv()

BASE_URL = os.getenv("HOLIBOB_BASE_URL", "http://staging.apigateway.travelai.com")
PROPERTY_BASE_URL=os.getenv("PROPERTY_BASE_URL","http://beta-mda.refine.lefttravel.com/v1/property/property-list")
API_KEY = os.getenv("HOLIBOB_API_KEY", "cGFydG5lci1hcGktZ2F0ZXdheS13Mw==")
CURRENCY = os.getenv("CURRENCY", "USD")
COOKIES = {
    "AWSALB": "q/vkkG6zWkag2xPffm5YLWWy5HAexam4mafsFWqSqZud1vWAoqn8RLDkoY+qleQdpK7vlbJQMmb/HW1Up6zgBqpXHPtwpfegItv+YILoCzuXA59DUocOG/Hohhsk",
    "AWSALBCORS": "q/vkkG6zWkag2xPffm5YLWWy5HAexam4mafsFWqSqZud1vWAoqn8RLDkoY+qleQdpK7vlbJQMmb/HW1Up6zgBqpXHPtwpfegItv+YILoCzuXA59DUocOG/Hohhsk",
}

def fetch_property(property_id):
    params = {
        "ownerIdList": property_id
    }

    try:
        response = requests.get(
            PROPERTY_BASE_URL,
            params=params,
            cookies=COOKIES,
            timeout=30,
        )

        response.raise_for_status()

        property = response.json()

        # API response return
        return property

    except requests.exceptions.RequestException as e:
        print(f"Property API Error: {e}")
        return None


def transform_booking(booking_node):

    transaction_id = str(booking_node.get("id"))

    created_at = booking_node.get("createdAt")

    transaction_ts_utc = datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )

    transaction_date = transaction_ts_utc.date()

    currency = "USD"
    revenue = booking_node.get("totalPrice", {}).get("commission")
    sale_amount = booking_node.get("totalPrice", {}).get("gross")
    
    availability_nodes = booking_node.get(
        "availabilityList", {}
    ).get("nodes", [])
    check_in_date = None
    if availability_nodes:
        check_in_date = availability_nodes[0].get("date")
    partner_response = booking_node

    return {
        "transaction_id": transaction_id,
        "transaction_date": transaction_date,
        "transaction_ts_utc": transaction_ts_utc,
        "currency": currency,
        "revenue": revenue,
        "sale_amount": sale_amount,
        "partner_response": partner_response,
        "check_in_date": check_in_date,
    }


def fetch_bookings(start_date, end_date, page_size=10):
    url = f"{BASE_URL}/graphql"

    headers = {
        "X-Api-Key": API_KEY,
        "X-Partner": "holibob",
        "X-Holibob-Currency": CURRENCY,
        "Content-Type": "application/json",
    }

    all_nodes = []
    page = 1
    record_count = None

    while True:
        query_string = (
            'query fetchBookingList {\n'
            '  bookingList(\n'
            '    filter: {createdSince: "' + start_date + '", createdTill: "' + end_date + '", isSandboxed: false}\n'
            f'    page: {page}\n'
            f'    pageSize: {page_size}\n'
            '    sort: {createdAt: asc}\n'
            '  ) {\n'
            '    recordCount\n'
            '    nodes {\n'
            '      id\n'
            '      name\n'
            '      code\n'
            '      consumerTrip {\n'
            '        partnerExternalReference\n'
            '      }\n'
            '      availabilityList {\n'
            '        nodes {\n'
            '          id\n'
            '          date\n'
            '          product {\n'
            '            id\n'
            '            name\n'
            '            code\n'
            '          }\n'
            '        }\n'
            '      }\n'
            '      partnerChannelBookingUrl\n'
            '      partnerChannelId\n'
            '      partnerChannelName\n'
            '      partnerExternalReference\n'
            '      partnerId\n'
            '      partnerName\n'
            '      paymentState\n'
            '      paymentType\n'
            '      processState\n'
            '      createdAt\n'
            '      isComplete\n'
            '      isFailed\n'
            '      isPendingCommit\n'
            '      isProcessing\n'
            '      isQuestionsComplete\n'
            '      isSandboxed\n'
            '      isWorkflowProcessing\n'
            '      totalPrice {\n'
            '        commission\n'
            '        currency\n'
            '        gross\n'
            '        grossFormattedText\n'
            '        commissionFormattedText\n'
            '        net\n'
            '        netFormattedText\n'
            '        pricingData\n'
            '      }\n'
            '    }\n'
            '  }\n'
            '}'
        )

        payload = {"query": query_string, "variables": {}}
        raw_body = json.dumps(payload, separators=(',', ':'))

        print(f"Sending to: {url} (page {page}, size {page_size})")

        response = requests.post(
            url,
            headers=headers,
            data=raw_body,
            allow_redirects=True,
            timeout=30
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"Error Response:\n{response.text}")
            response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print(f"GraphQL Errors: {data['errors']}")
            return None

        booking_list = data.get("data", {}).get("bookingList", {})
        nodes = booking_list.get("nodes", []) or []
        record_count = booking_list.get("recordCount", record_count)

        all_nodes.extend(nodes)

        # Stop when we get fewer than page_size rows
        if len(nodes) < page_size:
            break

        page += 1

    return {"data": {"bookingList": {"recordCount": record_count, "nodes": all_nodes}}}



def get_fresh_data():

    booking_data = fetch_bookings(gc.START_DATES, gc.END_DATES)
    nodes = booking_data["data"]["bookingList"]["nodes"]
    
    all_transformed = [] 
    
    for booking_node in nodes:
        transformed_booking = transform_booking(booking_node)
        
        availability_nodes = booking_node.get("availabilityList", {}).get("nodes", [])
        
        if availability_nodes:
            for avail_node in availability_nodes:
                property_id = avail_node.get("product", {}).get("id")
                if property_id:
                    single_property = fetch_property(property_id)

                    
                    
                    fresh_data = {
                        **transformed_booking,  
                        "property_id": property_id,
                        "property_info": single_property,
                        "property": single_property
                    }
                    
                    all_transformed.append(fresh_data)
        else:
            fresh_data = transformed_booking.copy()
            fresh_data["property_id"] = None
            fresh_data["property_info"] = None
            all_transformed.append(fresh_data)
    
    # print(all_transformed)

    return all_transformed
