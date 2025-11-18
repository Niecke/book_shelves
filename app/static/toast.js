// static/toast.js
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.querySelectorAll('.toast').forEach((toast) => {
            toast.style.transition = "opacity .6s";
            toast.style.opacity = 0;
            setTimeout(() => toast.remove(), 600);
        });
    }, 3500); // 3.5 seconds
});
