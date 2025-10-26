document.addEventListener('DOMContentLoaded', () => {
    const productItems = document.querySelectorAll('.product-item');
    const modal = document.getElementById('imageGalleryModal');
    const modalImg = document.getElementById('galleryImage');
    const closeBtn = modal.querySelector('.close-lightbox');
    const prevBtn = modal.querySelector('.prev-lightbox');
    const nextBtn = modal.querySelector('.next-lightbox');

    // Ensure modal is hidden on initial load
    if (modal) {
        modal.style.display = 'none';
    }

    let currentImages = [];
    let currentIndex = 0;

    // Function to update the modal image
    function showImage(index) {
        if (currentImages.length > 0) {
            currentIndex = (index + currentImages.length) % currentImages.length; // Handle wrap around
            modalImg.src = currentImages[currentIndex];
        }
    }

    // Add click listener to each product item
    productItems.forEach(item => {
        item.addEventListener('click', () => {
            const folderName = item.dataset.folder;
            if (!folderName) {
                console.error('Data-folder attribute missing on product item');
                return;
            }

            // Hide buttons initially before fetch
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';

            // Fetch images for the clicked folder
            fetch(`/get_images/${folderName}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(imageUrls => {
                    if (imageUrls.error) {
                         console.error('Error fetching images:', imageUrls.error);
                         currentImages = []; // Clear images if folder not found or error
                         modalImg.src = ""; // Clear image source
                         modalImg.alt = "Error loading images.";
                         prevBtn.style.display = 'none'; // Hide buttons on error
                         nextBtn.style.display = 'none';
                         modal.style.display = 'flex'; // Still show modal to indicate error?
                    } else if (imageUrls.length > 0) {
                        currentImages = imageUrls;
                        showImage(0); // Show the first image
                        modal.style.display = 'flex'; // Display the modal

                        // Show/hide buttons based on image count
                        if (currentImages.length > 1) {
                            prevBtn.style.display = 'block';
                            nextBtn.style.display = 'block';
                        } else {
                            prevBtn.style.display = 'none';
                            nextBtn.style.display = 'none';
                        }
                    } else {
                        // Handle case where folder exists but is empty
                        currentImages = [];
                        console.log('No images found in folder:', folderName);
                        modalImg.src = ""; // Clear image source
                        modalImg.alt = "No additional images available.";
                        prevBtn.style.display = 'none'; // Hide buttons if no images
                        nextBtn.style.display = 'none';
                        modal.style.display = 'flex'; // Show modal to indicate no images
                    }
                })
                .catch(error => {
                    console.error('Error fetching images:', error);
                    currentImages = [];
                    modalImg.src = "";
                    modalImg.alt = "Error fetching images.";
                    prevBtn.style.display = 'none'; // Hide buttons on fetch error
                    nextBtn.style.display = 'none';
                    modal.style.display = 'flex'; // Show modal to indicate error
                });
        });
    });

    // Close modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        currentImages = []; // Clear images when closing
        prevBtn.style.display = 'none'; // Hide buttons on close
        nextBtn.style.display = 'none';
    });

    // Previous image
    prevBtn.addEventListener('click', () => {
        showImage(currentIndex - 1);
    });

    // Next image
    nextBtn.addEventListener('click', () => {
        showImage(currentIndex + 1);
    });

    // Close modal if clicking outside the image content
    modal.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
            currentImages = [];
            prevBtn.style.display = 'none'; // Hide buttons on close
            nextBtn.style.display = 'none';
        }
    });

    // Optional: Keyboard navigation
    document.addEventListener('keydown', (event) => {
        if (modal.style.display === 'flex') {
            if (event.key === 'ArrowLeft' && currentImages.length > 1) { // Only navigate if multiple images
                showImage(currentIndex - 1);
            }
            else if (event.key === 'ArrowRight' && currentImages.length > 1) { // Only navigate if multiple images
                showImage(currentIndex + 1);
            }
            else if (event.key === 'Escape') {
                modal.style.display = 'none';
                currentImages = [];
                prevBtn.style.display = 'none'; // Hide buttons on close
                nextBtn.style.display = 'none';
            }
        }
    });
});
