# pip install mysql-connector-python streamlit
# pip install mysql-connector-python
from Insert_data import *
from sqlconnection import *

# Read user data from CSV
users_data = pd.read_csv('users_data.csv')

def fetch_voter_data():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(" SELECT * FROM VOTER")
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return []
    
class User:
    def __init__(self, user_ID,user_role,subscription_type,subscription_status):
        self.user_id = user_ID
        self.user_role = user_role
        self.susbscription_type = subscription_type
        self.susbscription_status = subscription_status

# Function to perform an action based on user role(Admin)

# Function to upload data from external sources 
file_content = "This is the content of the file to upload."

def check_permission_query(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            check_permission_query = f"SELECT * FROM USERS WHERE User_ID = '{user_id}'"
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role in ('Admin', 'Candidate', 'Party_worker'):
                check_user_role_query = f"SELECT * FROM USERS WHERE User_role = '{user_role}'"
                cursor.execute(check_user_role_query)
                connection.commit()
                print(f"User with ID {user_id} is admin.")
            else:
                print(f"User with ID {user_id} does not have permission")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error uploading data: {str(e)}")


def upload_data_from_external_source(user_id, user_role, file_content):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            check_permission_query = f"SELECT * FROM USERS WHERE User_ID = '{user_id}'"
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role in ('Admin', 'Candidate', 'Party_worker'):
                # User has permission, proceed to upload data
                print("Uploading data:")
                upload_query = f"INSERT INTO Uploads (User_ID, Upload_Time, File_Content) VALUES ('{user_id}', NOW(), '{file_content}')"
                cursor.execute(upload_query)
                connection.commit()
                print("Data uploaded successfully.")
            else:
                print("This action can be performed only by admin.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error uploading data: {str(e)}")


# Function to handle user submissions
def handle_submissions(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the user has permission to handle submissions
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role == 'Admin':
                print("Handling submissions:")
                submission_data = input("Enter the submission data: ")
                insert_submission_query = f"INSERT INTO Submissions (User_ID, Submission_Data) VALUES ('{user_id}', '{submission_data}')"
                cursor.execute(insert_submission_query)
                connection.commit()
                print("Submission handled successfully.")
            else:
                print(f"User with ID {user_id} does not have permission to handle submissions.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error handling submissions: {str(e)}")


# Function to manage shared data
def manage_shared_data(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the user has permission to manage shares
            check_permission_query = f"SELECT * FROM USERS WHERE User_ID = '{user_id}'"
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role in ('Admin', 'Candidate', 'Party_worker'):
                # if user has permission, proceed to manage shares
                print("Managing shares:")
                action = input("Enter the action (view/update/delete): ").lower()

                if action == 'view':
                    view_shares_query = f"SELECT * FROM SHARED_DATA WHERE User_ID = '{user_id}'"
                    cursor.execute(view_shares_query)
                    shares_data = cursor.fetchall()
                    if shares_data:
                        print("Shared data details:")
                        for share in shares_data:
                            print(share)
                    else:
                        print("No shared data records found.")

                elif action == 'update':
                    shared_data_id_to_update = input("Enter the Shared Data ID to update: ")
                    new_data = input("Enter the new data: ")
                    update_shared_data_query = f"UPDATE SHARED_DATA SET Data = '{new_data}' WHERE Shared_Data_ID = {shared_data_id_to_update}"
                    cursor.execute(update_shared_data_query)
                    connection.commit()
                    print(f"Shared data with ID {shared_data_id_to_update} updated successfully.")
                    print("Updating shared data information:")
                  
                elif action == 'delete':
                    shared_data_id_to_delete = input("Enter the Shared Data ID to delete: ")
                    delete_shared_data_query = f"DELETE FROM SHARED_DATA WHERE Shared_Data_ID = {shared_data_id_to_delete}"
                    cursor.execute(delete_shared_data_query)
                    connection.commit()
                    print(f"Shared data with ID {shared_data_id_to_delete} deleted successfully.")
                else:
                    print("Invalid action. Please enter 'view', 'update', or 'delete'.")
            else:
                print(f"User with ID {user_id} does not have permission to manage shares.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error managing shares: {str(e)}")


# Function to manage permissions
def manage_permissions(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the user has permission to manage permissions
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role == 'Admin':
                # User has permission, proceed to manage permissions
                print("Managing permissions:")
                print("1. Grant Permission")
                print("2. Revoke Permission")

                choice = input("Enter your choice (1 or 2): ")
                if choice == '1':
                    # Logic to grant permission
                    user_to_grant_permission = input("Enter the user ID to grant permission: ")
                    grant_permission_query = f"UPDATE USERS SET Permission = 'Granted' WHERE User_ID = '{user_to_grant_permission}'"
                    cursor.execute(grant_permission_query)
                    connection.commit()
                    grant_permission_query(user_to_grant_permission, user_id)
                    print(f"Permission granted to user with ID: {user_to_grant_permission} by {user.user_id}")

                elif choice == '2':
                    # Logic to revoke permission
                    user_to_revoke_permission = input("Enter the user ID to revoke permission: ")
                    revoke_permission_query = f"UPDATE USERS SET Permission = 'Revoked' WHERE User_ID = '{user_to_revoke_permission}'"
                    cursor.execute(revoke_permission_query)
                    connection.commit()
                    print(f"Permission revoked from user with ID: {user_to_revoke_permission} by {user.user_id}")
                    revoke_permission_query(user_to_revoke_permission, user_id)
                else:
                    print("Invalid choice. Please enter either 1 or 2.")
            else:
                print(f"User with ID {user_id} does not have permission to manage permissions.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error managing permissions: {str(e)}")


# Function to view usage logs
def view_usage_logs(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the user has permission to view usage logs
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()

            if user_permission and user_role in ['Admin', 'Candidate', 'Party_worker']:
            # User has permission, fetch and display usage logs
                fetch_logs_query = f"SELECT * FROM USER_ACTIVITY WHERE User_ID = '{user_id}'"
                cursor.execute(fetch_logs_query)
                logs = cursor.fetchall()
                if logs:
                    print("Viewing usage logs:")
                    for log in logs:
                        print(f"Activity ID: {log[0]}, LoggedIn Time: {log[2]}, LoggedOut Time: {log[3]}, Duration: {log[4]} seconds, Pages Accessed: {log[5]}, Transactions Done: {log[6]}")
                else:
                    print("No usage logs found.")
            else:
                print(f"User with ID {user_id} does not have permission to view usage logs.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error viewing usage logs: {str(e)}")


# Function to manage payments
def manage_payments(user_id, user_role):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the user has permission to manage payments
            cursor.execute(check_permission_query)
            user_permission = cursor.fetchone()
            if user_permission and user_role in ('Admin', 'Candidate', 'Party_worker'):
                # User has permission, proceed to manage payments
                print("Managing payments:")
                action = input("Enter the action (view/update/delete): ").lower()
                if action == 'view':
                    view_payments_query = f"SELECT * FROM PAYMENTS WHERE User_ID = '{user_id}'"
                    cursor.execute(view_payments_query)
                    payments_data = cursor.fetchall()
                    if payments_data:
                        print("Payment details:")
                        for payment in payments_data:
                            print(payment)
                    else:
                        print("No payment records found.")

                elif action == 'update':
                    payment_id_to_update = input("Enter the Payment ID to update: ")
                    print("Updating payment information:")
                    update_payment_query = f"UPDATE FROM PAYMENTS WHERE Payment_ID = {payment_id_to_update}"
                    cursor.execute(update_payment_query)
                    connection.commit()
                    print(f"Payment with ID {payment_id_to_update} updated successfully.")

                elif action == 'delete':
                    payment_id_to_delete = input("Enter the Payment ID to delete: ")
                    delete_payment_query = f"DELETE FROM PAYMENTS WHERE Payment_ID = {payment_id_to_delete}"
                    cursor.execute(delete_payment_query)
                    connection.commit()
                    print(f"Payment with ID {payment_id_to_delete} deleted successfully.")
                else:
                    print("Invalid action. Please enter 'view', 'update', or 'delete'.")
            else:
                print(f"User with ID {user_id} does not have permission to manage payments.")
        else:
            print("Database connection not established.")
    except Exception as e:
        print(f"Error managing payments: {str(e)}")


# Function to delete user data
def delete_user_data(user_id, user_role):
    try:
        if user_role == 'Admin':
            if connection.is_connected():
                cursor = connection.cursor()
                # Check if the user with the specified ID exists
                check_user_query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
                cursor.execute(check_user_query)
                existing_user = cursor.fetchone()
                if existing_user:
                    # User with ID exists, proceed with deletion
                    delete_query = f"DELETE FROM users WHERE user_id = '{user_id}'"
                    cursor.execute(delete_query)  # Execute the delete query
                    connection.commit()  # Commit the changes
                    print(f"Deleting data for user with ID: {user_id}")
                else:
                    print(f"User with ID {user_id} not found.")
        else:
            print(f"User with ID {user_id} does not have permission to delete data.")
    except Exception as e:
        print(f"Error deleting data: {str(e)}")


# Function to perform an action based on user role
def perform_action_based_on_role(user):
    # Perform actions for each user
    for _, user_data in users_data.iterrows():
        user = User(user_ID=user_data['User_ID'], user_role=user_data['User_Role'])
        if user.user_role == 'Admin':
           upload_data_from_external_source(user.user_id, user.user_role, file_content)
           handle_submissions(user.user_id,user.user_role)
           manage_shared_data(user.user_id,user.user_role)
           manage_permissions(user.user_id,user.user_role)
           manage_payments(user.user_id,user.user_role)
           view_usage_logs(user.user_id,user.user_role)
           delete_user_data(user.user_id,user.user_role)
        else:
            print("This action is not allowed for non-admin users.")


# Function to perform an action based on subscription type
def perform_action_based_on_subscription(user):
    if user.subscription_type == 'Individual':
        print("Individual subscription user can perform this action.") 
        # actions specific to Individual subscription
        action_choice = input("Enter the action you want to perform (e.g., 'view_data', 'upload_data'): ")
        if action_choice == 'view_data':
            view_data = f"SELECT * FROM SHARED_DATA WHERE User_ID = '{user.user_id}'"
            cursor.execute(view_data)
            View_data = cursor.fetchall()
            if View_data:
                print("View data details:")
                for share in View_data:
                    print(share)
                else:
                    print("No data records found.")
            print("Viewing data for Individual subscription user.")

            user_data = fetch_voter_data(user.user_id)
            if user_data:
               print("User data:")
               for key, value in user_data.items():
                   print(f"{key}: {value}")
            else:
                print("No data available for the user.")
        elif action_choice == 'upload_data':
            upload_data_from_external_source(user.user_id, user.user_role, file_content)
            print("Uploading data for Individual subscription user.")
        else:
            print(f"User with ID {user.user_id} does not have permission to upload data.")
    else:
        print("This action can be performed only by admin.")


def perform_action_based_on_subscription_status(user):
    cursor.execute(check_permission_query)
    if user.subscription_status == 'Active':
        print("User has an active subscription.")
        # Add logic for actions specific to an active subscription
        action_choice = input("Enter the action you want to perform ('view_data','upload_data'): ")
        if action_choice == 'view_data':
            view_data = f"SELECT * FROM SHARED_DATA WHERE User_ID = '{user.user_id}'"
            data_to_view = input("Enter the Data ID to view: ")
            cursor.execute(data_to_view)
            View_data = cursor.fetchall()
            if View_data:
                print("View data details:")
                for share in View_data:
                    print(share)
                else:            
                    print("No data records found.")
            print("Viewing data for a user with an active subscription.")
        elif action_choice == 'upload_data':
            upload_data_from_external_source(user.user_id, user.user_role, file_content)
            print("Uploading data for a user with an active subscription.")
        else:
            print(f"User with ID {user.user_id} does not have permission to upload data.")

    elif user.subscription_status == 'Pending':
        if action_choice == 'view_data':
            cursor.execute(view_data)
            View_data = cursor.fetchall()
            print("User has a pending subscription. Cannot perform actions until the subscription is active.")
        else:
            print("Invalid action choice.")

    elif user.subscription_status == 'Cancelled':
        if action_choice == 'view_data':
            cursor.execute(view_data)
            View_data = cursor.fetchall()
            print("User's subscription is cancelled. Actions are not allowed.")
        else:
            print("Invalid action choice.")
       
    elif user.subscription_status == 'Expired':
        if action_choice == 'view_data':
            cursor.execute(view_data)
            View_data = cursor.fetchall()
            print("User's subscription has expired. Actions are not allowed.")
    else:
        print("This action can be performed only by admin.")


if __name__ == "__main__":
    # Fetch voter data
    voters_data = fetch_voter_data(connection)

    # Perform actions for each user (admin, candidate, party worker)
for user_data in users_data:
    user = User(user_ID=user_data['User_ID'], 
                user_role=user_data['User_Role'], 
                subscription_type='Individual', 
                subscription_status='Active')
    
    # Check if the user has a valid role
    if user.user_role in ('Admin', 'Candidate', 'Party_worker'):
        # Perform actions based on user roles, subscription types, and subscription status
        check_permission_query(user.user_id, user.user_role)
        upload_data_from_external_source(user.user_id, user.user_role,file_content)
        handle_submissions(user.user_id, user.user_role)
        manage_shared_data(user.user_id, user.user_role)
        manage_permissions(user.user_id, user.user_role)
        view_usage_logs(user.user_id, user.user_role)
        manage_payments(user.user_id, user.user_role)
        delete_user_data(user.user_id, user.user_role)
        perform_action_based_on_role(user)
        perform_action_based_on_subscription(user)
        perform_action_based_on_subscription_status(user)
    else:
        print(f"Skipping actions for user {user.user_id} with role {user.user_role}")
   
    close_connection(connection)
