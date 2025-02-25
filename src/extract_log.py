import sys
import os
import time
import gzip
import concurrent.futures

def process_chunk(chunk, target_date, output_file):
    """Processes a chunk and writes matching lines to output."""
    lines_to_write = [line for line in chunk if line.startswith(target_date)]
    with open(output_file, "a", encoding="utf-8") as outfile:
        outfile.writelines(lines_to_write)

def extract_logs(log_file, target_date, output_dir="output", buffer_size=1024*1024, num_threads=8):
    """Extract logs for a given date using buffered reading and multi-threading."""
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"output_{target_date}.txt")
    
    # Ensure output file is empty before writing
    open(output_file, "w").close()

    start_time = time.time()

    with open(log_file, "r", encoding="utf-8") as infile:
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            while True:
                lines = infile.readlines(buffer_size)  # Read in 1MB chunks
                if not lines:
                    break
                executor.submit(process_chunk, lines, target_date, output_file)

    end_time = time.time()
    print(f"Logs for {target_date} saved in {output_file}")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_logs.py <log_file> <YYYY-MM-DD>")
        sys.exit(1)

    log_file = sys.argv[1]
    target_date = sys.argv[2]

    extract_logs(log_file, target_date)
