import dns.resolver
import pyfiglet
import argparse
import signal
import sys

class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

text = pyfiglet.figlet_format("SubDomain Finder")
print(Color.YELLOW, text)

# Global variable to store subdomains
subdomains = []

def find_subdomains(domain, wordlist_file):
    global subdomains  # Ensure we use the global list to store subdomains
    # Open the wordlist file
    with open(wordlist_file, 'r') as file:
        # Iterate through each word in the wordlist
        for word in file:
            subdomain = f"{word.strip()}.{domain}"
            try:
                # Perform a DNS query
                answers = dns.resolver.resolve(subdomain, 'A')
                # If no exception is raised, the subdomain exists
                subdomains.append(subdomain)
                print(f"Found: {subdomain}")
            except dns.resolver.NXDOMAIN:
                # NXDOMAIN means the subdomain does not exist
                pass
            except dns.resolver.NoAnswer:
                # NoAnswer means the query was valid but there was no answer
                pass
            except dns.exception.Timeout:
                # Timeout means the query timed out
                pass
            except dns.resolver.NoNameservers:
                # NoNameservers means there were no nameservers to answer the query
                pass

def save_results(subdomains, output_file):
    # Ensure the output file is created, even if no subdomains are found
    with open(output_file, 'w') as file:
        if subdomains:
            for subdomain in subdomains:
                file.write(subdomain + '\n')
            print(f"Results saved to {output_file}")
        else:
            file.write("No subdomains found.\n")
            print(f"No subdomains found. A file has been created: {output_file}")

def handle_exit(signum, frame):
    print("\nScript interrupted or suspended. Saving results...")
    save_results(subdomains, output_file)
    sys.exit(0)

# Argument parsing
parser = argparse.ArgumentParser(description="Subdomain Finder Tool")
parser.add_argument("domain", help="The domain to find subdomains for.")
parser.add_argument("-o", "--output", default="found_subdomains.txt", help="File to save the results (default: found_subdomains.txt).")
parser.add_argument("-w", "--wordlist", default="subdomain.txt", help="Wordlist file (default: subdomain.txt).")
args = parser.parse_args()

# Set up signal handlers for interruption and suspension (Ctrl+C and Ctrl+Z)
signal.signal(signal.SIGINT, handle_exit)  # Ctrl+C (SIGINT)
signal.signal(signal.SIGTSTP, handle_exit)  # Ctrl+Z (SIGTSTP)

try:
    domain = args.domain
    wordlist_file = args.wordlist
    output_file = args.output

    # Start the subdomain discovery process
    find_subdomains(domain, wordlist_file)
    print(f"Discovered subdomains for {domain}: {subdomains}")

except KeyboardInterrupt:
    print(Color.BLUE, "Script interrupted. Saving results...")
    save_results(subdomains, output_file)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure results are saved when the script is completed or interrupted
    save_results(subdomains, output_file)
