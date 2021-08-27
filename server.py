from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 'keyword': keyword, 'postalCode': postalcode,
                'radius': radius, 'unit': unit, 'sort': sort}

    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    res = requests.get(url, params=payload)
    
    data = res.json()
    # print(20 * "*")
    # print(data.keys())
    # print(data['page'])
    # print(data['_links'])
    # print(20 * "*")


    events = data["_embedded"]["events"]

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    print(f"id is {id}")
    
    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    print(f"url is {url}")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    payload = {"apikey" : API_KEY} #"id" : id}

    res = requests.get(url, params=payload)

    data = res.json()
    print(20 * "*")
    # print(f"data is {data} ")
    print(data.keys())
    # print(data['images'])
    # print(data['_links'])

    event_name = data["name"]
    print(event_name)

    event_image_url = data["images"][0]["url"]
    print(event_image_url)
    print(20 * "*")
    event_tickmaster_url = data["url"]
    event_start_date = data["dates"]["start"]["localDate"]
    print(event_start_date)
    print(20 * "*")
    
    # Get Venue API 
    event_venues = []

    data_event_venue = data["_links"]["venues"]

    for event in data_event_venue:
        event_url_id = event["href"]
        venue_url = f"https://app.ticketmaster.com/{event_url_id}"
        venue_res = requests.get(venue_url, params=payload)
        venue_data = venue_res.json()
        event_venue = venue_data["name"]
        event_venues.append(event_venue)

    # classifications =


    return render_template('event-details.html',
                            event_name = event_name,
                            event_image_url = event_image_url,
                            event_tickmaster_url = event_tickmaster_url,
                            event_start_date = event_start_date,
                            event_venue = event_venues)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
