
from sqlconnection import connection

cursor = connection.cursor()

# create tables
create_users_table = """
CREATE TABLE IF NOT EXISTS USERS (
     User_ID VARCHAR(20) PRIMARY KEY UNIQUE,
     Username VARCHAR(20) NOT NULL,
     User_Password VARCHAR(60) NOT NULL,
     User_Role ENUM('Admin', 'Candidate', 'Party_worker', 'Voter') NOT NULL,
     created_at TIMESTAMP NOT NULL
);
"""

create_voter_table = """
CREATE TABLE IF NOT EXISTS VOTER (
    Voter_ID INT PRIMARY KEY UNIQUE,
    User_ID VARCHAR(20) NOT NULL,
    Voter_Name VARCHAR(255) NOT NULL,
    Voter_FatherOrHusband_Name VARCHAR(255),
    Voter_Gender VARCHAR(10),
    Voter_Marital_Status VARCHAR(20),
    Voter_Age INT CHECK (Voter_Age >= 18),
    Voter_Educational_Qualification VARCHAR(255) NOT NULL,
    Voter_Profession VARCHAR(255) NOT NULL,
    Voter_Income_Per_Month DECIMAL(10, 2) CHECK (Voter_Income_Per_Month >= 0),
    Voter_Income_Per_Year DECIMAL(10, 2) CHECK (Voter_Income_Per_Year >= 0),
    Voter_Family_Income_Per_Month DECIMAL(10, 2) CHECK (Voter_Family_Income_Per_Month >= 0),
    Votes_In_Family INT CHECK (Votes_In_Family >= 0),
    Votes_In_Extended_Family INT CHECK (Votes_In_Extended_Family >= 0),
    Is_Politically_Neutral BOOLEAN,
    Government_Benefits BOOLEAN,
    Family_Government_Benefits BOOLEAN,
    Work_Location VARCHAR(255),
    Accepts_Money_From_Political_Party BOOLEAN,
    Family_Accepts_Money_From_Political_Party BOOLEAN,
    Police_Cases_On_Voter INT CHECK (Police_Cases_On_Voter >= 0),
    Police_Cases_On_Family_Members INT CHECK (Police_Cases_On_Family_Members >= 0),
    Has_Own_House BOOLEAN,
    Native_Or_Migrant VARCHAR(20),
    Mother_Tongue VARCHAR(255),
    Opinion_On_Present_Government TEXT,
    Opinion_Label_On_Present_Government VARCHAR(50),
    Opinion_On_Local_MLA TEXT,
    Opinion_Label_On_Local_MLA VARCHAR(50),
    Local_MLA_Political_Party VARCHAR(255),
    Opinion_On_Opposition_Party_MLA_Candidate TEXT,
    Opinion_Label_On_Opposition_Party_MLA_Candidate VARCHAR(50),
    Opposition_Party_MLA_Candidate_Political_Party VARCHAR(255),
    Opinion_On_Local_Corporator_Village_President TEXT,
    Opinion_Label_On_Local_Corporator_Village_President VARCHAR(50),
    Local_Corporator_Political_Party VARCHAR(255),
    Preferred_Political_Party_To_Vote VARCHAR(255),
    BPL BOOLEAN,
    Voter_Monthly_Spending DECIMAL(10, 2) CHECK (Voter_Monthly_Spending >= 0),
    Voter_Family_Monthly_Spending DECIMAL(10, 2) CHECK (Voter_Family_Monthly_Spending >= 0),
    Reservation_Category VARCHAR(255),
    Voted_In_Last_Election BOOLEAN,
    Voting_First_Time BOOLEAN,
    Constituency_Name VARCHAR(255) NOT NULL,
    Polling_Booth_Name VARCHAR(255) NOT NULL,
    Is_Voter_Handicap BOOLEAN,
    Members_Visited_Foreign_Country INT CHECK (Members_Visited_Foreign_Country >= 0),
    Dependents INT CHECK (Dependents >= 0),
    Has_Own_Car BOOLEAN,
    Has_Own_Bike BOOLEAN,
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_address_table = """
CREATE TABLE IF NOT EXISTS ADDRESS (
    Address_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT,
    User_ID VARCHAR(20) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Street_Name VARCHAR(255) NOT NULL,
    Ward VARCHAR(10) NOT NULL,
    Pin_Code VARCHAR(10) NOT NULL,
    Address_Latitude DECIMAL(10, 8) NOT NULL,
    Address_Longitude DECIMAL(11, 8) NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY(Voter_ID) REFERENCES VOTER(Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_contact_table ="""
CREATE TABLE IF NOT EXISTS CONTACT (
    Contact_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT,
    User_ID VARCHAR(20) NOT NULL,
    Phone_Number VARCHAR(15) UNIQUE,
    WhatsApp_Number VARCHAR(15) UNIQUE,
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY(Voter_ID) REFERENCES VOTER(Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_family_table = """
CREATE TABLE IF NOT EXISTS FAMILY (
    Family_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT,
    User_ID VARCHAR(20) NOT NULL,
    Number_of_Votes_In_Family INT CHECK (Number_of_Votes_In_Family >= 0),
    Number_of_Votes_In_Extended_Family INT CHECK (Number_of_Votes_In_Extended_Family >= 0),
    Members_Visited_Foreign_Country INT CHECK (Members_Visited_Foreign_Country >= 0),
    Dependents INT CHECK (Dependents >= 0),
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY (Voter_ID) REFERENCES VOTER (Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_religion_table = """
CREATE TABLE IF NOT EXISTS RELIGION (
    Religion_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT,
    User_ID VARCHAR(20) NOT NULL,
    Voter_Religion VARCHAR(255) NOT NULL,
    Voter_Caste VARCHAR(255) NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY(Voter_ID) REFERENCES VOTER(Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_political_affiliation_table = """
CREATE TABLE IF NOT EXISTS POLITICAL_AFFILIATION (
    Political_Affiliation_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT,
    User_ID VARCHAR(20) NOT NULL,
    Voter_Political_Party VARCHAR(255) NOT NULL,
    Local_MLA_Political_Party VARCHAR(255) NOT NULL,
    Opposition_Party_MLA_Candidate_Political_Party VARCHAR(255) NOT NULL,
    Local_Corporator_Political_Party VARCHAR(255) NOT NULL,
    Preferred_Political_Party_To_Vote VARCHAR(255) NOT NULL,
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY (Voter_ID) REFERENCES VOTER (Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_police_case_table = """
CREATE TABLE IF NOT EXISTS POLICE_CASE (
    Police_Case_ID INT AUTO_INCREMENT PRIMARY KEY,
    Voter_ID INT ,
    User_ID VARCHAR(20) NOT NULL,
    Police_Cases_On_Voter INT CHECK (Police_Cases_On_Voter >= 0),
    Police_Cases_On_Family_Members INT  CHECK (Police_Cases_On_Family_Members >= 0),
    FOREIGN KEY(User_ID) REFERENCES USERS(User_ID),
    FOREIGN KEY (Voter_ID) REFERENCES VOTER(Voter_ID),
    CONSTRAINT CHECK_ROLE CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) = 'Voter')
);
"""

create_payments_table =""" 
CREATE TABLE PAYMENTS (
    Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID VARCHAR(20) NOT NULL,
    Payment_DateTime DATETIME,
    Payment_Amount DECIMAL(10, 2),
    Currency VARCHAR(3),
    Payment_Method VARCHAR(255),
    Payment_Status VARCHAR(50),
    Payment_Gateway VARCHAR(255),
    Transaction_ID VARCHAR(255),
    Order_ID INT UNIQUE,
    Payment_Source VARCHAR(255),
    Tax_Amount DECIMAL(10, 2),
    Payment_Receipt VARCHAR(255),
    Payment_AuthorizationCode VARCHAR(50),
    Refund_Information TEXT,
    FOREIGN KEY (User_ID) REFERENCES USERS(User_ID),
    CONSTRAINT CHECK_ROLE_PAYMENT CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) IN ('Admin', 'Candidate','Party_worker'))
);
"""

create_subscriptions_table = """
CREATE TABLE SUBSCRIPTIONS (
    Subscription_ID INT AUTO_INCREMENT PRIMARY KEY,
    Subscription_Type ENUM('Individual', 'Group'),
    User_ID VARCHAR(20) NOT NULL,
    Plan_ID INT unique,
    Start_Date DATE,
    End_Date DATE,
    Subscription_status ENUM('Active', 'Pending', 'Cancelled', 'Expired'),
    Billing_Cycle ENUM('monthly', 'annually'),
    Payment_Method VARCHAR(255),
    Auto_Renew ENUM('YES', 'NO'),
    Price DECIMAL(10, 2),
    Payment_Status ENUM('Done', 'Pending', 'Failed'),
    Last_Payment_Date DATE,
    Next_Billing_Date DATE,
    Billing_Address VARCHAR(255),
	FOREIGN KEY (User_ID) REFERENCES USERS(User_ID),
    CONSTRAINT CHECK_ROLE_SUBSCRIPTION CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) IN ('Admin','Candidate','Party_worker'))
);
"""

create_user_activity_table = """
CREATE TABLE USER_ACTIVITY (
    Activity_ID INT AUTO_INCREMENT PRIMARY KEY,
    User_ID VARCHAR(20) NOT NULL,
    LoggedIn_Time TIMESTAMP,
    LoggedOut_Time TIMESTAMP,
    Duration INT,
    Pages_Accessed INT,
    Transactions_done INT,
	FOREIGN KEY (User_ID) REFERENCES USERS(User_ID),
    CONSTRAINT CHECK_ROLE_USER_ACTIVITY CHECK ((SELECT User_Role FROM USERS WHERE User_ID = User_ID) IN ('Admin','Candidate','Party_worker'))
);
"""

cursor.execute(create_users_table)
cursor.execute(create_voter_table)
cursor.execute(create_address_table)
cursor.execute(create_contact_table)
cursor.execute(create_family_table)
cursor.execute(create_religion_table)
cursor.execute(create_political_affiliation_table)
cursor.execute(create_police_case_table)
cursor.execute(create_payments_table)
cursor.execute(create_subscriptions_table)
cursor.execute(create_user_activity_table)

connection.commit()
connection.close()
