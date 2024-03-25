# Description: Insurance Policy Management and Calculation System for One Stop Insurance
# Name: Steven Norris
# Date Created: 03/14/2024
# Date Last Modified: 03/24/2024


#   |-----------|   #     
#   | LIBRARIES |   #
#   |-----------|   #

import string
from datetime import datetime, timedelta


#   |-----------|   #
#   | CONSTANTS |   #
#   |-----------|   #

# Default Values
NEXT_POLICY_NUMBER = 1944
BASIC_PREMIUM = 869.00
ADDITIONAL_CAR_DISCOUNT = 0.25
EXTRA_LIABILITY_COST_PER_CAR = 130.00
GLASS_COVERAGE_COST_PER_CAR = 86.00
LOANER_CAR_COST_PER_CAR = 58.00

# Tax and Fee Rate
HST_RATE = 0.15
MONTHLY_PAYMENT_PROCESSING_FEE = 39.99
    
# Validation Sets
ALLOWED_NAME_CHARACTERS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-.' ")
ALLOWED_NUMBERS = set("1234567890")
VALID_PROVINCES = {"AB", "BC", "MB", "NB", "NL", "NS", "ON", "PE", "QC", "SK", "NT", "NU", "YT"}
PHONE_NUMBER_LENGTH = 10
POSTAL_CODE_LENGTH = 6
NUM_PAYMENTS = 8

# Global Claims List
claims = []  



#   |-----------------|   #
#   | INPUT FUNCTIONS |   #
#   |-----------------|   #

def is_valid_input(input_value, validation_types):
    """
    Validates the input based on the given validation type or types, supporting a wide range of validations.
    Designed for flexibility and broad usability with detailed error messages for guidance.
    Now supports multiple validation types.

    Parameters:
        input_value (str): The value to be validated.
        validation_types (Union[str, List[str]]): The type(s) of validation to apply.

    Returns:
        tuple: A tuple containing a boolean indicating if the input is valid, and a message.
    """
    # Ensure validation_types is a list even if a single validation type is provided
    if isinstance(validation_types, str):
        validation_types = [validation_types]

    input_value = input_value.strip()

    if not input_value:
        return False, "Input cannot be blank."

    for validation_type in validation_types:
        if validation_type == 'long':
            if len(input_value) > 14:
                return False, "Input exceeds the maximum allowed length of 10 characters."
            
        elif validation_type == 'short':
            if len(input_value) > 5:
                return False, "Input exceeds the maximum allowed length of 5 characters."
        
        elif validation_type == 'name':
            if not set(input_value).issubset(ALLOWED_NAME_CHARACTERS):
                return False, "Invalid name. Please use only allowed characters."
            
        elif validation_type == 'phone_number':
            if not (len(input_value) == 10 and input_value.isdigit()):
                return False, "Invalid phone number. Please enter a 10-digit numeric phone number."
            
        elif validation_type == 'province':
            if input_value.upper() not in VALID_PROVINCES:
                return False, "Invalid province. Please enter a valid abbreviation."
            
        elif validation_type == 'postal_code':
            if not (len(input_value) == POSTAL_CODE_LENGTH and input_value[0].isalpha() and input_value[1].isdigit()):
                return False, "Invalid postal code format."
            
        elif validation_type == 'yes_no':
            if input_value.lower() not in ['y', 'n']:
                return False, "Data Entry Error - Answer Yes or No by typing Y or N."
            
        elif validation_type == 'day':
            try:
                day = int(input_value)
                if not 1 <= day <= 31:
                    return False, "Invalid day. Please enter a value between 1 and 31."
            except ValueError:
                return False, "Invalid day. Please enter a numeric value."
            
        elif validation_type == 'month':
            try:
                month = int(input_value)
                if not 1 <= month <= 12:
                    return False, "Invalid month. Please enter a value between 1 and 12."
            except ValueError:
                return False, "Invalid month. Please enter a numeric value."
            
        elif validation_type == 'year':
            try:
                year = int(input_value)
                if not 1900 <= year <= 2150:
                    return False, "Invalid year. Please enter a value between 1900 and 2150."
            except ValueError:
                return False, "Invalid year. Please enter a numeric value."
            
        elif validation_type == 'positive_integer':
            if not (input_value.isdigit() and int(input_value) > 0):
                return False, "Invalid input. Please enter a positive integer."
            
        elif validation_type == 'positive_float':
            try:
                value = float(input_value)
                if value <= 0:
                    return False, "Value must be a positive float."
            except ValueError:
                return False, "Invalid input. Please enter a valid floating-point number."
        
    return True, "Valid input."

