// Retrieve CSRF token from the HTML document
const csrfToken = getCookie('csrftoken')

// retrieve data from flight search
document.addEventListener('DOMContentLoaded', () => {
    // add event listener to the search button
    document.getElementById('search_button').addEventListener('click', () => { 
        // get form data from flights.html
        const origin = document.getElementById('origin').value;
        const destination = document.getElementById('destination').value;
        const departureDate = document.getElementById('departure_date').value;
        
        console.log(`${origin} ${destination} ${departureDate}`);

        // get form data from backend using AJAX request
        fetch(`/flights?origin=${origin}&destination=${destination}&departure_date=${departureDate}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrfToken
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayFlightData(data.context) // call function to display flights
        });
    });
});

// function to display flight data in HTML
function displayFlightData(flights) {
    const flightContainer = document.getElementById('flight_list');
    flightContainer.innerHTML = ''; // clear previous flight data

    if (flights.length == 0) {
        flightContainer.innerHTML = `
        <h5 class="card-title">No Flights Available</h5>
        `;
    } else {
    // for each flight in flights a separate flight card
        flights.forEach(flight => {
            // create flight card
            const flightCard = document.createElement('div');
            flightCard.classList.add('flight-card');

            // populate flight card with data
            flightCard.innerHTML = `
            <form action="/flights" method="POST" onsubmit="return confirm('Are you sure you want to make this booking?');">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"> 
                <div class="card-body">
                    <h5 class="card-title">Origin: ${flight.origin}</h5>
                    <p class="card-text">Destination: ${flight.destination}</p>
                    <p class="card-text">Departure Time: ${flight.departure_time}</p>
                    <p class="card-text">Arrival Time: ${flight.arrival_time}</p>
                    <p class="card-text">Seats Available: ${flight.seats}</p>
                    <p class="card-text">Price: $${flight.price}</p>
                    <input type="hidden" name="origin" value="${flight.origin}">
                    <input type="hidden" name="destination" value="${flight.destination}">
                    <input type="hidden" name="departure_time" value="${flight.departure_time}">
                    <input type="hidden" name="arrival_time" value="${flight.arrival_time}">
                    <input type="hidden" name="price" value="${flight.price}">
                    <input type="hidden" name="unique_code" value="${flight.unique_code}">
                    <input type="submit" class="btn btn-primary" value="Book">
                </div>
            </form>
        `;

            // append flight card to container
            flightContainer.appendChild(flightCard);
        });
    }
}

// Function to get CSRF token from cookies
function getCookie(name) {
    // initialize variable to null
    let cookieValue = null;
    // check if there are cookies present in the document and it is not an emptu stiring
    if (document.cookie && document.cookie !== '') {
        // split the document.cookie strign into an array of individual cookies
        const cookies = document.cookie.split(';');
        // iterate through substrings (cookie)
        for (let i = 0; i < cookies.length; i++) {
            // trim any whitespace from the cookie string
            const cookie = cookies[i].trim();
            // check if cookie string start with name we are after followed by '='
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // extract te value of the cookie (after the '=' character)
                // decode it from URI component encoding
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // return the value of the cookie or null if not found
    return cookieValue;
}

// function to rdirect user to home page
function redirectToHomePage() {
    window.location.href = "/";
}

// function to hide error messages after 5 seconds
setTimeout(() => {
    var errorMessages = document.getElementById('error-messages');
    if (errorMessages) {
        errorMessages.style.display = 'none';
    }
}, 5000); // 5 second timeout