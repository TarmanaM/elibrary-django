document.addEventListener("DOMContentLoaded", function () {
    var toastElList = document.querySelectorAll('.toast');
    toastElList.forEach(function (toastEl) {
        var toast = new bootstrap.Toast(toastEl, { delay: 3000 }); // Hilang setelah 3 detik
        toast.show();
    });
});