def prompt_and_validate(prompt_message, validation_types, error_message, initial_value=None):
    """
    Prompts the user for input, validates it according to the specified type(s), and includes a confirmation step.
    Designed to work with a wide range of input types and validation criteria. Now supports multiple validation types.

    Parameters:
        prompt_message (str): The message to display when prompting the user.
        validation_types (Union[str, List[str]]): The type(s) of validation to apply.
        error_message (str): The message to display upon validation failure.
        initial_value (str, optional): An initial value to validate without prompting. Defaults to None.

    Returns:
        str: A validated and confirmed input according to the validation type(s).
    """
    
    if initial_value is not None:
        is_valid, message = is_valid_input(initial_value, validation_types)
        if is_valid:
            confirmation_prompt = f"Confirm initial input '{initial_value}'? (Y/N): "
            confirmation = input(confirmation_prompt).strip().upper()
            confirmation_is_valid, _ = is_valid_input(confirmation, 'yes_no')
            if confirmation_is_valid and confirmation == 'Y':
                return initial_value
            else:
                print("Initial value not confirmed. Please enter the value again.")
                print()

    while True:
        user_input = input(prompt_message).strip()
        is_valid, validation_message = is_valid_input(user_input, validation_types)
        if is_valid:
            confirmation_prompt = f"Confirm input '{user_input}'? (Y/N): "
            confirmation = input(confirmation_prompt).strip().upper()
            print()
            confirmation_is_valid, _ = is_valid_input(confirmation, 'yes_no')
            if confirmation_is_valid and confirmation == 'Y':
                return user_input
            else:
                print("Input not confirmed. Please re-enter the value.")
                print()
        else:
            print(f"{error_message}")
            print(f"{validation_message}")
            print()

def collect_customer_info():
    """
    Collects customer information through prompts and validates each input according to specified criteria.
    The information collected includes personal details, address, contact, and insurance preferences.
    Validation is performed by a helper function `prompt_and_validate`.
    Upon successful validation, inputs are formatted appropriately (e.g., title casing for names, uppercasing for postal codes).

    Returns:
        dict: A dictionary containing all the validated and formatted customer information.
    """
    
    first_name = prompt_and_validate(
        "Enter customer's first name: ", 
        ['name', 'long'],  
        "Please use only allowed characters and ensure the name is no longer than 5 characters."
    ).title()

    last_name = prompt_and_validate(
        "Enter customer's last name: ", 
        ['name', 'long'],  
        "Please use only allowed characters and ensure the name is no longer than 10 characters."
    ).title()

    address = prompt_and_validate(
        "Enter customer's street address: ", 
        'empty',  
        "The address cannot be empty. Please enter a valid street address."
    )
    
    city = string.capwords(prompt_and_validate(
        "Enter customer's city: ", 
        ['name', 'empty'],  
        "Please use only allowed characters for the city name and ensure it is not empty."
    ))

    province = prompt_and_validate(
        "Enter customer's province (abbreviation): ", 
        ['province', 'empty'],
        "Please enter a valid province abbreviation. It cannot be empty."
    ).upper()

    postal_code = prompt_and_validate(
        "Please enter the postal code (Format: X1X1X1): ", 
        ['postal_code', 'empty'],
        "Please enter a valid postal code in the format X1X1X1 without spaces."
    ).upper().replace(" ", "")

    phone_number = prompt_and_validate(
        "Enter customer's phone number (10 digits): ", 
        ['phone_number', 'empty'],
        "Please enter a valid 10-digit numeric phone number without any spaces or special characters."
    )

    number_of_cars = int(prompt_and_validate(
        "Enter the number of cars being insured: ", 
        ['positive_integer', 'empty'],  
        "Please enter a positive integer for the number of cars."
    ))

    extra_liability = prompt_and_validate(
        "Do you want extra liability coverage? (Y/N): ", 
        'yes_no', 
        "Please answer Yes or No by typing Y or N."
    ).upper()

    glass_coverage = prompt_and_validate(
        "Do you want glass coverage? (Y/N): ", 
        'yes_no', 
        "Please answer Yes or No by typing Y or N."
    ).upper()

    loaner_car = prompt_and_validate(
        "Do you want a loaner car coverage? (Y/N): ", 
        'yes_no', 
        "Please answer Yes or No by typing Y or N."
    ).upper()

    return {
        'first_name': first_name,
        'last_name': last_name,
        'address': address,
        'city': city,
        'province': province,
        'postal_code': postal_code,
        'phone_number': phone_number,
        'number_of_cars': number_of_cars,
        'extra_liability': extra_liability,
        'glass_coverage': glass_coverage,
        'loaner_car': loaner_car
    }

