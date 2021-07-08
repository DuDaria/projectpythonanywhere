console.log('Привет от JavaScript!');

var stars = document.querySelectorAll('.stars');

$.fn.replaceText = function (e, f, g) {
    return this.each(function () {
        var a = this.firstChild,
            c, b, d = [];
        if (a) {
            do 3 === a.nodeType && (c = a.nodeValue, b = c.replace(e, f), b !== c && (!g && /</.test(b) ? ($(a).before(b), d.push(a)) : a.nodeValue = b));
            while (a = a.nextSibling)
        }
        d.length && $(d).remove()
    })
}; 

$(window).load(function () {
    $(stars).replaceText( /\d+/gi, function f(a){
        return Array(++a).join('<img src="/../../static/img/star_1.svg" alt="star">')
    });
});
