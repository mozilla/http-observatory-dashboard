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
});