def get_claims():
    claims = [] 
    
    while True:
        user_input = input("Enter claim number (or 'done' to finish): ").strip()
        confirmation_prompt = f"Confirm initial input '{user_input}'? (Y/N): "
        confirmation = input(confirmation_prompt).strip().upper()
        confirmation_is_valid, _ = is_valid_input(confirmation, 'yes_no')
        if confirmation_is_valid and confirmation == 'Y':
            if user_input.lower() == 'done':
                print()
                break
            if not user_input.isdigit():
                print("Please enter a numeric value.")
                print()
                continue

        
        claim_number = user_input

        # Prompt for and validate each component of the date
        claim_year = prompt_and_validate(
            "Enter the year of the claim date (YYYY): ",
            "year",
            "Invalid year. Please enter a valid year between 1900 and 2099."
        )

        claim_month = prompt_and_validate(
            "Enter the month of the claim date (MM): ",
            "month",
            "Invalid month. Please enter a value between 1 and 12."
        )

        claim_day = prompt_and_validate(
            "Enter the day of the claim date (DD): ",
            "day",
            "Invalid day. Please enter a value between 1 and 31."
        )

        # Combine the date components
        claim_date = f"{claim_year}-{claim_month.zfill(2)}-{claim_day.zfill(2)}"

        claim_amount = float(prompt_and_validate(
            "Enter claim amount: $", 
            "positive_float", 
            "Enter a valid positive number for the amount."
        ))
        
        existing_claim = next((claim for claim in claims if claim['number'] == claim_number), None)
        if existing_claim:
            print(f"Duplicate claim number found. Updating amount for claim number {claim_number}.")
            existing_claim['amount'] = claim_amount 
        else:
            claims.append({'number': claim_number, 'date': claim_date, 'amount': claim_amount})

    return claims

def get_payment_info(total_cost):
    """
    Collects payment method and down payment amount from the user.

    The function prompts the user to select a payment method by entering a single letter corresponding to
    either full payment, monthly payments, or an initial down payment with subsequent payments. If the user
    selects the option for an initial down payment ('D'), they are then prompted to enter the amount for
    this down payment.

    The selection and input are validated to ensure they match expected formats and values. The payment method
    must be one of the predefined options, and the down payment, if provided, must be a positive numerical value.

    Returns:
        tuple: A tuple containing two elements:
               - The full word string of the selected payment method ('Full', 'Monthly', 'Down Pay').
               - The amount of down payment as a float, or None if not applicable.
    """

    # Mapping from single-letter inputs to full-word descriptions of payment methods.
    payment_map = {'F': 'Full', 'M': 'Monthly', 'D': 'Down Pay'}
    
    # Continuously prompt the user until a valid payment method is selected.
    while True:
        payment_letter = input("Enter payment method (F = Full, M = Monthly, D = Down Pay): ").strip().upper()
        if payment_letter in payment_map:
            payment_method = payment_map[payment_letter]
            break
        else:
            print("Invalid payment method. Please enter 'F', 'M', or 'D'.")
    
    # Initialize down payment to None
    down_payment = None
    
    # Prompt for down payment amount if 'Down Pay' option is selected.
    if payment_method == 'Down Pay':
        max_down_payment = total_cost - (MONTHLY_PAYMENT_PROCESSING_FEE * NUM_PAYMENTS)
        while True:
            try:
                down_payment = float(input("Enter the amount of the down payment: $").strip())
                if down_payment < 0:
                    print("The down payment cannot be negative. Please enter a positive value.")
                elif down_payment > max_down_payment:
                    print(f"The down payment must not exceed {format_currency(max_down_payment)}. Please enter a valid amount.")
                else:
                    break
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")

    # Return a tuple containing two elements
    return payment_method, down_payment



