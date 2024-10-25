$(document).ready(function() {

    $('#toggleDropdown').click(function(event) {
        event.stopPropagation();
        $('#menu').toggleClass('hidden');
    });

    $(document).click(function() {
        $('#menu').addClass('hidden');
    });
    
    $('.barContainer').on('click', function() {
        $('.barContainer').toggleClass('change');
        $('#dropdownNav').toggleClass("flex hidden");

    });
});