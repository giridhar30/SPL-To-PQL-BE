import pandas as pd
import re

def replace_or_remove_macros(query, csv_file):
    # Load the CSV file
    macros_df = pd.read_csv(csv_file)

    # Extract macros from the query
    macros_in_query = re.findall(r'`([^`]*)`', query)

    # Replace or remove each macro in the query based on its definition from the CSV file
    for macro in macros_in_query:
        if macro in macros_df['Name'].values:
            definition = macros_df[macros_df['Name'] == macro]['Definition'].values[0]
            if definition.strip() == 'search *':
                # Remove the macro if the definition is 'search *'
                query = query.replace(f'`{macro}`', '')
            else:
                # Replace the macro with its definition
                query = query.replace(f'`{macro}`', definition)

    # Remove trailing pipe if present
    query = query.rstrip(' |')

    return query

# Your query with macros
query = "`cloudtrail` eventName = PutBucketReplication eventSource = s3.amazonaws.com | rename requestParameters.* as * | stats count values(bucketName) as source_bucket values(ReplicationConfiguration.Rule.ID) as rule_id values(ReplicationConfiguration.Rule.Destination.Bucket) as destination_bucket by _time user_arn userName user_type src_ip aws_account_id userIdentity.principalId user_agent | `aws_exfiltration_via_ec2_snapshot_filter`"

# Replace macros in the query or remove them if the definition is 'search *'
updated_query = replace_or_remove_macros(query, "SQL.csv")
print(updated_query)