#   |-----------------------|   #
#   | CALCULATION FUNCTIONS |   #
#   |-----------------------|   #

def calculate_insurance_premium(num_cars, extra_liability, glass_coverage, loaner_car):
    """
    Calculates the total insurance premium and additional coverage costs for insuring one or more cars.
    
    The base premium for the first car is adjusted by a discount for each additional car. Additional costs
    are incurred if extra liability, glass coverage, or loaner car options are selected. The function returns
    a dictionary summarizing the total premium and the cost of each selected option.
    
    Parameters:
        num_cars (int): The number of cars being insured.
        extra_liability (str): Indicates if extra liability coverage is selected ('Y' for yes, 'N' for no).
        glass_coverage (str): Indicates if glass coverage is selected ('Y' for yes, 'N' for no).
        loaner_car (str): Indicates if loaner car coverage is selected ('Y' for yes, 'N' for no).
    
    Returns:
        dict: A dictionary containing the total premium and additional costs for selected coverages. Includes
              - 'premium': The total insurance premium (float).
              - 'extra_liability_cost': The total cost of extra liability coverage (float).
              - 'glass_coverage_cost': The total cost of glass coverage (float).
              - 'loaner_car_cost': The total cost of loaner car coverage (float).
    """
    
    # Initial premium calculation for all cars, considering discounts for additional cars
    premium = BASIC_PREMIUM + (BASIC_PREMIUM * (1 - ADDITIONAL_CAR_DISCOUNT) * (num_cars - 1))

    # Calculate extra charges
    # Calculate costs for selected coverages
    extra_liability_cost = EXTRA_LIABILITY_COST_PER_CAR * num_cars if extra_liability == 'Y' else 0
    glass_coverage_cost = GLASS_COVERAGE_COST_PER_CAR * num_cars if glass_coverage == 'Y' else 0
    loaner_car_cost = LOANER_CAR_COST_PER_CAR * num_cars if loaner_car == 'Y' else 0

    # Add additional costs to the premium
    total_premium = premium + extra_liability_cost + glass_coverage_cost + loaner_car_cost
    
    # Return a dictionary with all values
    return {
        'premium': premium,
        'total premium': total_premium,
        'extra_liability_cost': extra_liability_cost,
        'glass_coverage_cost': glass_coverage_cost,
        'loaner_car_cost': loaner_car_cost,
    }

def calculate_total_cost(premium):
    """
    Calculates the Harmonized Sales Tax (HST) on an insurance premium and the overall total cost including the HST.

    This function takes the total insurance premium as input and applies the HST rate to compute the tax amount.
    It then adds this tax amount to the original premium to determine the total cost. The HST rate is defined by
    a constant `HST_RATE`. This function returns both the computed HST amount and the total cost including HST.

    Parameters:
        premium (float): The total insurance premium before tax.
    
    Returns:
        tuple: A tuple containing two float values:
               - The first element is the HST amount calculated on the insurance premium.
               - The second element is the total cost including the HST.
    """

    # Calculate the HST based on the given premium
    hst = premium * HST_RATE

    # Calculate the total cost by adding the HST to the premium
    total_cost = premium + hst
    
    # Returns a tuple containing two float values
    return hst, total_cost

