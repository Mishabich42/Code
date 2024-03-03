import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Set up the Gmail API credentials
credentials = Credentials.from_authorized_user_file('path_to_credentials.json')
service = build('gmail', 'v1', credentials=credentials)


def delete_emails_by_label(label_id, batch_size=100):
    # Retrieve emails with the specified label
    results = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found with the specified label.")
        return

    # Delete emails in batches
    total_deleted = 0
    while messages:
        batch = service.new_batch_http_request()

        for message in messages[:batch_size]:
            batch.add(service.users().messages().delete(userId='me', id=message['id']))

        batch.execute()

        total_deleted += len(messages[:batch_size])
        messages = messages[batch_size:]

        print(f"Deleted {total_deleted} emails.")

    print("All emails have been deleted.")


def delete_emails_by_criteria(criteria):
    # Build the Gmail search query based on the provided criteria
    query = ""
    if 'label' in criteria:
        query += f"label:{criteria['label']} "
    if 'from_email' in criteria:
        query += f"from:{criteria['from_email']} "
    if 'after' in criteria:
        query += f"after:{criteria['after']} "
    if 'before' in criteria:
        query += f"before:{criteria['before']} "

    # Retrieve emails based on the search query
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No emails found with the specified criteria.")
        return

    # Delete emails
    for message in messages:
        service.users().messages().delete(userId='me', id=message['id']).execute()

    print(f"{len(messages)} emails have been deleted.")


# Example usage to delete emails with the 'forums' label in batches of 100
delete_emails_by_label('forums', batch_size=100)

# Example usage to delete emails based on criteria
delete_emails_by_criteria({
    'label': 'forums',
    'from_email': 'example@gmail.com',
    'after': '2023/03/10',
    'before': '2023/04/22'
})
