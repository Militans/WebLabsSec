document.addEventListener('DOMContentLoaded', function () {
        const sliderWrapper = document.querySelector('.slider-wrapper');
        let slideIndex = 0;

        function showSlide(index) {
            const slideWidth = document.querySelector('.slide').offsetWidth;
            sliderWrapper.style.transform = `translateX(-${slideWidth * index}px)`;
        }

        function nextSlide() {
            slideIndex = (slideIndex + 1) % sliderWrapper.children.length;
            showSlide(slideIndex);
        }

        function prevSlide() {
            slideIndex = (slideIndex - 1 + sliderWrapper.children.length) % sliderWrapper.children.length;
            showSlide(slideIndex);
        }

        setInterval(nextSlide, 3000); // Менять слайд каждые 3 секунды (настройте по необходимости)
    });