def calculate_monthly_payments(total_cost, payment_method, down_payment=None):
    """
    Calculates the monthly payment amount for an insurance policy based on the total cost, payment method, and
    an optional down payment.

    The function takes into account the total cost of the insurance, the payment method selected by the customer
    ('Full', 'Monthly', or 'Down Pay'), and any initial down payment made. If the payment method is 'Full', the
    function returns None, indicating no monthly payments are required. For 'Monthly' or 'Down Pay' methods, it
    calculates the monthly payments considering any down payment and adds a processing fee to each monthly payment.
    
    The number of payments and the monthly payment processing fee are determined by constants `NUM_PAYMENTS` and
    `MONTHLY_PAYMENT_PROCESSING_FEE`, respectively.

    Parameters:
        total_cost (float): The total cost of the insurance policy.
        payment_method (str): The payment method chosen by the customer, which can be 'Full', 'Monthly', or 'Down Pay'.
        down_payment (float, optional): The down payment amount, if any. Defaults to None.

    Returns:
        float or None: The amount of each monthly payment if the payment method involves monthly payments; otherwise, None.
    """

    # No monthly payments are needed if the payment is made in full.        
    if payment_method == 'Full':
        return None
    else:
        # Adjust the total cost by subtracting any down payment provided.
        adjusted_cost = total_cost - down_payment if down_payment else total_cost
        
        # Calculate monthly payments by dividing the adjusted cost by the number of payments
        # and adding the processing fee to each payment.
        monthly_payment = (adjusted_cost / NUM_PAYMENTS) + MONTHLY_PAYMENT_PROCESSING_FEE
        
        # Returns the monthly payment as an amount, or none.
        return monthly_payment
    

    # Main workflow function



#   |------------------|   #
#   | OUTPUT FUNCTIONS |   #
#   |------------------|   #
    
def format_currency(value):
    """Format a number as a currency."""
    return "${:,.2f}".format(value)

def format_date(date_value):
    """Format a datetime object into a more user-friendly string."""
    return date_value.strftime('%Y-%m-%d')

def prepare_customer_info_display(customer_info):
    """
    Formats customer information for display by combining and rearranging data entries.

    This function takes a dictionary containing customer information, combines first and last names into
    a full name, combines city, province, and postal code into one line, and prepares these details along
    with the street address and phone number for display. It ensures that if certain pieces of information
    are missing, the function still proceeds without errors by providing default empty values.

    Parameters:
        customer_info (dict): A dictionary containing keys like 'first_name', 'last_name', 'phone_number',
                              'address', 'city', 'province', and 'postal_code' with corresponding values.

    Returns:
        dict: A dictionary formatted for display, containing keys for 'Full Name', 'Phone Number', 'Street',
              and 'City' with their corresponding values formatted and combined appropriately.
    """
    
    # Combine first name and last name into a full name; handle missing values with defaults.
    full_name = f"{customer_info.get('first_name', '')} {customer_info.get('last_name', '')}"

    # Retrieve phone number; handle missing value with a default.
    phone_number = customer_info.get('phone_number', '')
    
    # Combine city, province, and postal code into one formatted string; handle missing values with defaults.
    city_province = f"{customer_info.get('city', '')}, {customer_info.get('province', '')}, {customer_info.get('postal_code')}"

    # Retrieve street address; handle missing value with a default.
    address = f"{customer_info.get('address', '')}"

    # Preparing display variables
    display_info = {
        "Full Name": full_name,
        "Phone Number": phone_number,
        "Street": address,
        "City": city_province 
    }

    # Return a dictionary formatted for display
    return display_info

