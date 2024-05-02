

// Function to load content into the main content area inside the user dashboard page
function loadContent(element) {
    var url = element.getAttribute('data-url'); // Get URL stored in data-url attribute
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('main-content').innerHTML = xhr.responseText; // Update the main content area with the response
        }
    };
    xhr.send();
}