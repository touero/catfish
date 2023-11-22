$(document).ready(function () {
    var clickCounts = {};

    $('.a1').on('click', function (event) {
        event.preventDefault();

        var filename = $(this).siblings('.a3').text();
        clickCounts[filename] = (clickCounts[filename] || 0) + 1;

        if (clickCounts[filename] > 3) {
            Toastify({
                text: 'The download limit may have been reached',
                backgroundColor: 'linear-gradient(to right, #d9cab7, #96183a)',
                className: 'info',
                gravity: 'bottom',
                caption: 'Warning',
            }).showToast();
        } else {
            window.location.href = $(this).attr('href');
        }
    });
});