def generate_and_display_receipt(customer_info, claims, premium_details, hst, total_cost, payment_method, down_payment, monthly_payment, total_premium):
    """
    Generates and displays a receipt with detailed insurance transaction information, including customer details,
    claims, premium breakdown, tax (HST), total cost, payment method, and payments schedule.

    Parameters:
        customer_info (dict): Customer personal information.
        claims (list): Claims data, each claim represented by a dictionary.
        premium_details (dict): Breakdown of the insurance premium costs.
        hst (float): Calculated HST amount on the premium.
        total_cost (float): The total cost of the insurance, including HST.
        payment_method (str): Selected payment method ('Full', 'Monthly', or 'Down Pay').
        down_payment (float or None): Down payment amount, if applicable.
        monthly_payment (float or None): Monthly payment amount, if applicable.
        total_premium (float): Total premium before taxes.

    Note: This function utilizes helper functions such as `format_date` and `format_currency` to format the dates
    and currency values for display.
    """


    #   |------------|   #
    #   | FORMATTING |   #
    #   |------------|   #

    # Format policy number for display
    DisplayPolicyNumber = f"{NEXT_POLICY_NUMBER}"

    # Format current date and future payment dates using a datetime format helper
    DisplayInvoiceDate = datetime.now().strftime('%Y-%b-%d')
    
    # Calculate the first payment date as the first day of the next month
    next_month = datetime.now().replace(day=28) + timedelta(days=4)
    DisplayFirstPaymentDate = next_month.replace(day=1).strftime('%Y-%b-%d')

    # Format financial figures using a currency format helper
    DisplayPremium = format_currency(premium_details['premium'])
    DisplayTotalCost = format_currency(total_cost)
    DisplayHST = format_currency(hst)
    DisplayPaymentMethod = f"{payment_method}"
    DisplayDownPayment = format_currency(down_payment) if down_payment else "N/A"
    DisplayMonthlyPayment = format_currency(monthly_payment) if monthly_payment else "N/A"

    # Format customer information for display
    Display_customer_info = prepare_customer_info_display(customer_info)

     # Format additional premium costs
    DisplayExtraLiabilityCost = format_currency(premium_details['extra_liability_cost'])
    DisplayGlassCoverageCost = format_currency(premium_details['glass_coverage_cost'])
    DisplayLoanerCarCost = format_currency(premium_details['loaner_car_cost'])
    DisplayTotalPremium = format_currency(total_premium)
    
    # Format each claim for display, including claim number, date, and amount
    DisplayClaims = []
    for claim in claims:
        claim_date_formatted = datetime.strptime(claim['date'], '%Y-%m-%d').strftime('%Y-%b-%d')
        DisplayClaims.append({
            'number': claim['number'],
            'date': claim_date_formatted,
            'amount': format_currency(claim['amount'])
        })

    #   |---------|   #
    #   | RECEIPT |   #
    #   |---------|   #
        

    print(f"")
    print(f"")
    print(f"    ____________________________________________________________ ")
    print(f"   |0        1         2         3         4         5         6|")
    print(f"   |123456789012345678901234567890123456789012345678901234567890|")
    print(f"   |____________________________________________________________|")
    print(f"   |         ------- One Stop Insurance Policy --------         |")
    print(f"   |                       Policy - #{DisplayPolicyNumber:<10s}                 |")
    print(f"   |    -------------------              -------------------    |")
    print(f"   | ---------- Current Invoice Date -- {DisplayInvoiceDate:>10s} ----------- |")
    print(f"   | ----------   First Payment Date -- {DisplayFirstPaymentDate:>10s} ----------- |")             
    print(f"   |____________________________________________________________|")
    print(f"   |          --------  Customer Information  --------          |")
    print(f"   |                                                            |")
    for key, value in Display_customer_info.items():
        print(f"   | {key:>22s} -- {value:<33s}|")
    print(f"   |____________________________________________________________|")
    print(f"   |                 -----------  Premium Details  -----------  |")
    print(f"   |        1STOP                                               |")
    print(f"   |     11STOP11    Number  of Cars  ----  {customer_info['number_of_cars']}  ----  {DisplayPremium:>9s}  |")
    print(f"   |   1STOP1STOP    Extra Liability  ----  {customer_info['extra_liability']}  ----  {DisplayExtraLiabilityCost:>9s}  |")   
    print(f"   |        1STOP    Glass  Coverage  ----  {customer_info['glass_coverage']}  ----  {DisplayGlassCoverageCost:>9s}  |")
    print(f"   |        1STOP         Loaner Car  ----  {customer_info['loaner_car']}  ----  {DisplayLoanerCarCost:>9s}  |")
    print(f"   |        1STOP     __________________________________________|")
    print(f"   |        1STOP                                               |")
    print(f"   |        1STOP      Total Premium  -------------  {DisplayTotalPremium:>9s}  |")
    print(f"   |        1STOP         HST Charge  -------------  {DisplayHST:>9s}  |")
    print(f"   |  1STOP1STOP1STOP1   _______________________________________|")
    print(f"   |  1STOP1STOP1STOP1    Total Cost  -------------  {DisplayTotalCost:>9s}  |")
    print(f"   |____________________________________________________________|")
    print(f"   |              ------  Payment  Details  ------              |")
    print(f"   |                                                            |")
    if payment_method != 'Full':
        print(f"   |          ----  Payment Method ----- {DisplayPaymentMethod:>9s} ----         |")
        print(f"   |          ----    Down Payment ----- {DisplayDownPayment:>9s} ----         |")
        print(f"   |          ---- Monthly Payment ----- {DisplayMonthlyPayment:>9s} ----         |")
    else:
        print(f"   |                 Payment Method: Full Payment               |")
    if claims:
        print(f"   |____________________________________________________________|")
        print(f"   |              ------  Claim(s) Details  --------            |")
        print(f"   |                                                            |")
        print(f"   |              Claim #    Claim Date       Amount            |")
        print(f"   |------------------------------------------------------------|")
        for display_claim in DisplayClaims:
            print(f"   |                {display_claim['number']:>5s},   {display_claim['date']:>11s},   {display_claim['amount']:>9s}           |")
    else:
        print(f"   |____________________________________________________________|")
        print(f"   |            --------  Claim(s) Details  --------            |")
        print(f"   |                                                            |")
        print(f"   |                   Claims History: None :)                  |")
        print(f"   |____________________________________________________________|")
    print(f"   |                                                            |")
    print(f"   |       Thank you for choosing One Stop Insurance Company    |")
    print(f"   |____________________________________________________________|")
    print(f"")
    print(f"")
    print(f"")
    print(f"")
    print(f"Your policy data for policy number {DisplayPolicyNumber} has been saved successfully.")
    print()



