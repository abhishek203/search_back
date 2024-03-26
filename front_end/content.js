// content.js
let isBlockingEnabled = true; // Assume we start with blocking enabled.

function handlePaste(e) {
  if (isBlockingEnabled) {
    // Get the pasted text
    const pastedText = e.clipboardData.getData('text');
    
    e.preventDefault();

    // Get the target element and its current value
    const target = e.target;
    const originalText = target.value;
    
    // Calculate the cursor's current position
    const cursorPosition = target.selectionStart;

    if (e.target && e.target.value !== undefined) {
      e.target.value = originalText;
    }

    // Combine the original text and the pasted text at the cursor position
    const beforeText = originalText.substring(0, cursorPosition);
    const afterText = originalText.substring(cursorPosition, originalText.length);
    const combinedText = beforeText + pastedText + afterText;

    // Prepare the data as URL-encoded string
    const encodedData = new URLSearchParams();
    encodedData.append('message', pastedText);
    const baseURL = "http://127.0.0.1:8000/inference";

    // Define your parameters
    const params = {
        query: encodedData
          };

    // Function to convert object to query string
    const queryString = Object.keys(params)
        .map(key => key + '=' + encodeURIComponent(params[key]))
        .join('&');

    // Append parameters to the base URL
    const urlWithParams = `${baseURL}?${queryString}`;

    // API call with x-www-form-urlencoded data
    fetch(urlWithParams, {
      method: 'GET',
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data['response'] === true) {
        alert('Pasting confidential text is not allowed on this website.');
      } else {
        e.target.value = combinedText;

        target.selectionStart = target.selectionEnd = cursorPosition + pastedText.length;
        
        e.target.style.height = "";
        e.target.style.height = e.target.scrollHeight + "px";
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  }
}


function toggleMediaUploads(enable) {
  const mediaUploadInputs = document.querySelectorAll('input[type="file"]');
  mediaUploadInputs.forEach(input => {
    input.disabled = !enable; // Disable or enable based on the passed parameter.
  });
}

// Attach the paste event listener to the document.
document.addEventListener('paste', handlePaste, true);

// Disable media uploads initially.
toggleMediaUploads(false);

// Use a MutationObserver to detect and react to changes in the DOM.
function observeDOMChanges() {
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Re-apply the media upload restrictions for newly added nodes.
        toggleMediaUploads(!isBlockingEnabled);
      }
    });
  });

  // Observe changes in the entire body of the document.
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}

// Start observing DOM changes for dynamically added content.
observeDOMChanges();

// Listen for messages from the popup to toggle functionality.
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    isBlockingEnabled = request.block;
    // Update both paste blocking and media upload restrictions based on the message.
    toggleMediaUploads(!isBlockingEnabled);
  }
);
