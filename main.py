import requests
from bs4 import BeautifulSoup

while True:
  # Take user input for movie name search
  query = input("Enter movie name: ")

  # Send query to the provided URL
  url = f"https://on.akwam.cx/search?q={query}"
  response = requests.get(url)

  # Parse the resulting page with BeautifulSoup
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find all the div elements with the class 'entry-box entry-box-1'
  entry_boxes = soup.find_all('div', {'class': 'entry-box entry-box-1'})

  # Create a list of dictionaries to store the title, quality, and URL for each movie
  movies = []
  index = 1
  for entry_box in entry_boxes:
    title = entry_box.find('h3', {'class': 'entry-title font-size-14 m-0'}).text
    quality_tag = entry_box.find('span', {'class': 'label quality'})
    rating_span = entry_box.find('span', class_='label rating')
    if quality_tag:
      quality = quality_tag.text
      rating = rating_span.text
      url_tag = entry_box.find('a', {'class': 'text-white'})
      url = url_tag['href']
      movies.append({'index': index, 'title': title, 'quality': quality, 'url': url, 'rating': rating})
      index += 1

  # Print the search results as a numbered list
  for movie in movies:
    print(f"{movie['index']}. {movie['title']} ({movie['quality']}) IMDP Score: {movie['rating']}")

  # Take user input for movie selection
  selection = int(input("Enter movie number: "))

  # Get the selected movie from the list
  selected_movie = movies[selection-1]

  # Send a request to the selected movie's URL
  response = requests.get(selected_movie['url'])
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find all the available quality options
  quality_options = soup.find_all('li')

  # Print out the available quality options
  print(f"The available quality options for {selected_movie['title']}:")
  for i, option in enumerate(quality_options):
    print(f"{i + 1}. {option.text}")

  # Ask the user to enter the number of the selected quality
  selected_quality = int(input("Enter the number of the selected quality: "))

  # Find the tab content element for the selected quality
  tab_id = f"tab-{selected_quality}"
  tab_content = soup.find('div', {'id': tab_id})

  # Find the URL of the selected quality
  quality_div = tab_content.find('div', {'class': 'qualities'})
  link_show = quality_div.find('a', {'class': 'link-show'})
  selected_quality_url = link_show['href']

  # Send a request to the selected movie's URL
  response = requests.get(selected_quality_url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find the `a` element with the `download-link` class
  link_element = soup.find('a', class_='download-link')

  # Extract the URL from the `href` attribute
  url = link_element['href']
  watchLink = url

  # Print the URL
  print(f"The stream link is: {watchLink}")

  # Make a GET request to the URL
  response = requests.get(watchLink)

  # Parse the HTML content of the page
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find all the source elements
  source_elements = soup.find_all('source')

  # Iterate over the source elements
  for source in source_elements:
    # Extract the download link and quality from the source element
    download_link = source['src']
    quality = source['size']

    # Print the download link and quality
    print(f'Quality: {quality} | Download Link: {download_link}')

  # Ask the user if they want to search again
  search_again = input("Do you want to search again (Y/N)? ")
  if search_again.lower() != 'y':
    break
