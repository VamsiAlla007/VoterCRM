import streamlit as st
import pandas as pd
import xlsxwriter
import re


def validate_integer(value, field_name):
    return bool(re.match("^[0-9]+$", value)), f"{field_name} should contain only Numbers."

def validate_string(value, field_name):
    return isinstance(value, str), f"{field_name} should be a valid string."

def validate_alphabets_and_space(value, field_name):
    return bool(re.match("^[A-Za-z ]+$", value)), f"{field_name} should contain only alphabets and spaces."

def validate_alpha_numeric(value, field_name):
    return bool(re.match("^[A-Za-z0-9]+$", str(value))), f"{field_name} should contain only alphabets and numbers."

def validate_boolean(value):
    return value in ['Yes', 'No'], f"Invalid value for {value}."

def validate_pin_code(pin_code):
    return bool(re.match("^\d{6}$", str(pin_code))), "Pin Code should be a 6-digit integer."

def validate_phone_number(phone_number):
    return bool(re.match("^[0-9]{10}$", str(phone_number))), "Phone Number should be a 10-digit integer."

def validate_gender(value):
    return value in ['Male', 'Female', 'Others'], "Invalid value for Voter Gender."

def validate_education(value):
    return value in ['Illiterate', 'Below 10th','Intermediate','Degree','Masters','PHD'], "Invalid value for Educational Qualification."

def validate_profession(value):
    return value in ['Self Employed', 'Govt Job','Private Job','Unemployed'], "Invalid value for Profession."

def validate_marital_status(value):
    return value in ['Single', 'Married','Widow'], "Invalid value for Marital Status."

def validate_yes_no(value):
    return value in ['Yes', 'No'], f"Invalid value for {value}."

def validate_age(age):
    return age > 18, f"Invalid age value: {age}. Age should be greater than 18."

def validate_opinion_label(value):
    return value in ['Very Bad', 'Bad', 'Good', 'Very Good', 'Excellent'], f"Invalid value for {value}."

def validate_reservation_category(value, field_name):
    return value in ['General', 'SC', 'ST', 'OBC','BC'], f"{field_name} is not a valid reservation category."

