// Lightbox functionality for product images
document.addEventListener('DOMContentLoaded', function() {
    // Get all product images
    const productImages = document.querySelectorAll('.product-image');
    const lightbox = document.getElementById('imageModal');
    const expandedImg = document.getElementById('expandedImg');
    const closeButton = document.querySelector('.close-lightbox');
    
    // Add tooltip to each product image
    productImages.forEach(image => {
        image.title = "Кликнете, за да видите пълно изображение"; // Bulgarian tooltip: "Click to view full image"
    });

    // Add click event to each product image
    productImages.forEach(image => {
        image.addEventListener('click', function() {
            expandedImg.src = this.src;
            expandedImg.alt = this.alt;
            lightbox.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent scrolling when lightbox is open
        });
    });

    // Close lightbox when clicking the close button
    closeButton.addEventListener('click', function() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    });

    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', function(event) {
        if (event.target === lightbox) {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Close lightbox when pressing ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && lightbox.style.display === 'flex') {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
});
