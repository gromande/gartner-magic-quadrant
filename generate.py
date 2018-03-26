from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def get_vendors(url):
    capability_page = urlopen(url)
    soup = BeautifulSoup(capability_page, 'html.parser')
    table_of_contents = soup.find('ul', {"class": "noindt"})
    for item in table_of_contents.find_all('li'):
        item_text = item.text.strip()
        if item_text.startswith("Vendor Strengths and Cautions") or item_text.startswith("Vendors\n"):
            list_of_vendors = item.ul.find_all('li')
            vendors = []
            for item in list_of_vendors:
                vendors.append(item.string.strip())
            return vendors
    return []

whitelist = [
    "Access Management"
    "Application Security Testing",
    "Cloud Access Security Brokers",
    "Endpoint Protection Platforms",
    "Enterprise Data Loss Prevention",
    "Enterprise Network Firewalls",
    "Enterprise Asset Management Software",
    "High-Security Mobility Management",
    "Identity Governance and Administration",
    "Intrusion Detection and Prevention Systems",
    "Secure Web Gateways",
    "Security Awareness Computer-Based Training",
    "Security Information and Event Management",
    "Software Asset Management Tools",
    "Unified Threat Management",
    "Web Application Firewalls",
    "Wired and Wireless LAN Access Infrastructure",
]

ROOT = 'https://www.gartner.com'
#print(get_vendors(ROOT + "/doc/3551917"))
#quit()
page = urlopen(ROOT + '/technology/research/methodologies/magicQuadrants.jsp')
soup = BeautifulSoup(page, 'html.parser')
links = [link for link in soup.find_all('a') if link.get('href').startswith('/doc/code/')]
capabilities = {}

for link in links:
    capability_name = link.string
    #if capability_name not in whitelist:
    #    continue
    url = ROOT + link.get('href')
    capability = {"url": url}
    capability["vendors"] = get_vendors(url)
    capabilities[link.string] = capability

print(json.dumps(capabilities))
