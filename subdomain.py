import dns.resolver
import pyfiglet

class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

text = pyfiglet.figlet_format("SubDomain Finder" )
print(Color.YELLOW,text)
def find_subdomains(domain, wordlist_file):
    subdomains = []

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
                # NoAnswer means the query was valid but there was no answerS
                pass
            except dns.exception.Timeout:
                # Timeout means the query timed out
                pass
            except dns.resolver.NoNameservers:
                # NoNameservers means there were no nameservers to answer the query
                pass

    return subdomains

# Example usage
try:
    domain = input("Enter Domain Name : ")
    wordlist_file = "subdomain.txt"
    subdomains = find_subdomains(domain, wordlist_file)
    print(f"Discovered subdomains for {domain}: {subdomains}")
except KeyboardInterrupt:
    print(Color.BLUE,"Thank You For Using")
