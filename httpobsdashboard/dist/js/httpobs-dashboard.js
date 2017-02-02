$(document).ready(function() {
    'use strict';

    // initialize all the popovers
    $(function () { $('.grade[data-toggle="popover"]').popover(
        {
            html: true,
            placement: 'top',
            trigger: 'hover'
        }
    ) });

    // the glyph info sign ones work a bit differently
    $(function () { $('.glyphicon-info-sign[data-toggle="popover"]').popover(
        {
            delay: {
                'hide': 500
            },
            html: true,
            placement: 'bottom',
            trigger: 'manual'
        }
    ).on('mouseenter', function () {
        var _this = this;
        $(this).popover('show');
        $(".popover").on('mouseleave', function () {
            $(_this).popover('hide');
        });
    }).on('mouseleave', function () {
        var _this = this;
        setTimeout(function () {
            if (!$('.popover:hover').length) {
                $(_this).popover('hide');
            }
        }, 500);
        });
    });

    // Filter websites shown based on filter input
    $('#filter-sites').on('keyup', function (e) {
        var search = e.target.value;
        // Clear previous search
        $('table, tr').show();

        $('tr td:first-of-type a:first-of-type').each(function (i, link) {
            var linkName = link.textContent;
            if (linkName.match(search)) {
                return;
            }
            $(link).closest('tr').hide();
            return;
        });

        $('tbody').each(function (i, tbody) {
            if ($(tbody).children(':visible').length === 0) {
                $(tbody).closest('table').hide();
            }
        });
    });

});