def validate_row(row):
    validations = [
        validate_integer(str(row['voter_number']), 'Voter Number'),
        validate_alphabets_and_space(row.get('voter_name', ''), 'Voter Name'),
        validate_alphabets_and_space(row['father_name'], 'Father/Husband Name'),
        validate_string(row['address'], 'Address'),
        validate_pin_code(row['pin_code']),
        validate_alpha_numeric(row['latitude'], 'Address Latitude'),
        validate_alpha_numeric(row['longitude'], 'Address Longitude'),
        validate_phone_number(row['phone_number']),
        validate_phone_number(row['whatsapp_number']),
        validate_gender(row['voter_gender']),
        validate_marital_status(row['marital_status']),
        validate_age(row['voter_age']),
        validate_yes_no(row['is_handicap']),
        validate_education(row['education']),
        validate_profession(row['profession']),
        validate_integer(str(row['income_per_month']), 'Voter Income Per Month'),
        validate_integer(str(row['income_per_year']), 'Voter Income Per Year'),
        validate_integer(str(row['family_income_per_month']), 'Voter Family Income Per Month'),
        validate_integer(str(row['votes_in_family']), "Number of Votes in Voter's Family"),
        validate_integer(str(row['extended_family_votes']), "Number of Votes in Voter's Extended Family"),
        validate_integer(str(row['family_members_visited_foreign_country']), 'Number of Family Members Visited Foreign Country'),
        validate_integer(str(row['number_of_dependents']), 'Number of Dependents'),
        validate_string(row['religion'], 'Voter Religion'),
        validate_string(row['caste'], 'Voter Caste'),
        validate_string(row['political_party'], 'Voter Political Party'),
        validate_yes_no(row['politically_neutral']),
        validate_yes_no(row['government_benefits']),
        validate_yes_no(row['family_government_benefits']),
        validate_string(row['work_location'], 'Voter Work Location'),
        validate_yes_no(row['accepts_money']),
        validate_yes_no(row['family_accepts_money']),
        validate_integer(str(row['police_cases']), 'Number of Police Cases on Voter'),
        validate_integer(str(row['family_police_cases']), 'Number of Police Cases on Voter\'s Family Members'),
        validate_yes_no(row['own_house']),
        validate_yes_no(row['own_car']),
        validate_yes_no(row['own_bike']),
        validate_yes_no(row['native_or_migrated']),
        validate_alphabets_and_space(row['mother_tongue'], 'Voter Mother Tongue'),
        validate_string(row['government_opinion'], 'Voter Opinion on Present Government'),
        validate_opinion_label(row['government_opinion_label']),
        validate_string(row['mla_opinion'], 'Voter Opinion on Local MLA'),
        validate_opinion_label(row['mla_opinion_label']),
        validate_string(row['mla_political_party'], 'Local MLA Political Party'),
        validate_string(row['opposition_mla_opinion'], 'Voter Opinion on Opposition Party MLA Candidate'),
        validate_opinion_label(row['opposition_mla_opinion_label']),
        validate_string(row['opposition_mla_political_party'], 'Opposition Party MLA Candidate Political Party'),
        validate_string(row['coporator_opinion'], 'Voter Opinion on Local Corporator or Village President'),
        validate_opinion_label(row['coporator_opinion_label']),
        validate_string(row['local_coporator_party'], 'Local Corporator Political Party'),
        validate_string(row['vote_preference'], 'Vote Preference'),
        validate_yes_no(row['bpl_status']),
        validate_integer(str(row['monthly_spending']), 'Voter Monthly Spending'),
        validate_integer(str(row['family_monthly_spending']), 'Voter Family Monthly Spending'),
        validate_reservation_category(row['reservation_category'], 'Reservation Category'),
        validate_yes_no(row['voted_last_election']),
        validate_alphabets_and_space(row['street_name'], 'Street Name'),
        validate_alphabets_and_space(row['ward'], 'Ward'),
        validate_yes_no(row['first_time_voter']),
        validate_alphabets_and_space(row['constituency_name'], 'Constituency Name'),
        validate_alphabets_and_space(row['polling_booth_name'], 'Polling Booth Name'),
    ]

    valid = all(result[0] for result in validations)
    messages = [result[1] for result in validations if not result[0]]

    return valid, messages

def download_excel(form_data):
    is_valid, messages = validate_row(form_data)

    if is_valid:
        output_file = "VoterData.xlsx"
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet("VoterData")

        # Write headers
        headers = form_data.keys()
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        row_num = 1
        for col_num, value in enumerate(form_data.values()):
            worksheet.write(row_num, col_num, value)

        workbook.close()

        st.success("Excel file downloaded successfully!")
    else:
        st.warning("Data validation failed. Please check the following issues:\n" + "\n".join(messages))

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        valid_rows = []
        invalid_rows = []

        for index, row in df.iterrows():
            is_valid, messages = validate_row(row)

            if is_valid:
                valid_rows.append(row)
            else:
                invalid_row = {column: row[column] for column in df.columns}
                invalid_rows.append(invalid_row)

        valid_df = pd.DataFrame(valid_rows).drop_duplicates()

        output_file = "valid_data.xlsx"
        valid_df.to_excel(output_file, index=False)

        if invalid_rows:
            invalid_df = pd.DataFrame(invalid_rows)
            invalid_df.to_excel("invalid_data.xlsx", index=False)

            st.warning("Some rows contain invalid data. Please check the 'invalid_data.xlsx' file for details.")
        else:
            st.success("All rows are valid. Data processed successfully!")

    else:
        st.warning("Please upload a file.")

