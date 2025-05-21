from pipeline.csv_to_parquet import process_csv

def main():
    # Define the input CSV file, output directory, S3 bucket name, and S3 key
    csv_file = "./data/international_education_costs.csv"
    output_dir = "output"
    bucket_name = "sql-athena-parquet-3"
    s3_key = "parquet_files/internacional_education_costs.parquet"

    # Process the CSV file and upload to S3
    process_csv(csv_file, output_dir, bucket_name, s3_key)

if __name__ == "__main__":
    main()