import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

from dotenv import load_dotenv
load_dotenv()


def process_csv(csv_file: str, output_dir: str, bucket_name: str, s3_key: str) -> None:
    """
    Process a CSV file, convert it to Parquet format, and upload it to S3.

    Args:
        csv_file (str): Path to the input CSV file.
        output_dir (str): Directory to save the Parquet file.
        bucket_name (str): S3 bucket name.
        s3_key (str): S3 key for the uploaded Parquet file.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Creating it.")
    os.makedirs(output_dir, exist_ok=True)

    # Accessing path of system
    csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "international_education_costs.csv"))

    if not csv_file.endswith(".csv"):
        raise ValueError(f"O caminho {csv_file} não parece ser um arquivo CSV.")


    # Ensure AWS credentials are set in the environment or use a profile
    # boto3.setup_default_session(profile_name='your_profile_name')
    # or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the environment
    # boto3.setup_default_session(aws_access_key_id='your_access_key', aws_secret_access_key='your_secret_key')
    # Initialize S3 client
    session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION_NAME")
)
    
    # Check if the bucket exists
    try:
        s3_client = boto3.client("s3")
        s3_client.head_bucket(Bucket=bucket_name)
    except Exception as e:
        raise ValueError(f"Bucket {bucket_name} does not exist or is not accessible: {e}")
    
    # Check if the S3 key is valid
    if not s3_key.endswith(".parquet"):
        raise ValueError(f"O caminho {s3_key} não parece ser um arquivo Parquet.")
    
    # Turn on S3 client
    s3_client = session.client('s3')

    # Read the CSV file
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file {csv_file} does not exist.")
    print(f"Reading CSV file {csv_file}")
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert the DataFrame to JSON format
    json_file = os.path.join(output_dir, "internacional_education_costs.json")
    # Save the DataFrame to JSON format
    df.to_json(json_file, orient='records', lines=True)
    parquet_file = os.path.join(output_dir, "internacional_education_costs.parquet")

    # Convert DataFrame to Parquet format
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file)

    # Upload the Parquet file to S3
    s3_client.upload_file(parquet_file, bucket_name, s3_key)

if __name__ == "__main__":

    pass
