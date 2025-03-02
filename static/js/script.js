document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('routeForm');
    const calculateBtn = document.getElementById('calculateBtn');
    const spinner = calculateBtn.querySelector('.spinner-border');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const mapForm = document.getElementById('mapForm');

    let konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // Up, Up, Down, Down, Left, Right, Left, Right, B, A
    let keyPresses = []; 
    document.addEventListener('keydown', function(e) {
      keyPresses.push(e.keyCode);
      if (keyPresses.slice(-konamiCode.length).join('') === konamiCode.join('')) {
          window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
        keyPresses = []; // Reset the sequence
      }
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Form validation
        if (!form.checkValidity()) {
            e.stopPropagation();
            form.classList.add('was-validated');
            return;
        }

        // Show loading state
        calculateBtn.disabled = true;
        spinner.classList.remove('d-none');
        resultsDiv.classList.add('d-none');
        errorDiv.classList.add('d-none');

        try {
            const formData = new FormData(form);
            const response = await fetch('/calculate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }
            
            // Update results
            document.getElementById('roadDistance').textContent = `${data.road_distance} Km`;
            document.getElementById('railDistance').textContent = `${data.railway_metrics.rail_distance} Km`;
            document.getElementById('estimatedCost').textContent = `$${data.railway_metrics.estimated_cost.toLocaleString("en-US")}`;
            document.getElementById('co2Savings').textContent = `${data.railway_metrics.co2_savings} Kg`;

            resultsDiv.classList.remove('d-none');
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('d-none');
        } finally {
            // Reset loading state
            calculateBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    });

    mapForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const populationRadius = document.getElementById('populationRadius').value;
        const ticketPrice = document.getElementById('ticketPrice').value;
        const maxSpeed = document.getElementById('maxSpeed').value;

        // Handle the slider values as needed
        console.log(`Population Radius: ${populationRadius} km`);
        console.log(`Ticket Price: $${ticketPrice}`);
        console.log(`Max Speed: ${maxSpeed} km/h`);
    });
});

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}


