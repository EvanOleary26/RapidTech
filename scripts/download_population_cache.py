import boto3

def download_population_cache():
    s3 = boto3.client('s3')
    bucket_name = 'your-bucket-name'
    file_key = 'path/to/population_cache.pkl'
    download_path = 'population_cache.pkl'

    s3.download_file(bucket_name, file_key, download_path)
    print(f'Downloaded {file_key} to {download_path}')

if __name__ == '__main__':
    download_population_cache()
