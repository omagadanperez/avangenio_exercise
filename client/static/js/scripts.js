document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('clientForm');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');

    // Popup elements
    const popup = document.getElementById('popup');
    const popupMessage = document.getElementById('popup-message');
    const popupClose = document.getElementById('popup-close');
    const downloadLinks = document.getElementById('download-links');
    const downloadError = document.getElementById('download-error');

    const downloadChains = document.getElementById('download-chains');
    const downloadResponses = document.getElementById('download-responses');

    const numInput = document.getElementById('num_strings');
    const inputError = document.getElementById('input-error');


    const flashMessagesDiv = document.getElementById('flash-messages');
    let flashMessages = [];

    try {
        flashMessages = JSON.parse(flashMessagesDiv.getAttribute('data-messages'));
    } catch (e) {
        console.error("Failed to parse flash messages JSON:", e);
    }

    function showPopup(message, category) {
        popupMessage.textContent = message;
        popupMessage.style.color = category === 'success' ? '#2e7d32' : (category === 'error' ? '#d32f2f' : '#000');
        popup.classList.remove('hidden');

        if (category === 'success') {
            downloadLinks.classList.remove('hidden');
        } else {
            downloadLinks.classList.add('hidden');
        }

        downloadError.classList.add('hidden');
    }

    popupClose.addEventListener('click', () => {
        popup.classList.add('hidden');
    });

    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            popup.classList.add('hidden');
        }
    });

    if (flashMessages.length > 0) {
        const [category, message] = flashMessages[0];
        showPopup(message, category);
    }

    form.addEventListener('submit', (e) => {
        const value = parseInt(numInput.value);
        let errorMessage = '';

        if (!numInput.value) {
            errorMessage = 'This field is required.';
        } else if (isNaN(value) || value < 1) {
            errorMessage = 'The value must be greater than 0.';
        }
        // else if (value > 1000000) {
        //     errorMessage = 'The value must be less than or equal to 1,000,000.';
        // }

        if (errorMessage) {
            e.preventDefault();
            inputError.textContent = errorMessage;
            inputError.classList.remove('hidden');
            submitBtn.disabled = false;
            document.getElementById('spinner').classList.remove('visible');
        } else {
            inputError.classList.add('hidden');
            inputError.textContent = '';
            submitBtn.disabled = true;
            document.getElementById('spinner').classList.add('visible');
        }
    });

    function attemptDownload(button, fileUrl) {
        fetch(fileUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error("File not found.");
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = button.getAttribute('download');
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            })
            .catch(err => {
                downloadError.textContent = `Error: Could not download "${button.getAttribute('download')}"`;
                downloadError.classList.remove('hidden');
            });
    }

    downloadChains.addEventListener('click', (e) => {
        e.preventDefault();
        attemptDownload(downloadChains, '/download/chains.txt');
    });

    downloadResponses.addEventListener('click', (e) => {
        e.preventDefault();
        attemptDownload(downloadResponses, '/download/responses.txt');
    });
});