def main():
    st.set_page_config(page_title="Voter Information", page_icon=":ballot_box_with_check:")

    st.title("Voter Information Form")

    # Ask the user whether to input data for a single voter or upload an Excel file
    option = st.radio("Choose an option:", ("Input Single Voter Data", "Upload Excel File"))

    if option == "Input Single Voter Data":
        # Create input elements for the form
        voter_number = st.number_input("Voter Number (Integer):", min_value=1, step=1)
        voter_name = st.text_input("Voter Name (Alphabets and space):")
        father_name = st.text_input("Father/Husband Name (Alphabets and space):")
        address = st.text_input("Address (String):")
        pin_code = st.number_input("Pin Code (6 digit integer):", min_value=100000, max_value=999999, step=1)
        latitude = st.text_input("Address Latitude (Alpha numeric):")
        longitude = st.text_input("Address Longitude (Alpha numeric):")
        phone_number = st.number_input("Phone Number (10 digit integer):", min_value=1000000000, max_value=9999999999,
                                       step=1)
        whatsapp_number = st.number_input("WhatsApp Number (10 digit integer):", min_value=1000000000,
                                          max_value=9999999999, step=1)
        voter_gender = st.selectbox("Voter Gender:", ["Male", "Female", "Others"])
        marital_status = st.selectbox("Marital Status:", ["Single", "Married","Widow"])
        voter_age = st.number_input("Voter Age (3 digit integer):", min_value=1, max_value=999, step=1)
        is_handicap = st.selectbox("Is Voter Handicap?", ["Yes", "No"])
        education = st.selectbox("Voter Educational Qualification:", ["Illiterate", "Below 10th","Intermediate","Degree","Masters","PHD"])
        profession = st.selectbox("Voter Profession:", ["Self Employed","Govt Job","Private Job","Unemployed"])
        income_per_month = st.number_input("Voter Income Per Month (Integer):", min_value=0, step=1)
        income_per_year = st.number_input("Voter Income Per Year (Integer):", min_value=0, step=1)
        family_income_per_month = st.number_input("Voter Family Income per Month (Integer):", min_value=0, step=1)
        votes_in_family = st.number_input("Number of Votes in Voter's Family (Integer):", min_value=0, step=1)
        extended_family_votes = st.number_input(
            "Number of Votes in Voter's Extended Family (in same constituency) (Integer):", min_value=0, step=1)
        family_members_visited_foreign_country = st.number_input(
            "Number of family members visited foreign country (Integer):", min_value=0, step=1)
        number_of_dependents = st.number_input("Number of dependents (Integer):", min_value=0, step=1)
        religion = st.text_input("Voter Religion:")
        caste = st.text_input("Voter Caste:")
        political_party = st.text_input("Voter Political Party:")
        politically_neutral = st.selectbox("Is Voter Politically Neutral?", ["Yes", "No"])
        government_benefits = st.selectbox("Does Voter Avail Government Benefits?", ["Yes", "No"])
        family_government_benefits = st.selectbox("Does Voter's Family Avail Government Benefits?", ["Yes", "No"])
        work_location = st.text_input("Voter Work Location:")
        accepts_money = st.selectbox("Does Voter Accept Money for Vote?", ["Yes", "No"])
        family_accepts_money = st.selectbox("Does Voter's Family Accept Money for Vote?", ["Yes", "No"])
        police_cases = st.number_input("Number of Police Cases on Voter (Integer):", min_value=0, step=1)
        family_police_cases = st.number_input("Number of Police Cases on Voter's Family Members (Integer):", min_value=0, step=1)
        own_house = st.selectbox("Does Voter Own a House?", ["Yes", "No"])
        own_car = st.selectbox("Does Voter Own a Car?", ["Yes", "No"])
        own_bike = st.selectbox("Does Voter Own a Bike?", ["Yes", "No"])
        native_or_migrated = st.selectbox("Is Voter Native or Migrated?", ["Yes", "No"])
        mother_tongue = st.text_input("Voter Mother Tongue:")
        government_opinion = st.text_input("Voter Opinion on Present Government:")
        government_opinion_label = st.selectbox("Voter Opinion Label on Present Government:", ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
        mla_opinion = st.text_input("Voter Opinion on Local MLA:")
        mla_opinion_label = st.selectbox("Voter Opinion Label on Local MLA:", ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
        mla_political_party = st.text_input("Local MLA Political Party:")
        opposition_mla_opinion = st.text_input("Voter Opinion on Opposition Party MLA Candidate:")
        opposition_mla_opinion_label = st.selectbox("Voter Opinion Label on Opposition Party MLA Candidate:", ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
        opposition_mla_political_party = st.text_input("Opposition Party MLA Candidate Political Party:")
        coporator_opinion = st.text_input("Voter Opinion on Local Corporator or Village President:")
        coporator_opinion_label = st.selectbox("Voter Opinion Label on Local Corporator or Village President:", ["Very Bad", "Bad", "Good", "Very Good", "Excellent"])
        local_coporator_party = st.text_input("Local Corporator Political Party:")
        vote_preference = st.text_input("Vote Preference:")
        bpl_status = st.selectbox("Is Voter Below Poverty Line (BPL)?", ["Yes", "No"])
        monthly_spending = st.number_input("Voter Monthly Spending (Integer):", min_value=0, step=1)
        family_monthly_spending = st.number_input("Voter Family Monthly Spending (Integer):", min_value=0, step=1)
        reservation_category = st.selectbox("Voter Reservation Category:", ["General", "SC", "ST", "OBC","BC",])
        voted_last_election = st.selectbox("Did Voter Vote in the Last Election?", ["Yes", "No"])
        street_name = st.text_input("Street Name:")
        ward = st.text_input("Ward:")
        first_time_voter = st.selectbox("Is Voter a First-Time Voter?", ["Yes", "No"])
        constituency_name = st.text_input("Constituency Name:")
        polling_booth_name = st.text_input("Polling Booth Name:")

        form_data = {
            'voter_number': voter_number,
            'voter_name': voter_name,
            'father_name': father_name,
            'address': address,
            'pin_code': pin_code,
            'latitude': latitude,
            'longitude': longitude,
            'phone_number': phone_number,
            'whatsapp_number': whatsapp_number,
            'voter_gender': voter_gender,
            'marital_status': marital_status,
            'voter_age': voter_age,
            'is_handicap': is_handicap,
            'education': education,
            'profession': profession,
            'income_per_month': income_per_month,
            'income_per_year': income_per_year,
            'family_income_per_month': family_income_per_month,
            'votes_in_family': votes_in_family,
            'extended_family_votes': extended_family_votes,
            'family_members_visited_foreign_country': family_members_visited_foreign_country,
            'number_of_dependents': number_of_dependents,
            'religion': religion,
            'caste': caste,
            'political_party': political_party,
            'politically_neutral': politically_neutral,
            'government_benefits': government_benefits,
            'family_government_benefits': family_government_benefits,
            'work_location': work_location,
            'accepts_money': accepts_money,
            'family_accepts_money': family_accepts_money,
            'police_cases': police_cases,
            'family_police_cases': family_police_cases,
            'own_house': own_house,
            'own_car': own_car,
            'own_bike': own_bike,
            'native_or_migrated': native_or_migrated,
            'mother_tongue': mother_tongue,
            'government_opinion': government_opinion,
            'government_opinion_label': government_opinion_label,
            'mla_opinion': mla_opinion,
            'mla_opinion_label': mla_opinion_label,
            'mla_political_party': mla_political_party,
            'opposition_mla_opinion': opposition_mla_opinion,
            'opposition_mla_opinion_label': opposition_mla_opinion_label,
            'opposition_mla_political_party': opposition_mla_political_party,
            'coporator_opinion': coporator_opinion,
            'coporator_opinion_label': coporator_opinion_label,
            'local_coporator_party': local_coporator_party,
            'vote_preference': vote_preference,
            'bpl_status': bpl_status,
            'monthly_spending': monthly_spending,
            'family_monthly_spending': family_monthly_spending,
            'reservation_category': reservation_category,
            'voted_last_election': voted_last_election,
            'street_name': street_name,
            'ward': ward,
            'first_time_voter': first_time_voter,
            'constituency_name': constituency_name,
            'polling_booth_name': polling_booth_name
        }

        if st.button("Submit"):
            download_excel(form_data)

    elif option == "Upload Excel File":
        uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

        if st.button("Process File"):
            process_uploaded_file(uploaded_file)

if __name__ == "__main__":
    main()

