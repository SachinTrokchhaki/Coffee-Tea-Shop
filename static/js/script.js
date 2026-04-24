// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    
    // Get elements
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('overlay');
    
    // Function to open menu
    function openMenu() {
        if (mobileMenu) {
            mobileMenu.classList.add('active');
        }
        if (overlay) {
            overlay.classList.add('active');
        }
        document.body.style.overflow = 'hidden';
    }
    
    // Function to close menu
    function closeMenu() {
        if (mobileMenu) {
            mobileMenu.classList.remove('active');
        }
        if (overlay) {
            overlay.classList.remove('active');
        }
        document.body.style.overflow = '';
    }
    
    // Event listeners
    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', openMenu);
    }
    
    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', closeMenu);
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }
    
    // Close menu when clicking on a link
    const mobileLinks = document.querySelectorAll('.mobile-menu-links a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });
    
    // View Products button
    const viewProductsBtn = document.querySelector('.primary-btn');
    if (viewProductsBtn) {
        viewProductsBtn.addEventListener('click', function() {
            const menuSection = document.querySelector('.menu');
            if (menuSection) {
                menuSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // Learn More button
    const learnMoreBtn = document.querySelector('.secondary-btn');
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', function() {
            const aboutSection = document.querySelector('.about-section');
            if (aboutSection) {
                aboutSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input').value;
            if (email) {
                alert(`Thanks for subscribing! 📧\nWe'll send updates to: ${email}`);
                this.reset();
            }
        });
    }
    
    console.log('Coffee & Tea Shop Website Loaded! ☕');
});

// Profile Dropdown Toggle
function toggleDropdown(event) {
  event.preventDefault();
  event.stopPropagation();
  
  const menu = document.getElementById('dropdownMenu');
  const toggle = document.getElementById('userDropdown');
  
  if (menu) {
    menu.classList.toggle('show');
    if (toggle) toggle.classList.toggle('active');
  }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
  const dropdown = document.querySelector('.dropdown');
  const menu = document.getElementById('dropdownMenu');
  const toggle = document.getElementById('userDropdown');
  
  if (dropdown && menu && !dropdown.contains(event.target)) {
    menu.classList.remove('show');
    if (toggle) toggle.classList.remove('active');
  }
});