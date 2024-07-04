import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import argparse

def main():
  parser = argparse.ArgumentParser(description="Scrape top words from URL")
  parser.add_argument('--domaininput', type=str, default="https://example.com", help='Domain to scrape')
  parser.add_argument('--NoOfWords', type=int, default="30", help='Amount of Words')
  args = parser.parse_args()

  if (str(args.domaininput).startswith('https://')) == False:
      domain = "https://" + args.domaininput
  else:
      domain = args.domaininput
  most_frequent_words = scrape_and_count_words(domain, args.NoOfWords)
  print('\n'.join('{}: {}'.format(*k) for k in enumerate(most_frequent_words)))

def scrape_and_count_words(url, num_words):
#Spoof user Agent to beat WAFs!
    request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    # Fetch the webpage content
    response = requests.get(url, headers=request_headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return
 
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
 
    # Extract text from paragraphs and other relevant tags
    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    # Clean and split the text into words
    words = (re.findall(r'\b\w+\b', text.lower())) #alphanumeric
    words = filter(lambda item: len(item) > 4, words) #Can't use less than length of 4 for banned password list
    whitelist = {'their','right','through','customers','your','with'}
    words = filter(lambda item: item not in whitelist, words) #allow words to be removed
 
    # Count the frequency of each word
    word_counts = Counter(words)
    common_words = word_counts.most_common(num_words)
    print("list of top " + str(num_words) + " words from " + str(url))
  
    return common_words


if __name__ == "__main__":
    main()
