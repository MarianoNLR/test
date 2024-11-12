document.addEventListener('DOMContentLoaded', () => {
    const carousels = [
        { id: 'carousel-masajes' },
        { id: 'carousel-belleza' },
        { id: 'carousel-faciales' },
        { id: 'carousel-corporales' },
    ];

    carousels.forEach(({ id }) => {
        const carousel = document.getElementById(id);
        const slides = carousel.querySelectorAll('.slide');
        let currentSlide = 0;

        const showSlide = (index) => {
            slides.forEach((slide, i) => {
                slide.classList.toggle('active', i === index);
            });
        };

        const nextSlide = () => {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        };

        const prevSlide = () => {
            currentSlide = (currentSlide - 1 + slides.length) % slides.length;
            showSlide(currentSlide);
        };

        // Inicializa el primer slide como activo
        showSlide(currentSlide);

        // Agrega eventos de clic a los botones de navegación específicos de cada carrusel
        carousel.querySelector('.next').addEventListener('click', nextSlide);
        carousel.querySelector('.prev').addEventListener('click', prevSlide);
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.carousel .slide');
    let currentSlide = 0;

    const showSlide = (index) => {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    };

    const nextSlide = () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    };

    const prevSlide = () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    };

    // Inicializa el primer slide como activo
    showSlide(currentSlide);

    // Cambia de slide cada 5 segundos
    setInterval(nextSlide, 5000);

    // Asocia los botones de navegación a las funciones
    document.querySelector('.carousel-controls .next').addEventListener('click', nextSlide);
    document.querySelector('.carousel-controls .prev').addEventListener('click', prevSlide);
});

