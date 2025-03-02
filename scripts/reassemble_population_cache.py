import os

def reassemble_population_cache():
    parts = [f for f in os.listdir() if f.startswith('population_cache_part_')]
    parts.sort()
    with open('population_cache.pkl', 'wb') as output_file:
        for part in parts:
            with open(part, 'rb') as input_file:
                output_file.write(input_file.read())
    print('Reassembled population_cache.pkl')

if __name__ == '__main__':
    reassemble_population_cache()
