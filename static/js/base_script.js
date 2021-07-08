document.getElementById('my_select').onchange = function() {
    window.location.href = this.children[this.selectedIndex].getAttribute('href');
}

$(function() {
    if (localStorage.getItem('my_select')) {
        $("#my_select option").eq(localStorage.getItem('my_select')).prop('selected', true);
    }

    $("#my_select").on('change', function() {
        localStorage.setItem('my_select', $('option:selected', this).index());
    });
});