#   |-------------------------|   #
#   | MAIN WORKFLOW FUNCTIONS |   #
#   |-------------------------|   #

def process_insurance_policy():
    """
    Orchestrates the processing of an insurance policy by sequentially executing steps that collect customer information,
    process claims, calculate the insurance premium and total costs, and finally, generate and display a detailed receipt.
    
    The function follows a structured workflow:
        1. Collects customer and insurance details.
        2. Calculates the insurance premium based on customer details and coverage selections.
        3. Calculates the total premium, including any extra charges for selected coverages.
        4. Determines the total cost, including applicable taxes (HST).
        5. Gathers payment information, including the payment method and any down payment.
        6. Calculates monthly payments, if necessary, based on the selected payment method.
        7. Generates and displays a detailed receipt for the customer.
        8. Increments the policy number to prepare for processing the next policy.
    
    Uses global variable:
        NEXT_POLICY_NUMBER (int): The policy number for the current insurance policy, automatically incremented to prepare for the next policy.
    """

    global NEXT_POLICY_NUMBER

    # Announce the processing of the current policy number
    print(f"")
    print(f"Processing Policy Number: {NEXT_POLICY_NUMBER}")
    print(f"")

    # Step 1: Collect customer and insurance details
    customer_info = collect_customer_info()
    claims = get_claims()

    # Step 2: Calculate insurance premium
    premium_details = calculate_insurance_premium(
        customer_info['number_of_cars'],
        customer_info['extra_liability'],
        customer_info['glass_coverage'],
        customer_info['loaner_car']
    )

    # Step 3: Calculate total premium including extra charges
    total_premium = premium_details['total premium']

    # Step 4: Calculate total cost including HST
    hst, total_cost = calculate_total_cost(total_premium)

    # Step 5: Collect payment information
    payment_method, down_payment = get_payment_info(total_cost)

    # Step 6: Calculate monthly payments if necessary
    monthly_payment = calculate_monthly_payments(total_cost, payment_method, down_payment)

    # Step 7: Generating and displaying the receipt
    generate_and_display_receipt(customer_info, claims, premium_details, hst, total_cost, payment_method, down_payment, monthly_payment, total_premium)
    
    # Step 8: Increment policy number for the next customer     
    NEXT_POLICY_NUMBER += 1    

def main():
    """
    Main function to repeatedly process insurance policies based on user input.
    
    This function calls `process_insurance_policy` to handle the details of a single insurance policy processing.
    After processing, it prompts the user to decide whether to process another policy. This loop continues until
    the user chooses not to process another policy, at which point a thank you message is displayed, and the program
    terminates.
    """

    continue_processing = True
    while continue_processing:
        # Process a single insurance policy
        process_insurance_policy()

        # Ask the user if they want to process another policy
        user_decision = prompt_and_validate("Process another insurance policy? (Y/N): ", "yes_no", "Please enter Y/N for Yes or No")
        
        # Break the loop if the user decides not to continue
        if user_decision.upper() != 'Y':
            continue_processing = False

    # Display a thank you message upon exiting the loop        
    print("Thank you for using the One Stop Insurance Company program.")

if __name__ == "__main__":
    main()
