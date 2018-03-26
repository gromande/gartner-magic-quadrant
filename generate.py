from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def get_vendors(url):
    try:
        capability_page = urlopen(url)
        soup = BeautifulSoup(capability_page, 'html.parser')
        table_of_contents = soup.find('ul', {"class": "noindt"})
        if "Magic Quadrant" in table_of_contents.find_all('li')[1].text:
            return []
        list_of_vendors = table_of_contents.find_all('li')[1].ul.find_all('li')[1].ul.find_all('li')
        vendors = []
        for item in list_of_vendors:
            vendors.append(item.string.strip())
        return vendors
    except:
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
#print(get_vendors(ROOT + "/doc/3527219"))
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
