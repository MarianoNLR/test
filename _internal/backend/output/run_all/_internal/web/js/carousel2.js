document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.carousel .slide');
    const prevButton = document.querySelector('.carousel-controls .prev');
    const nextButton = document.querySelector('.carousel-controls .next');
    let currentSlide = 0;
    let autoSlideInterval;

    // Función para mostrar la diapositiva en el índice especificado
    const showSlide = (index) => {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });
    };

    // Función para avanzar a la siguiente diapositiva
    const nextSlide = () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    };

    // Función para retroceder a la diapositiva anterior
    const prevSlide = () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    };

    // Inicializa el primer slide como activo
    showSlide(currentSlide);

    // Establece el intervalo para cambiar de slide automáticamente cada 5 segundos
    const startAutoSlide = () => {
        autoSlideInterval = setInterval(nextSlide, 5000);
    };

    // Detiene el cambio automático de diapositivas
    const stopAutoSlide = () => {
        clearInterval(autoSlideInterval);
    };

    // Eventos de clic para los botones de navegación
    nextButton.addEventListener('click', () => {
        stopAutoSlide();
        nextSlide();
        startAutoSlide();
    });

    prevButton.addEventListener('click', () => {
        stopAutoSlide();
        prevSlide();
        startAutoSlide();
    });

    // Inicia el carrusel en modo automático
    startAutoSlide();
});
