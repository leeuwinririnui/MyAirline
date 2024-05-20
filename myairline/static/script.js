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

    // for each flight in flights a separate flight card
    flights.forEach(flight => {
        // create flight card
        const flightCard = document.createElement('div');
        flightCard.classList.add('flight-card');

        // populate flight card with data
        flightCard.innerHTML = `
            <p>Origin: ${flight.origin}</p>
            <p>Destination: ${flight.destination}</p>
            <p>Departure Time: ${flight.departure_time}</p>
            <p>Arrival Time: ${flight.arrival_time}</p>
            <p>Price: $${flight.price}</p>
            <button class="book-flight-button">Book</button>
        `;

        // append flight card to container
        flightContainer.appendChild(flightCard);
    });
}